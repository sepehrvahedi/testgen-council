"""
Pydantic response models for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class ModelInfo(BaseModel):
    """Model information"""
    id: str = Field(..., description="Model identifier")
    name: str = Field(..., description="Display name")
    icon: str = Field(..., description="Icon emoji")
    color: str = Field(..., description="Color code")
    roles: List[str] = Field(..., description="Assigned roles")


class RoleInfo(BaseModel):
    """Role information"""
    id: str = Field(..., description="Role identifier")
    name: str = Field(..., description="Role name")
    philosophy: str = Field(..., description="Role philosophy")
    icon: str = Field(..., description="Icon emoji")
    color: str = Field(..., description="Color code")
    focus_categories: List[str] = Field(..., description="Focus test categories")


class ClusteringMethodInfo(BaseModel):
    """Clustering method information"""
    id: str = Field(..., description="Method identifier")
    name: str = Field(..., description="Method name")
    description: str = Field(..., description="Method description")


class ConfigResponse(BaseModel):
    """Configuration response"""
    models: List[ModelInfo] = Field(..., description="Available models")
    roles: List[RoleInfo] = Field(..., description="Available roles")
    clustering_methods: List[ClusteringMethodInfo] = Field(..., description="Available clustering methods")
    test_categories: List[str] = Field(..., description="Test categories")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status", example="healthy")
    version: str = Field(..., description="API version", example="1.0.0")
    timestamp: datetime = Field(..., description="Response timestamp")
    models_available: int = Field(..., description="Number of models configured")
    roles_available: int = Field(..., description="Number of roles configured")


class LLMOutput(BaseModel):
    """Individual LLM output"""
    model: str = Field(..., description="Model identifier")
    role: str = Field(..., description="Role identifier")
    tests: List[str] = Field(..., description="Generated test functions")
    raw_output: str = Field(..., description="Raw LLM output")
    tokens_used: Optional[int] = Field(None, description="Tokens used")
    duration_seconds: Optional[float] = Field(None, description="Generation duration")


class ClusterInfo(BaseModel):
    """Cluster information"""
    cluster_id: int = Field(..., description="Cluster identifier (-1 for noise)")
    size: int = Field(..., description="Number of tests in cluster")
    category: Optional[str] = Field(None, description="Detected category")
    representative_test: Optional[str] = Field(None, description="Representative test")
    tests: List[str] = Field(..., description="Test functions in cluster")


class CoverageResult(BaseModel):
    """Coverage analysis result"""
    total_lines: int = Field(..., description="Total lines of code")
    covered_lines: int = Field(..., description="Covered lines")
    missing_lines: List[int] = Field(..., description="Missing line numbers")
    coverage_percentage: float = Field(..., description="Coverage percentage")
    passed_tests: int = Field(..., description="Number of passed tests")
    failed_tests: int = Field(..., description="Number of failed tests")
    total_tests: int = Field(..., description="Total number of tests")
    success_rate: float = Field(..., description="Test success rate percentage")


class Statistics(BaseModel):
    """Generation statistics"""
    total_raw_tests: int = Field(..., description="Total tests before clustering")
    total_clusters: int = Field(..., description="Number of clusters formed")
    noise_tests: int = Field(..., description="Tests marked as noise")
    final_tests: int = Field(..., description="Final synthesized tests")
    total_duration_seconds: float = Field(..., description="Total generation time")
    llm_duration_seconds: float = Field(..., description="LLM generation time")
    clustering_duration_seconds: float = Field(..., description="Clustering time")
    synthesis_duration_seconds: float = Field(..., description="Synthesis time")
    coverage_duration_seconds: Optional[float] = Field(None, description="Coverage analysis time")


class TestGenerationResponse(BaseModel):
    """Complete test generation response"""
    success: bool = Field(..., description="Operation success status")
    function_name: str = Field(..., description="Target function name")
    final_tests: str = Field(..., description="Final synthesized test code")
    llm_outputs: List[LLMOutput] = Field(..., description="Individual LLM outputs")
    clusters: List[ClusterInfo] = Field(..., description="Cluster information")
    coverage: Optional[CoverageResult] = Field(None, description="Coverage results")
    statistics: Statistics = Field(..., description="Generation statistics")
    timestamp: datetime = Field(..., description="Generation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "function_name": "divide",
                "final_tests": "# Synthesized test suite...",
                "llm_outputs": [
                    {
                        "model": "gemini-2.0-flash",
                        "role": "qa_engineer",
                        "tests": ["def test_divide_positive(): ..."],
                        "raw_output": "...",
                        "tokens_used": 1500,
                        "duration_seconds": 2.5
                    }
                ],
                "clusters": [
                    {
                        "cluster_id": 0,
                        "size": 5,
                        "category": "positive",
                        "representative_test": "def test_divide_positive(): ...",
                        "tests": ["def test_divide_positive(): ..."]
                    }
                ],
                "coverage": {
                    "total_lines": 10,
                    "covered_lines": 9,
                    "missing_lines": [5],
                    "coverage_percentage": 90.0,
                    "passed_tests": 8,
                    "failed_tests": 0,
                    "total_tests": 8,
                    "success_rate": 100.0
                },
                "statistics": {
                    "total_raw_tests": 25,
                    "total_clusters": 5,
                    "noise_tests": 3,
                    "final_tests": 8,
                    "total_duration_seconds": 12.5,
                    "llm_duration_seconds": 8.0,
                    "clustering_duration_seconds": 1.5,
                    "synthesis_duration_seconds": 2.5,
                    "coverage_duration_seconds": 0.5
                },
                "timestamp": "2025-10-21T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")


class StreamEvent(BaseModel):
    """Server-Sent Event structure"""
    event: str = Field(..., description="Event type")
    data: Dict[str, Any] = Field(..., description="Event data")

    def to_sse(self) -> str:
        """Convert to SSE format"""
        import json
        return f"event: {self.event}\ndata: {json.dumps(self.data, default=str)}\n\n"
