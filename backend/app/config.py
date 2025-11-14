"""
Configuration module for Intelligent Test Council
Manages API keys, model configurations, and role definitions
"""

from typing import Dict, Any, List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Configuration
    OPENAI_API_KEY: str = Field(
        default="",
        description="OpenAI API Key"
    )
    OPENAI_BASE_URL: str = Field(
        default="https://api.gapgpt.app/v1",
        description="OpenAI API Base URL"
    )

    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=True, description="Debug mode")
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://testcouncil.com",
            "https://testcouncil.com",
            "http://www.testcouncil.com",
            "https://www.testcouncil.com"
        ],
        description="Allowed CORS origins"
    )

    # Application Settings
    MAX_CONCURRENT_LLMS: int = Field(default=12, description="Max concurrent LLM calls")
    REQUEST_TIMEOUT: int = Field(default=599, description="Request timeout in seconds")

    class Config:
        env_file = ".env"
        case_sensitive = True


class Config:
    """Configuration class for the intelligent council system"""

    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()

        # ✅ Validate API key is set
        if not self.settings.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Please create a .env file with your API key. "
                "See .env.example for reference."
            )

        # API Keys
        self.OPENAI_API_KEY = self.settings.OPENAI_API_KEY
        self.OPENAI_BASE_URL = self.settings.OPENAI_BASE_URL

        # Server Settings
        self.HOST = self.settings.HOST
        self.PORT = self.settings.PORT
        self.DEBUG = self.settings.DEBUG
        self.CORS_ORIGINS = self.settings.CORS_ORIGINS

        # Application Settings
        self.MAX_CONCURRENT_LLMS = self.settings.MAX_CONCURRENT_LLMS
        self.REQUEST_TIMEOUT = self.settings.REQUEST_TIMEOUT

        # Synthesizer Model
        self.SYNTHESIS_MODEL = "gemini-2.0-flash"

        # LLM API Configuration
        self.LLM_API_KEY = self.OPENAI_API_KEY
        self.LLM_API_BASES = {
            "openai": self.OPENAI_BASE_URL,
            "anthropic": self.OPENAI_BASE_URL,
            "google": self.OPENAI_BASE_URL
        }

        # Model configurations
        self.LLM_MODELS = {
            "gemini-2.0-flash": {
                "type": "openai",
                "provider": "google",
                "model_name": "gemini-2.0-flash",
                "api_name": "gemini-2.0-flash",
                "base_url": self.OPENAI_BASE_URL,
                "api_key": self.OPENAI_API_KEY,
                "display_name": "Gemini 2.0 Flash",
                "icon": "✨",
                "color": "#4285f4"
            },
            "deepseek-chat": {
                "type": "openai",
                "provider": "openai",
                "model_name": "deepseek-chat",
                "api_name": "deepseek-chat",
                "base_url": self.OPENAI_BASE_URL,
                "api_key": self.OPENAI_API_KEY,
                "display_name": "Deepseek Chat",
                "icon": "🤖",
                "color": "#000000"
            },
            "qwen3-235b-a22b": {
                "type": "openai",
                "provider": "openai",
                "model_name": "qwen3-235b-a22b",
                "api_name": "qwen3-235b-a22b",
                "base_url": self.OPENAI_BASE_URL,
                "api_key": self.OPENAI_API_KEY,
                "display_name": "Qwen 3 235B",
                "icon": "🧠",
                "color": "#722ed1"
            }
        }

        # 🚀 ENHANCED Role-Based Test Generation Personas
        # ================================================
        # NEW STRATEGY: 6 highly specialized roles designed to:
        # 1. Maximize line/branch coverage
        # 2. Reduce duplication through focused mandates
        # 3. Increase assertion density with explicit quality metrics
        # 4. Generate diverse test categories

        self.ROLES = {
            # ========================================
            # ROLE 1: Line Coverage Hunter
            # ========================================
            "coverage_hunter": {
                "name": "Line Coverage Hunter",
                "philosophy": "Test every line of code",
                "focus_categories": ["positive", "edge_case"],
                "icon": "🎯",
                "color": "#13c2c2",
                "prompt_persona": """You write tests to execute EVERY LINE of the function.

**Task**: Create 3-4 tests that:
1. Call the function with different inputs
2. Make sure EVERY line runs at least once
3. Test both if/else branches

**Example**:
```python
def test_basic_case():
    \"\"\"Tests lines 1-5\"\"\"
    result = function(normal_input)
    assert result == expected
    
def test_edge_case():
    \"\"\"Tests lines 6-8 (error path)\"\"
    result = function(edge_input)
    assert result == expected_edge

Generate simple tests that cover all lines."""
            },

            # ========================================
            # ROLE 2: Assertion Booster
            # ========================================
            "assertion_booster": {
                "name": "Assertion Booster",
                "philosophy": "More checks = better tests",
                "focus_categories": ["positive", "boundary"],
                "icon": "✅",
                "color": "#52c41a",
                "prompt_persona": """You add LOTS of checks to tests.

**Task**: Create 3-4 tests with MANY assertions:
1. Check the return value
2. Check the type: `assert isinstance(result, int)`
3. Check the length: `assert len(result) > 0`
4. Check properties: `assert result > 0`

**Example**:
```python
def test_with_many_checks():
    result = function(input)
    assert result is not None  # Check 1
    assert isinstance(result, list)  # Check 2
    assert len(result) == 3  # Check 3
    assert all(x > 0 for x in result)  # Check 4
```

Add 3-4 assertions per test."""
            },

            # ========================================
            # ROLE 3: Error Finder
            # ========================================
            "error_finder": {
                "name": "Error Finder",
                "philosophy": "Break it with bad inputs",
                "focus_categories": ["negative", "edge_case"],
                "icon": "❌",
                "color": "#f5222d",
                "prompt_persona": """You test with BAD inputs to find errors.

**Task**: Create tests with wrong inputs:

**Bad Input Types**:
```python
def test_none_input():
    with pytest.raises(TypeError):
        function(None)

def test_empty_input():
    with pytest.raises(ValueError):
        function("")

def test_negative_number():
    with pytest.raises(ValueError):
        function(-1)

def test_huge_input():
    with pytest.raises(ValueError):
        function("A" * 10000)
```

Test with: None, empty, negative, too big."""
            },

            # ========================================
            # ROLE 4: Security Checker
            # ========================================
            "security_checker": {
                "name": "Security Checker",
                "philosophy": "Test dangerous inputs",
                "focus_categories": ["security", "negative"],
                "icon": "🔒",
                "color": "#fa8c16",
                "prompt_persona": """You test with DANGEROUS strings.

**Task**: Create 3-4 tests with risky inputs:

```python
def test_sql_injection():
    \"\"\"Test SQL injection blocked\"\"\"
    result = function("admin' OR '1'='1")
    assert "OR" not in result  # Injection blocked

def test_path_traversal():
    \"\"\"Test path traversal blocked\"\"\"
    result = function("../../etc/passwd")
    assert ".." not in result  # Traversal blocked

def test_large_input():
    \"\"\"Test oversized input handled\"\"\"
    result = function("A" * 100000)
    assert len(result) < 1000  # Truncated or rejected
```

Test: SQL injection, path traversal, huge strings."""
            },

            # ========================================
            # ROLE 5: Property Tester
            # ========================================
            "property_tester": {
                "name": "Property Tester",
                "philosophy": "Test rules that always work",
                "focus_categories": ["positive", "boundary"],
                "icon": "🧮",
                "color": "#722ed1",
                "prompt_persona": """You test RULES that must ALWAYS be true.

**Task**: Create 2-3 tests for these rules:

1. **Same input = same output**:
```python
def test_consistent_output():
    result1 = function(input)
    result2 = function(input)
    assert result1 == result2
```

2. **Output type is always correct**:
```python
def test_type_always_correct():
    for input in [test1, test2, test3]:
        result = function(input)
        assert isinstance(result, int)
```

3. **Output in valid range**:
```python
def test_output_in_range():
    result = function(input)
    assert 0 <= result <= 100
```

Test simple rules that NEVER break."""
            },

            # ========================================
            # ROLE 6: Real Usage Tester
            # ========================================
            "usage_tester": {
                "name": "Real Usage Tester",
                "philosophy": "Test like users actually use it",
                "focus_categories": ["positive", "integration"],
                "icon": "👤",
                "color": "#1890ff",
                "prompt_persona": """You test REAL usage scenarios.

**Task**: Create 2-3 tests showing normal usage:

```python
def test_typical_usage():
    \"\"\"How users normally call this\"\"\"
    result = function(typical_input)
    assert result is not None
    assert result == expected_normal

def test_multi_step_usage():
    \"\"\"Multiple calls in sequence\"\"\"
    step1 = function(input1)
    step2 = function(step1)
    assert step2 == expected_final
```

Test realistic scenarios users actually do."""
            }
        }

        # 🎯 STRATEGIC MODEL-ROLE ASSIGNMENTS
        # ====================================
        # Each model gets a BALANCED set of roles to maximize diversity

        self.MODEL_ROLE_ASSIGNMENTS = {
            "gemini-2.0-flash": [
                "coverage_hunter",
                "assertion_booster"
            ],
            "deepseek-chat": [
                "error_finder",
                "security_checker"
            ],
            "qwen3-235b-a22b": [
                "property_tester",
                "usage_tester"
            ]
        }

        # Test categories
        self.TEST_CATEGORIES = [
            "positive",    # Normal cases
            "negative",    # Error cases
            "boundary",    # Edge values
            "edge_case",   # Unusual cases
            "security",    # Security tests
            "integration"  # NEW: Integration tests
        ]

        # Clustering configuration
        self.CLUSTERING_METHODS = {
            "vector": {
                "name": "Advanced Vector-based DBSCAN",
                "description": "Uses AST feature vectors for semantic clustering",
                "eps": 0.3,
                "min_samples": 2
            },
            "hash": {
                "name": "Fast Structural Hashing",
                "description": "Uses structural hashes for quick deduplication"
            }
        }

    def get_models_info(self) -> List[Dict[str, Any]]:
        """Get formatted model information for API responses"""
        return [
            {
                "id": model_id,
                "name": config["display_name"],
                "icon": config["icon"],
                "color": config["color"],
                "roles": self.MODEL_ROLE_ASSIGNMENTS.get(model_id, [])
            }
            for model_id, config in self.LLM_MODELS.items()
        ]

    def get_roles_info(self) -> List[Dict[str, Any]]:
        """Get formatted role information for API responses"""
        return [
            {
                "id": role_id,
                "name": role_data["name"],
                "philosophy": role_data["philosophy"],
                "icon": role_data["icon"],
                "color": role_data["color"],
                "focus_categories": role_data["focus_categories"],
                # ✅ NEW: Expose metrics to frontend
                "coverage_target": role_data.get("coverage_target"),
                "min_assertions": role_data.get("min_assertions_per_test"),
                "min_tests": role_data.get("min_exception_tests") or
                             role_data.get("min_security_tests") or
                             role_data.get("min_property_tests") or
                             role_data.get("min_integration_tests")
            }
            for role_id, role_data in self.ROLES.items()
        ]

    def get_clustering_methods_info(self) -> List[Dict[str, Any]]:
        """Get formatted clustering method information"""
        return [
            {
                "id": method_id,
                "name": method_data["name"],
                "description": method_data["description"]
            }
            for method_id, method_data in self.CLUSTERING_METHODS.items()
        ]


# Global configuration instance
settings = Settings()
config = Config(settings)