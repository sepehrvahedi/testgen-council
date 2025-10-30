"""
Server-Sent Events (SSE) streaming utilities for real-time updates
"""

import json
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator, List
from datetime import datetime
from loguru import logger


class SSEStream:
    """Server-Sent Events stream manager"""

    @staticmethod
    def format_event(event: str, data: Dict[str, Any]) -> str:
        """
        Format data as SSE event

        Args:
            event: Event type
            data: Event data

        Returns:
            Formatted SSE string
        """
        try:
            json_data = json.dumps(data, default=str)
            return f"event: {event}\ndata: {json_data}\n\n"
        except Exception as e:
            logger.error(f"Error formatting SSE event: {e}")
            return f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    @staticmethod
    async def send_event(
            event: str,
            data: Dict[str, Any],
            include_timestamp: bool = True
    ) -> str:
        """
        Create an SSE event with optional timestamp

        Args:
            event: Event type
            data: Event data
            include_timestamp: Whether to include timestamp

        Returns:
            Formatted SSE event string
        """
        if include_timestamp:
            data["timestamp"] = datetime.utcnow().isoformat()

        return SSEStream.format_event(event, data)

    @staticmethod
    async def send_start_event(
            function_name: str,
            models: list,
            roles: list
    ) -> str:
        """Send pipeline start event"""
        return await SSEStream.send_event(
            "pipeline_start",
            {
                "function_name": function_name,
                "models": models,
                "roles": roles,
                "message": f"🚀 Starting test generation for function: {function_name}"
            }
        )

    @staticmethod
    async def send_llm_start_event(
            model: str,
            role: str,
            model_index: int,
            total_models: int
    ) -> str:
        """Send LLM generation start event"""
        return await SSEStream.send_event(
            "llm_start",
            {
                "model": model,
                "role": role,
                "model_index": model_index,
                "total_models": total_models,
                "message": f"🤖 [{model_index}/{total_models}] Starting generation with {model} as {role}"
            }
        )

    @staticmethod
    async def send_llm_chunk_event(
            model: str,
            role: str,
            chunk: str,
            chunk_index: int
    ) -> str:
        """Send LLM streaming chunk event"""
        return await SSEStream.send_event(
            "llm_chunk",
            {
                "model": model,
                "role": role,
                "chunk": chunk,
                "chunk_index": chunk_index
            },
            include_timestamp=False  # High-frequency events don't need timestamps
        )

    @staticmethod
    async def send_llm_complete_event(
            model: str,
            role: str,
            tests_generated: int,
            duration: float
    ) -> str:
        """Send LLM generation complete event"""
        return await SSEStream.send_event(
            "llm_complete",
            {
                "model": model,
                "role": role,
                "tests_generated": tests_generated,
                "duration_seconds": round(duration, 2),
                "message": f"✅ {model} ({role}) generated {tests_generated} tests in {duration:.2f}s"
            }
        )

    @staticmethod
    async def send_clustering_start_event(
            method: str,
            total_tests: int
    ) -> str:
        """Send clustering start event"""
        return await SSEStream.send_event(
            "clustering_start",
            {
                "method": method,
                "total_tests": total_tests,
                "message": f"🧩 Starting {method} clustering on {total_tests} tests"
            }
        )

    @staticmethod
    async def send_cluster_formed_event(
            cluster_id: int,
            size: int,
            category: Optional[str],
            representative_test: Optional[str],
            tests: List[str]
    ) -> str:
        """Send cluster formed event with all tests"""
        return await SSEStream.send_event(
            "cluster_formed",
            {
                "cluster_id": cluster_id,
                "size": size,
                "category": category,
                "representative_test": representative_test[:100] + "..." if representative_test and len(representative_test) > 100 else representative_test,
                "tests": tests,
                "message": f"📊 Cluster {cluster_id}: {size} tests ({category or 'uncategorized'})"
            }
        )

    @staticmethod
    async def send_clustering_complete_event(
            total_clusters: int,
            noise_tests: int,
            duration: float
    ) -> str:
        """Send clustering complete event"""
        return await SSEStream.send_event(
            "clustering_complete",
            {
                "total_clusters": total_clusters,
                "noise_tests": noise_tests,
                "duration_seconds": round(duration, 2),
                "message": f"✅ Clustering complete: {total_clusters} clusters, {noise_tests} noise tests ({duration:.2f}s)"
            }
        )

    @staticmethod
    async def send_synthesis_start_event(
            clusters_to_synthesize: int
    ) -> str:
        """Send synthesis start event"""
        return await SSEStream.send_event(
            "synthesis_start",
            {
                "clusters_to_synthesize": clusters_to_synthesize,
                "message": f"🔄 Starting synthesis for {clusters_to_synthesize} clusters"
            }
        )

    @staticmethod
    async def send_synthesis_thinking_event(
            thinking_chunk: str
    ) -> str:
        """Send synthesis thinking chunk event"""
        return await SSEStream.send_event(
            "synthesis_thinking",
            {
                "thinking": thinking_chunk
            },
            include_timestamp=False
        )

    @staticmethod
    async def send_synthesis_complete_event(
            final_tests_count: int,
            duration: float
    ) -> str:
        """Send synthesis complete event"""
        return await SSEStream.send_event(
            "synthesis_complete",
            {
                "final_tests_count": final_tests_count,
                "duration_seconds": round(duration, 2),
                "message": f"✅ Synthesis complete: {final_tests_count} final tests ({duration:.2f}s)"
            }
        )

    @staticmethod
    async def send_coverage_start_event() -> str:
        """Send coverage analysis start event"""
        return await SSEStream.send_event(
            "coverage_start",
            {
                "message": "📊 Starting code coverage analysis"
            }
        )

    @staticmethod
    async def send_coverage_complete_event(
            coverage_percentage: float,
            passed_tests: int,
            failed_tests: int,
            total_tests: int,
            duration: float
    ) -> str:
        """Send coverage analysis complete event"""
        return await SSEStream.send_event(
            "coverage_complete",
            {
                "coverage_percentage": round(coverage_percentage, 2),
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "total_tests": total_tests,
                "success_rate": round((passed_tests / total_tests * 100) if total_tests > 0 else 0, 2),
                "duration_seconds": round(duration, 2),
                "message": f"✅ Coverage: {coverage_percentage:.1f}% | Tests: {passed_tests}/{total_tests} passed ({duration:.2f}s)"
            }
        )

    @staticmethod
    async def send_complete_event(
            total_duration: float,
            statistics: Dict[str, Any]
    ) -> str:
        """Send pipeline complete event"""
        return await SSEStream.send_event(
            "pipeline_complete",
            {
                "total_duration_seconds": round(total_duration, 2),
                "statistics": statistics,
                "message": f"🎉 Pipeline complete in {total_duration:.2f}s"
            }
        )

    @staticmethod
    async def send_error_event(
            error_type: str,
            error_message: str,
            details: Optional[Dict[str, Any]] = None
    ) -> str:
        """Send error event"""
        return await SSEStream.send_event(
            "error",
            {
                "error_type": error_type,
                "error_message": error_message,
                "details": details or {}
            }
        )

    @staticmethod
    async def send_heartbeat() -> str:
        """Send heartbeat event to keep connection alive"""
        return await SSEStream.send_event(
            "heartbeat",
            {"status": "alive"},
            include_timestamp=False
        )


class StreamingQueue:
    """Queue for managing streaming events"""

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self._closed = False

    async def put(self, event: str):
        """Add event to queue"""
        if not self._closed:
            await self.queue.put(event)

    async def get(self) -> str:
        """Get event from queue"""
        return await self.queue.get()

    def close(self):
        """Close the queue"""
        self._closed = True

    def is_closed(self) -> bool:
        """Check if queue is closed"""
        return self._closed

    async def stream(self) -> AsyncGenerator[str, None]:
        """Stream events from queue"""
        while not self._closed or not self.queue.empty():
            try:
                event = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                yield event
            except asyncio.TimeoutError:
                # Send heartbeat if no events for 1 second
                yield await SSEStream.send_heartbeat()
            except Exception as e:
                logger.error(f"Error streaming event: {e}")
                break
