"""
Main orchestration service for test generation pipeline
Coordinates all components and manages the complete workflow
"""

import ast
import re
import time
from datetime import datetime
from typing import Dict, Optional

from loguru import logger

from app.config import config
from app.core.ast_clusterer import ASTClusterer
from app.core.code_analyzer import CodeAnalyzer
from app.core.coverage_analyzer import CoverageAnalyzer
from app.core.llm_council import LLMCouncil
from app.core.test_classifier import TestClassifier
from app.core.test_synthesizer import TestSynthesizer
from app.models.experiments import ExperimentConfig
from app.models.requests import TestGenerationRequest
from app.models.responses import (
    TestGenerationResponse,
    LLMOutput,
    ClusterInfo,
    CoverageResult,
    Statistics
)
from app.utils.exceptions import TestGenerationError
from app.utils.streaming import StreamingQueue, SSEStream


class TestGenerationService:
    """Orchestrates the complete test generation pipeline"""
    async def generate_tests_batch(
            self,
            request: TestGenerationRequest,
            experiment_config: Optional['ExperimentConfig'] = None
    ) -> TestGenerationResponse:
        """
        Generate tests WITHOUT streaming (for batch processing)
        Supports experiment configurations for ablation studies
        """
        pipeline_start = time.time()

        try:
            # Apply experiment configuration if provided
            if experiment_config:
                request = self._apply_experiment_config(request, experiment_config)

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

            # ====================
            # STAGE 2: LLM COUNCIL GENERATION
            # ====================
            logger.info("Stage 2: LLM Council Generation")
            llm_start = time.time()

            async with LLMCouncil(streaming_queue=None) as council:
                # ✅ FIX: Check if we should use generic or role-based generation
                if experiment_config and not experiment_config.use_role_personas:
                    # Ablation 2: No Roles - use generic prompts
                    logger.info("Using generic generation (No Roles)")
                    llm_results = await council.generate_tests_generic(
                        function_context=function_context,
                        function_name=function_name,
                        models=request.models
                    )
                else:
                    # Normal role-based generation
                    logger.info("Using role-based generation")
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

            logger.info(f"Generated {len(all_tests)} total tests")

            # ====================
            # STAGE 3: CLASSIFICATION
            # ====================
            logger.info("Stage 3: Test Classification")
            classifier = TestClassifier()
            test_categories = classifier.classify_tests(all_tests)

            # ====================
            # STAGE 4: CLUSTERING (Optional based on experiment)
            # ====================
            cluster_map = {}
            cluster_infos = []
            clusters_for_synthesis = {}
            clustering_duration = 0.0

            if experiment_config is None or experiment_config.enable_clustering:
                logger.info("Stage 4: Clustering")
                clustering_start = time.time()

                clusterer = ASTClusterer(
                    method=request.clustering_method,
                    eps=request.eps,
                    min_samples=request.min_samples
                )

                cluster_map = clusterer.cluster_tests(all_tests)

                for cluster_id, test_indices in cluster_map.items():
                    if cluster_id == -1:
                        continue

                    cluster_tests = [all_tests[i] for i in test_indices]
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

                    clusters_for_synthesis[cluster_id] = {
                        "tests": cluster_tests,
                        "category": most_common_category
                    }

                clustering_duration = time.time() - clustering_start
            else:
                # ✅ FIX: Ablation 3 - Each test is its own cluster (n tests = n clusters)
                logger.info("Stage 4: SKIPPED (Ablation: No Clustering - Each test as separate cluster)")

                for i, test in enumerate(all_tests):
                    cluster_id = i
                    category = test_categories.get(str(i), "positive")

                    cluster_infos.append(ClusterInfo(
                        cluster_id=cluster_id,
                        size=1,
                        category=category,
                        representative_test=test,
                        tests=[test]
                    ))

                    clusters_for_synthesis[cluster_id] = {
                        "tests": [test],
                        "category": category
                    }

            # ====================
            # STAGE 5: SYNTHESIS (Optional based on experiment)
            # ====================
            final_tests = ""
            synthesis_duration = 0.0

            if experiment_config is None or experiment_config.enable_synthesis:
                logger.info("Stage 5: Test Synthesis")
                synthesis_start = time.time()

                async with TestSynthesizer(streaming_queue=None) as synthesizer:
                    cluster_synthesized_tests = await synthesizer.synthesize_clusters_individually(
                        clusters=clusters_for_synthesis,
                        function_name=function_name,
                        function_code=request.function_code
                    )

                    final_tests = await synthesizer.create_final_test_file(
                        cluster_tests=cluster_synthesized_tests,
                        function_name=function_name,
                        function_code=request.function_code
                    )

                synthesis_duration = time.time() - synthesis_start
            else:
                # ✅ FIX: Ablation 4 - Include ALL tests (no random selection)
                logger.info("Stage 5: SKIPPED (Ablation: No Synthesis - Including ALL tests)")
                final_tests = self._combine_all_tests_no_synthesis(
                    clusters_for_synthesis,
                    function_name,
                    request.function_code
                )

            # ✅ FIX: Count test functions more robustly
            final_test_count = self._count_test_functions(final_tests)

            # ====================
            # STAGE 6: COVERAGE ANALYSIS
            # ====================
            coverage_result = None
            coverage_duration = 0.0

            if request.enable_coverage:
                logger.info("Stage 6: Coverage Analysis")
                coverage_start = time.time()

                coverage_analyzer = CoverageAnalyzer()

                try:
                    # ✅ UPDATED: Pass enable_mutation flag
                    coverage_data = await coverage_analyzer.analyze_coverage(
                        function_code=request.function_code,
                        test_code=final_tests,
                        function_name=function_name,
                        enable_mutation=request.enable_mutation  # ✅ NEW
                    )

                    coverage_result = CoverageResult(**coverage_data)
                    coverage_duration = time.time() - coverage_start

                except Exception as e:
                    logger.error(f"Coverage analysis failed: {e}")

            # ====================
            # BUILD RESPONSE
            # ====================
            total_duration = time.time() - pipeline_start

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

            statistics = Statistics(
                total_raw_tests=len(all_tests),
                total_clusters=len(clusters_for_synthesis),
                noise_tests=len(cluster_map.get(-1, [])) if cluster_map else 0,
                final_tests=final_test_count,
                total_duration_seconds=total_duration,
                llm_duration_seconds=llm_duration,
                clustering_duration_seconds=clustering_duration,
                synthesis_duration_seconds=synthesis_duration,
                coverage_duration_seconds=coverage_duration if request.enable_coverage else None
            )

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

            logger.info(f"Batch pipeline complete in {total_duration:.2f}s")

            return response

        except Exception as e:
            logger.error(f"Batch pipeline failed: {e}", exc_info=True)
            raise TestGenerationError(
                message=f"Batch test generation failed: {str(e)}",
                details={"stage": "batch_pipeline"}
            )


    def _combine_all_tests_no_synthesis(
            self,
            clusters: Dict[int, Dict],
            function_name: str,
            function_code: str
    ) -> str:
        """
        ✅ FIXED: Combine ALL tests from clusters (for Ablation 4: No Synthesis)
        Properly extract ONLY test functions, avoiding nested structures
        """

        # Collect all tests from all clusters
        all_tests = []
        for cluster_id, cluster_data in clusters.items():
            all_tests.extend(cluster_data["tests"])

        logger.info(f"Including ALL {len(all_tests)} tests without synthesis")

        # Extract test functions using a cleaner approach
        test_functions = []
        seen_tests = set()  # Deduplicate identical tests

        for i, test in enumerate(all_tests):
            test_code = test.strip()

            # Remove markdown code fences
            test_code = re.sub(r'^```(?:python)?\s*\n?', '', test_code)
            test_code = re.sub(r'\n?```\s*$', '', test_code)
            test_code = test_code.strip()

            try:
                # Parse the entire block
                tree = ast.parse(test_code)

                # Extract ONLY test functions
                for node in tree.body:  # Use .body instead of iter_child_nodes
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        # Convert back to source code
                        test_func_source = ast.unparse(node)

                        # Deduplicate
                        test_hash = hash(test_func_source)
                        if test_hash not in seen_tests:
                            seen_tests.add(test_hash)
                            test_functions.append(test_func_source)

            except SyntaxError as e:
                logger.warning(f"Failed to parse test {i}: {e}")

                # Fallback: Extract test function using regex
                test_pattern = r'(def test_\w+\([^)]*\):(?:\n(?:    |\t).+)*)'
                matches = re.findall(test_pattern, test_code, re.MULTILINE)

                for match in matches:
                    test_hash = hash(match)
                    if test_hash not in seen_tests:
                        seen_tests.add(test_hash)
                        test_functions.append(match)

        logger.info(f"Extracted {len(test_functions)} unique test functions")

        # Build final test file
        final_test_file = f'''import pytest
from typing import Any

# Tests for {function_name}
# Generated via No Synthesis Ablation (All {len(test_functions)} tests included)

# Original function
{function_code}

'''

        # Add all test functions with proper spacing
        for test_func in test_functions:
            # Ensure proper indentation (no nested indents)
            lines = test_func.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove excessive indentation
                if line.strip():
                    # Keep only base indentation (4 spaces for function body)
                    if line.startswith('def test_'):
                        cleaned_lines.append(line)
                    else:
                        # Function body - ensure 4-space indent
                        cleaned_lines.append('    ' + line.lstrip())
                else:
                    cleaned_lines.append('')

            final_test_file += '\n'.join(cleaned_lines) + '\n\n'

        return final_test_file



    def _count_test_functions(self, code: str) -> int:
        """
        ✅ FIX: Robustly count test functions
        Looks for actual function definitions, not just 'def test_'
        """
        import re

        # Pattern to match function definitions starting with 'test'
        # Handles: def test_name(...):
        pattern = r'^\s*def\s+test\w*\s*\('

        matches = re.findall(pattern, code, re.MULTILINE)
        count = len(matches)

        logger.info(f"Counted {count} test functions in generated code")
        return count


    def _apply_experiment_config(
            self,
            request: TestGenerationRequest,
            config: 'ExperimentConfig'
    ) -> TestGenerationRequest:
        """Apply experiment configuration to request"""
        # Modify models
        if config.models:
            request.models = config.models

        # Modify roles (empty list = no roles)
        if config.roles is not None:
            request.roles = config.roles

        # Modify clustering settings
        request.clustering_method = config.clustering_method
        request.eps = config.eps
        request.min_samples = config.min_samples

        # ✅ NEW: Apply mutation testing flag
        request.enable_mutation = config.enable_mutation

        return request



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

            # Send cluster formation events and prepare cluster data
            cluster_infos = []
            clusters_for_synthesis = {}

            for cluster_id, test_indices in cluster_map.items():
                if cluster_id == -1:  # Skip noise cluster for now
                    continue

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

                # Store for synthesis
                clusters_for_synthesis[cluster_id] = {
                    "tests": cluster_tests,
                    "category": most_common_category
                }

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
                    total_clusters=len(clusters_for_synthesis),
                    noise_tests=len(cluster_map.get(-1, [])),
                    duration=clustering_duration
                )
            )

            # ====================
            # STAGE 5: SYNTHESIS (TWO-PHASE)
            # ====================
            logger.info("Stage 5: Two-Phase Test Synthesis")
            synthesis_start = time.time()

            async with TestSynthesizer(streaming_queue=stream_queue) as synthesizer:
                # PHASE 1: Synthesize each cluster individually
                logger.info(f"Phase 1: Synthesizing {len(clusters_for_synthesis)} clusters individually")

                cluster_synthesized_tests = await synthesizer.synthesize_clusters_individually(
                    clusters=clusters_for_synthesis,
                    function_name=function_name,
                    function_code=request.function_code
                )

                # PHASE 2: Create final unified test file
                logger.info("Phase 2: Creating final unified test file")

                final_tests = await synthesizer.create_final_test_file(
                    cluster_tests=cluster_synthesized_tests,
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
                    # ✅ UPDATED: Pass enable_mutation flag
                    coverage_data = await coverage_analyzer.analyze_coverage(
                        function_code=request.function_code,
                        test_code=final_tests,
                        function_name=function_name,
                        enable_mutation=request.enable_mutation  # ✅ NEW
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
                total_clusters=len(clusters_for_synthesis),
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
