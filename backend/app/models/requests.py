"""
Pydantic request models for API validation
"""

from typing import Optional, List

from pydantic import BaseModel, Field, validator


class TestGenerationRequest(BaseModel):
    """Request model for test generation endpoint"""

    function_code: str = Field(
        ...,
        description="The Python function code to generate tests for",
        min_length=10,
        example="""def add(a: int, b: int) -> int:
    \"\"\"Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    \"\"\"
    return a + b"""
    )

    function_name: Optional[str] = Field(
        None,
        description="Name of the function (auto-detected if not provided)",
        example="add"
    )

    clustering_method: str = Field(
        default="vector",
        description="Clustering method to use: 'vector' (DBSCAN) or 'hash' (structural hashing)",
        example="vector"
    )

    eps: float = Field(
        default=0.3,
        ge=0.1,
        le=1.0,
        description="DBSCAN epsilon parameter for vector clustering (0.1-1.0)",
        example=0.3
    )

    min_samples: int = Field(
        default=2,
        ge=1,
        le=5,
        description="DBSCAN min_samples parameter (1-5)",
        example=2
    )

    models: Optional[List[str]] = Field(
        default=None,
        description="List of model IDs to use (uses all if not specified)",
        example=["gemini-2.0-flash", "deepseek-chat"]
    )

    roles: Optional[List[str]] = Field(
        default=None,
        description="List of role IDs to use (uses all if not specified)",
        example=["qa_engineer", "agent_of_chaos"]
    )

    enable_coverage: bool = Field(
        default=True,
        description="Enable code coverage analysis",
        example=True
    )

    enable_mutation: bool = Field(
        default=True,
        description="Enable mutation testing (gold standard metric for test quality, can be slow)",
        example=True
    )

    stream_updates: bool = Field(
        default=True,
        description="Enable real-time streaming updates via SSE",
        example=True
    )

    @validator('clustering_method')
    def validate_clustering_method(cls, v):
        """Validate clustering method"""
        allowed_methods = ['vector', 'hash']
        if v not in allowed_methods:
            raise ValueError(f"clustering_method must be one of {allowed_methods}")
        return v

    @validator('function_code')
    def validate_function_code(cls, v):
        """Validate function code is not empty and contains 'def'"""
        if not v.strip():
            raise ValueError("function_code cannot be empty")
        if 'def ' not in v:
            raise ValueError("function_code must contain a Python function definition")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "function_code": """def divide(a: int, b: int) -> float:
    \"\"\"Divide two numbers.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division
        
    Raises:
        ZeroDivisionError: If b is zero
    \"\"\"
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b""",
                "function_name": "divide",
                "clustering_method": "vector",
                "eps": 0.3,
                "min_samples": 2,
                "enable_coverage": True,
                "enable_mutation": True,
                "stream_updates": True
            }
        }


class ConfigRequest(BaseModel):
    """Request model for updating configuration (future use)"""

    max_concurrent_llms: Optional[int] = Field(
        None,
        ge=1,
        le=12,
        description="Maximum concurrent LLM calls"
    )

    request_timeout: Optional[int] = Field(
        None,
        ge=30,
        le=600,
        description="Request timeout in seconds"
    )
