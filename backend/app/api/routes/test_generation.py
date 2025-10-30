"""
Main test generation endpoint with SSE streaming
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
import asyncio
from typing import AsyncGenerator

from app.models.requests import TestGenerationRequest
from app.models.responses import TestGenerationResponse, ErrorResponse
from app.utils.streaming import SSEStream, StreamingQueue
from app.utils.exceptions import TestGenerationError
from app.config import config
from app.core.services.test_generation_service import TestGenerationService


router = APIRouter()


# Initialize the actual service instance
test_service = TestGenerationService()


async def generate_sse_stream(
        request: TestGenerationRequest
) -> AsyncGenerator[str, None]:
    """
    Generate Server-Sent Events stream for test generation

    Args:
        request: Test generation request

    Yields:
        SSE formatted strings
    """
    stream_queue = StreamingQueue()

    try:
        # Start the generation process in background
        generation_task = asyncio.create_task(
            test_service.generate_tests_stream(request, stream_queue)
        )

        # Stream events as they arrive
        async for event in stream_queue.stream():
            yield event

        # Wait for generation to complete
        result = await generation_task

        # Send final result
        yield await SSEStream.send_event(
            "result",
            {
                "success": True,
                "data": result.dict()
            }
        )

    except TestGenerationError as e:
        logger.error(f"Test generation error: {e.message}")
        yield await SSEStream.send_error_event(
            error_type=e.error_code,
            error_message=e.message,
            details=e.details
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        yield await SSEStream.send_error_event(
            error_type="UNEXPECTED_ERROR",
            error_message=str(e)
        )
    finally:
        stream_queue.close()


@router.post(
    "/generate-tests",
    summary="Generate Tests with Streaming",
    description="Generate test cases using the Intelligent Test Council with real-time SSE updates",
    response_class=StreamingResponse,
    responses={
        200: {
            "description": "Server-Sent Events stream",
            "content": {
                "text/event-stream": {
                    "example": """event: pipeline_start
data: {"function_name": "divide", "message": "🚀 Starting test generation"}

event: llm_chunk
data: {"model": "gemini-2.0-flash", "chunk": "def test_divide_positive():"}

event: pipeline_complete
data: {"total_duration_seconds": 12.5, "message": "🎉 Pipeline complete"}"""
                }
            }
        },
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def generate_tests(request: TestGenerationRequest):
    """
    Generate test cases for a given function with real-time streaming updates

    This endpoint uses Server-Sent Events (SSE) to provide real-time updates during:
    - Code analysis
    - LLM test generation (with streaming chunks)
    - Test clustering
    - Test synthesis (with thinking process)
    - Coverage analysis

    **Event Types:**
    - `pipeline_start`: Generation started
    - `llm_start`: LLM generation starting
    - `llm_chunk`: Streaming LLM output chunk
    - `llm_complete`: LLM generation completed
    - `clustering_start`: Clustering started
    - `cluster_formed`: New cluster identified
    - `clustering_complete`: Clustering completed
    - `synthesis_start`: Synthesis started
    - `synthesis_thinking`: Synthesizer thinking process
    - `synthesis_complete`: Synthesis completed
    - `coverage_start`: Coverage analysis started
    - `coverage_complete`: Coverage analysis completed
    - `pipeline_complete`: Entire pipeline completed
    - `result`: Final result data
    - `error`: Error occurred
    - `heartbeat`: Keep-alive signal

    Args:
        request: Test generation request parameters

    Returns:
        StreamingResponse: SSE stream of generation events
    """
    try:
        logger.info(f"Test generation request received for function: {request.function_name or 'auto-detect'}")

        # Validate request
        if not request.function_code.strip():
            raise HTTPException(
                status_code=400,
                detail="function_code cannot be empty"
            )

        # Return SSE stream
        return StreamingResponse(
            generate_sse_stream(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # Disable buffering in nginx
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start test generation: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start test generation: {str(e)}"
        )


@router.get(
    "/generate-tests/status",
    summary="Get Generation Status",
    description="Get the status of an ongoing test generation (future feature)"
)
async def get_generation_status(task_id: str):
    """
    Get the status of a test generation task

    This is a future feature for tracking long-running generations
    without using SSE.

    Args:
        task_id: Task identifier

    Returns:
        Task status information
    """
    # Future implementation for non-streaming status checks
    raise HTTPException(
        status_code=501,
        detail="Status endpoint not yet implemented. Use SSE streaming for real-time updates."
    )
