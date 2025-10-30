"""
Custom exception classes for the application
"""

from typing import Optional, Dict, Any


class TestGenerationError(Exception):
    """Base exception for test generation errors"""

    def __init__(
            self,
            message: str,
            error_code: str = "GENERATION_ERROR",
            details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class CodeAnalysisError(TestGenerationError):
    """Error during code analysis"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CODE_ANALYSIS_ERROR",
            details=details
        )


class LLMError(TestGenerationError):
    """Error during LLM generation"""

    def __init__(
            self,
            message: str,
            model: Optional[str] = None,
            role: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if model:
            error_details["model"] = model
        if role:
            error_details["role"] = role

        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            details=error_details
        )


class ClusteringError(TestGenerationError):
    """Error during clustering"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CLUSTERING_ERROR",
            details=details
        )


class SynthesisError(TestGenerationError):
    """Error during test synthesis"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="SYNTHESIS_ERROR",
            details=details
        )


class CoverageError(TestGenerationError):
    """Error during coverage analysis"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="COVERAGE_ERROR",
            details=details
        )


class ValidationError(TestGenerationError):
    """Input validation error"""

    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        error_details = details or {}
        if field:
            error_details["field"] = field

        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=error_details
        )


class TimeoutError(TestGenerationError):
    """Operation timeout error"""

    def __init__(self, message: str, timeout_seconds: Optional[float] = None):
        details = {}
        if timeout_seconds:
            details["timeout_seconds"] = timeout_seconds

        super().__init__(
            message=message,
            error_code="TIMEOUT_ERROR",
            details=details
        )


class ConfigurationError(TestGenerationError):
    """Configuration error"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            details=details
        )
