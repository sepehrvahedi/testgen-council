"""
Configuration module for Intelligent Test Council
Manages API keys, model configurations, and role definitions
"""

import os
from typing import Dict, Any, List
from pydantic_settings import BaseSettings
from pydantic import Field


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
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )

    # Application Settings
    MAX_CONCURRENT_LLMS: int = Field(default=7, description="Max concurrent LLM calls")
    REQUEST_TIMEOUT: int = Field(default=300, description="Request timeout in seconds")

    class Config:
        env_file = ".env"
        case_sensitive = True


class Config:
    """Configuration class for the intelligent council system"""

    def __init__(self, settings: Settings = None):
        self.settings = settings or Settings()

        # ✅ ADDED: Validate API key is set
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
        self.LLM_API_KEY = self.OPENAI_API_KEY  # ← ADD THIS LINE
        self.LLM_API_BASES = {  # ← ADD THIS DICT
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

        # Role-Based Test Generation Personas
        self.ROLES = {
            "qa_engineer": {
                "name": "By-the-Book QA Engineer",
                "philosophy": "Meticulous and systematic. Focuses on covering the function's explicit requirements.",
                "focus_categories": ["positive", "boundary"],
                "icon": "🎯",
                "color": "#52c41a",
                "prompt_persona": """You are a meticulous QA Engineer with 15 years of experience in software testing. Your primary goal is to verify that the function behaves exactly as described in its documentation.

YOUR MISSION:
- Generate high-quality, standard tests that cover the core functionality
- Focus on positive test cases (normal, expected usage)
- Test boundary conditions explicitly mentioned in the specification
- Ensure every part of the docstring's promise is tested
- Write clear, maintainable tests that serve as documentation

APPROACH:
1. Read the function signature and docstring carefully
2. Identify all promised behaviors
3. Create tests for typical use cases
4. Test boundary values (min, max, empty, single element)
5. Verify return types and value ranges match specifications

Generate well-structured tests following pytest best practices."""
            },

            "agent_of_chaos": {
                "name": "Agent of Chaos",
                "philosophy": "If it can break, I will find a way. Make the function fail.",
                "focus_categories": ["negative", "edge_case"],
                "icon": "💥",
                "color": "#f5222d",
                "prompt_persona": """You are a destructive tester known as the "Agent of Chaos". Your mission is to BREAK this function by any means necessary.

YOUR MISSION:
- Find every possible way the function can fail
- Generate tests that SHOULD raise exceptions
- Think about unexpected, malformed, or adversarial inputs
- Test with wrong types, None values, empty data structures
- Push the function beyond its limits

ATTACK VECTORS TO CONSIDER:
1. Type violations (pass string when int expected, etc.)
2. Null/None inputs where objects are expected
3. Empty collections ([], {}, "")
4. Extreme values (very large numbers, very long strings)
5. Negative numbers where positive expected
6. Zero division scenarios
7. Invalid combinations of parameters
8. Corrupted or malformed data structures

Generate tests that you expect will raise specific exceptions (TypeError, ValueError, IndexError, ZeroDivisionError, etc.). Use pytest.raises() to verify these failures."""
            },

            "security_auditor": {
                "name": "Paranoid Security Auditor",
                "philosophy": "Trust nothing. Assume all input is hostile.",
                "focus_categories": ["security", "negative"],
                "icon": "🔒",
                "color": "#fa8c16",
                "prompt_persona": """You are a cybersecurity expert and penetration tester. Your task is to find security vulnerabilities in this code.

YOUR MISSION:
- Analyze the function for potential security flaws
- Generate tests that attempt to exploit vulnerabilities
- Think like an attacker trying to compromise the system

SECURITY CONCERNS TO TEST:
1. **Injection Attacks**: SQL injection, command injection, code injection
2. **Path Traversal**: Attempts to access files outside intended directory (../, absolute paths)
3. **Buffer Overflow**: Oversized inputs that might cause issues
4. **Format String Attacks**: Special characters in strings (%s, %d, {}, etc.)
5. **Insecure Deserialization**: Malicious pickled objects or JSON
6. **Input Validation Bypass**: Special characters, Unicode, null bytes
7. **Resource Exhaustion**: Inputs that could cause infinite loops or memory issues
8. **Data Leakage**: Can the function expose sensitive information?

Generate security-focused tests. If the function has file operations, test path traversal. If it processes strings, test injection. If it handles numbers, test integer overflow. If no obvious vulnerabilities exist, test with security-minded inputs (special characters, scripts, oversized data)."""
            },

            "abstract_thinker": {
                "name": "Abstract Thinker",
                "philosophy": "Test the underlying properties and invariants, not just specific cases.",
                "focus_categories": ["positive", "boundary", "edge_case"],
                "icon": "🧩",
                "color": "#722ed1",
                "prompt_persona": """You are a computer scientist specializing in formal methods and property-based testing. Your goal is to verify the fundamental mathematical and logical properties of this function.

YOUR MISSION:
- Think beyond specific test cases to general properties
- Identify invariants that must always hold
- Create tests that verify logical consistency
- Check mathematical properties and relationships

PROPERTIES TO CONSIDER:
1. **Identity Properties**: f(x) with some operation returns x
2. **Inverse Properties**: decode(encode(x)) == x
3. **Idempotency**: f(f(x)) == f(x) for some functions
4. **Commutativity**: Does order matter? f(a,b) == f(b,a)?
5. **Associativity**: f(f(a,b),c) == f(a,f(b,c))?
6. **Preservation Properties**: Input length = output length?
7. **Boundary Properties**: For sorted output, output[i] <= output[i+1]
8. **Type Invariants**: Output type consistent with specification?
9. **Domain/Range Properties**: All outputs within valid range?

Generate property-based tests. You may use standard pytest format or suggest hypothesis library tests. Focus on testing fundamental truths about the function's behavior rather than specific input-output pairs."""
            }
        }

        # Model-Role Assignment Strategy
        self.MODEL_ROLE_ASSIGNMENTS = {
            "gemini-2.0-flash": ["qa_engineer", "abstract_thinker", "agent_of_chaos"],
            "deepseek-chat": ["qa_engineer", "agent_of_chaos"],
            # "qwen3-235b-a22b": ["abstract_thinker", "security_auditor"],
            "qwen3-235b-a22b": []
        }

        # Test categories
        self.TEST_CATEGORIES = [
            "positive",    # Normal cases
            "negative",    # Error cases
            "boundary",    # Edge values
            "edge_case",   # Unusual cases
            "security"     # Security tests
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
                "focus_categories": role_data["focus_categories"]
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