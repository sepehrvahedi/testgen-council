"""
Main orchestration service for test generation pipeline
Coordinates all components and manages the complete workflow
"""

import asyncio
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger

from app.config import config
from app.models.requests import TestGenerationRequest
from app.models.responses import (
    TestGenerationResponse,
    LLMOutput,
    ClusterInfo,
    CoverageResult,
    Statistics
)
from app.core.code_analyzer import CodeAnalyzer
from app.core.llm_council import LLMCouncil
from app.core.test_classifier import TestClassifier
from app.core.ast_clusterer import ASTClusterer
from app.core.test_synthesizer import TestSynthesizer
from app.core.coverage_analyzer import CoverageAnalyzer
from app.utils.streaming import StreamingQueue, SSEStream
from app.utils.exceptions import TestGenerationError


class TestGenerationService:
    """Orchestrates the complete test generation pipeline"""

    async def generate_tests_stream(
            self,
            request: TestGenerationRequest,
            stream_queue: StreamingQueue
    ) -> TestGenerationResponse:
        """
        Generate tests with streaming updates

        Args:
            request: Test generation request
            stream_queue: Queue for SSE events

        Returns:
            Complete test generation response
        """
        pipeline_start = time.time()

        try:
            # ====================
            # STAGE 1: CODE ANALYSIS
            # ====================
            logger.info("Stage 1: Code Analysis")
            analyzer = CodeAnalyzer()

            function_metadata = analyzer.analyze_function(
                function_code=request.function_code,
                function_name=request.function_name
            )

            function_name = function_metadata["name"]
            function_context = analyzer.generate_test_context()
            test_hints = analyzer.get_test_hints()

            # Send pipeline start event
            await stream_queue.put(
                await SSEStream.send_start_event(
                    function_name=function_name,
                    models=request.models or list(config.LLM_MODELS.keys()),
                    roles=request.roles or list(config.ROLES.keys())
                )
            )

            # ====================
            # STAGE 2: LLM COUNCIL GENERATION
            # ====================
            logger.info("Stage 2: LLM Council Generation")
            llm_start = time.time()

            async with LLMCouncil(streaming_queue=stream_queue) as council:
                llm_results = await council.generate_tests_parallel(
                    function_context=function_context,
                    function_name=function_name,
                    test_hints=test_hints,
                    models=request.models,
                    roles=request.roles
                )

            llm_duration = time.time() - llm_start

            # Collect all tests
            all_tests = []
            for result in llm_results:
                all_tests.extend(result["tests"])

            logger.info(f"Generated {len(all_tests)} total tests from {len(llm_results)} models")

            # ====================
            # STAGE 3: CLASSIFICATION
            # ====================
            logger.info("Stage 3: Test Classification")

            classifier = TestClassifier()
            test_categories = classifier.classify_tests(all_tests)

            # ====================
            # STAGE 4: CLUSTERING
            # ====================
            logger.info("Stage 4: AST-based Clustering")
            clustering_start = time.time()

            await stream_queue.put(
                await SSEStream.send_clustering_start_event(
                    method=request.clustering_method,
                    total_tests=len(all_tests)
                )
            )

            clusterer = ASTClusterer(
                method=request.clustering_method,
                eps=request.eps,
                min_samples=request.min_samples
            )

            cluster_map = clusterer.cluster_tests(all_tests)

            # Send cluster formation events
            cluster_infos = []
            for cluster_id, test_indices in cluster_map.items():
                cluster_tests = [all_tests[i] for i in test_indices]

                # Determine category
                categories = [test_categories.get(str(i), "positive") for i in test_indices]
                most_common_category = max(set(categories), key=categories.count)

                cluster_info = clusterer.get_cluster_info(cluster_id, all_tests, cluster_map)
                cluster_info["category"] = most_common_category

                cluster_infos.append(ClusterInfo(
                    cluster_id=cluster_id,
                    size=len(test_indices),
                    category=most_common_category,
                    representative_test=cluster_info.get("representative_test", ""),
                    tests=cluster_tests
                ))


                await stream_queue.put(
                    await SSEStream.send_cluster_formed_event(
                        cluster_id=cluster_id,
                        size=len(test_indices),
                        category=most_common_category,
                        representative_test=cluster_info.get("representative_test"),
                        tests=cluster_tests
                    )
                )


            clustering_duration = time.time() - clustering_start

            await stream_queue.put(
                await SSEStream.send_clustering_complete_event(
                    total_clusters=len([c for c in cluster_map.keys() if c != -1]),
                    noise_tests=len(cluster_map.get(-1, [])),
                    duration=clustering_duration
                )
            )

            # ====================
            # STAGE 5: SYNTHESIS
            # ====================
            logger.info("Stage 5: Test Synthesis")
            synthesis_start = time.time()

            # Prepare clusters for synthesis (exclude noise)
            synthesis_clusters = {}
            for cluster_id, test_indices in cluster_map.items():
                if cluster_id != -1:  # Exclude noise
                    synthesis_clusters[cluster_id] = [all_tests[i] for i in test_indices]

            async with TestSynthesizer(streaming_queue=stream_queue) as synthesizer:
                final_tests = await synthesizer.synthesize_tests(
                    clusters=synthesis_clusters,
                    function_name=function_name,
                    function_code=request.function_code
                )

            synthesis_duration = time.time() - synthesis_start

            # Count final tests
            final_test_count = final_tests.count("def test_")

            await stream_queue.put(
                await SSEStream.send_synthesis_complete_event(
                    final_tests_count=final_test_count,
                    duration=synthesis_duration
                )
            )

            # ====================
            # STAGE 6: COVERAGE ANALYSIS (Optional)
            # ====================
            coverage_result = None
            coverage_duration = 0.0

            if request.enable_coverage:
                logger.info("Stage 6: Coverage Analysis")
                coverage_start = time.time()

                await stream_queue.put(
                    await SSEStream.send_coverage_start_event()
                )

                coverage_analyzer = CoverageAnalyzer()

                try:
                    coverage_data = await coverage_analyzer.analyze_coverage(
                        function_code=request.function_code,
                        test_code=final_tests,
                        function_name=function_name
                    )

                    coverage_result = CoverageResult(**coverage_data)

                    coverage_duration = time.time() - coverage_start

                    await stream_queue.put(
                        await SSEStream.send_coverage_complete_event(
                            coverage_percentage=coverage_data["coverage_percentage"],
                            passed_tests=coverage_data["passed_tests"],
                            failed_tests=coverage_data["failed_tests"],
                            total_tests=coverage_data["total_tests"],
                            duration=coverage_duration
                        )
                    )

                except Exception as e:
                    logger.error(f"Coverage analysis failed: {e}", exc_info=True)
                    # Continue without coverage data

            # ====================
            # BUILD RESPONSE
            # ====================
            total_duration = time.time() - pipeline_start

            # Build LLM outputs
            llm_outputs = [
                LLMOutput(
                    model=result["model"],
                    role=result["role"],
                    tests=result["tests"],
                    raw_output=result["raw_output"],
                    tokens_used=result.get("tokens_used"),
                    duration_seconds=result["duration_seconds"]
                )
                for result in llm_results
            ]

            # Build statistics
            statistics = Statistics(
                total_raw_tests=len(all_tests),
                total_clusters=len([c for c in cluster_map.keys() if c != -1]),
                noise_tests=len(cluster_map.get(-1, [])),
                final_tests=final_test_count,
                total_duration_seconds=total_duration,
                llm_duration_seconds=llm_duration,
                clustering_duration_seconds=clustering_duration,
                synthesis_duration_seconds=synthesis_duration,
                coverage_duration_seconds=coverage_duration if request.enable_coverage else None
            )

            # Send pipeline complete event
            await stream_queue.put(
                await SSEStream.send_complete_event(
                    total_duration=total_duration,
                    statistics=statistics.dict()
                )
            )

            # Build final response
            response = TestGenerationResponse(
                success=True,
                function_name=function_name,
                final_tests=final_tests,
                llm_outputs=llm_outputs,
                clusters=cluster_infos,
                coverage=coverage_result,
                statistics=statistics,
                timestamp=datetime.utcnow()
            )

            logger.info(f"Pipeline complete in {total_duration:.2f}s")

            return response

        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)

            # Send error event
            await stream_queue.put(
                await SSEStream.send_error_event(
                    error_type=type(e).__name__,
                    error_message=str(e)
                )
            )

            raise TestGenerationError(
                message=f"Test generation pipeline failed: {str(e)}",
                details={"stage": "pipeline_orchestration"}
            )