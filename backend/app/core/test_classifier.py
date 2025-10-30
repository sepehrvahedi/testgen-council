"""
Test classification module for categorizing generated tests
"""

from typing import Dict, List
from loguru import logger


class TestClassifier:
    """Classifies test cases into categories based on their content and intent"""

    # Keywords for each category (UPDATED to match config)
    CATEGORY_KEYWORDS = {
        "positive": [
            "basic", "normal", "valid", "typical", "standard", "happy path",
            "success", "correct", "expected"
        ],
        "negative": [
            "invalid", "error", "exception", "raises", "fail", "wrong",
            "bad", "incorrect", "malformed", "TypeError", "ValueError"
        ],
        "boundary": [
            "edge", "boundary", "limit", "max", "min", "empty", "zero",
            "extreme", "corner", "first", "last"
        ],
        "edge_case": [  # ← CHANGED from "edge" to "edge_case"
            "edge case", "unusual", "rare", "special", "corner case",
            "unexpected", "pathological", "degenerate"
        ],
        "security": [
            "security", "injection", "exploit", "malicious", "attack",
            "vulnerability", "sanitize", "escape", "sql", "xss", "path traversal"
        ],
        "performance": [
            "performance", "speed", "efficiency", "large", "scale",
            "benchmark", "timeout", "memory", "optimize"
        ]
    }

    def classify_tests(self, tests: List[str]) -> Dict[str, str]:
        """
        Classify tests into categories

        Args:
            tests: List of test function code strings

        Returns:
            Dictionary mapping test index to category
        """
        classifications = {}

        for i, test in enumerate(tests):
            # Lowercase for case-insensitive matching
            test_lower = test.lower()

            # Score each category
            category_scores = {}
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                score = sum(1 for keyword in keywords if keyword in test_lower)
                category_scores[category] = score

            # Get category with highest score
            if max(category_scores.values()) > 0:
                best_category = max(category_scores.items(), key=lambda x: x[1])[0]
            else:
                # Default to positive if no keywords match
                best_category = "positive"

            classifications[str(i)] = best_category

        logger.info(f"Classified {len(tests)} tests into categories")
        return classifications

    def get_category_distribution(self, classifications: Dict[str, str]) -> Dict[str, int]:
        """
        Get count of tests per category

        Args:
            classifications: Test classifications

        Returns:
            Dictionary with category counts
        """
        distribution = {}
        for category in classifications.values():
            distribution[category] = distribution.get(category, 0) + 1

        return distribution
