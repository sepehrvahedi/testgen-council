```python
"""
Final optimized test suite for example_function.

This suite combines the best tests from multiple AI models, removing duplicates
and ensuring comprehensive coverage of positive, negative, boundary, and edge
cases.
"""

import pytest
from typing import Any

# Function under test (assumed to be in the same directory or accessible via PYTHONPATH)
def example_function(x, y):
    """
    Add two numbers together
    
    Args:
        x (int): First number
        y (int): Second number
        
    Returns:
        int: Sum of x and y
    """
    return x + y


# Positive Tests
class TestPositive:
    """Tests for normal, positive scenarios."""

    def test_positive_integers(self):
        """Test normal addition with two positive integers."""
        result = example_function(5, 3)
        assert result == 8, "Should return 8 for 5 + 3"

    def test_addition_with_zero(self):
        """Test addition with zero."""
        assert example_function(7, 0) == 7, "Should return 7 for 7 + 0"
        assert example_function(0, 123) == 123, "0 + 123 should be 123"
        assert example_function(456, 0) == 456, "456 + 0 should be 456"

    def test_negative_integers(self):
        """Test addition with two negative integers."""
        result = example_function(-2, -5)
        assert result == -7, "Should return -7 for -2 + -5"

    def test_mixed_positive_negative(self):
        """Test addition with one positive and one negative integer."""
        result = example_function(10, -3)
        assert result == 7, "Should return 7 for 10 + -3"

    def test_positive_floats(self):
        """Test functionality with float inputs."""
        result = example_function(1.5, 2.3)
        assert result == pytest.approx(3.8), f"Adding 1.5 and 2.3 should be approximately 3.8, got {result}"


# Boundary Tests
class TestBoundary:
    """Tests for boundary conditions with large numbers and edge cases."""

    def test_large_integers(self):
        """Test addition with very large integers."""
        x = 2**31 - 1
        y = 1
        result = example_function(x, y)
        assert result == 2147483648, f"Should return correct sum for large numbers: expected 2147483648, got {result}"

    def test_negative_large_integers(self):
        """Test addition with very large negative integers."""
        x = -(2**31)
        y = -1
        result = example_function(x, y)
        assert result == -2147483649, f"Should return correct sum for large numbers: expected -2147483649, got {result}"

    def test_very_large_integers(self):
        """Test boundary with very large integers to ensure arbitrary-precision addition works"""
        a = 10**100
        b = 10**100
        expected = 2 * 10**100
        result = example_function(a, b)
        assert result == expected, f"Adding two very large integers should yield {expected}, got {result}"


# Edge Case Tests
class TestEdgeCases:
    """Tests for unusual or unexpected inputs."""

    def test_max_min_int(self):
        """Test addition with max and min int."""
        max_int = 2**31 - 1
        min_int = -(2**31)
        result = example_function(max_int, min_int)
        assert result == -1, f"Should return correct sum for max and min integers"

    def test_boolean_operands(self):
        """Test booleans (subclass of int) to verify behavior is consistent with integers."""
        # True == 1, False == 0
        result = example_function(True, False)
        assert result == 1, f"True + False should be 1, got {result}"
        result2 = example_function(True, True)
        assert result2 == 2, f"True + True should be 2, got {result2}"

    def test_list_concatenation(self):
        """Test that the function uses + operator semantics for lists and does not mutate inputs."""
        a = [1, 2]
        b = [3, 4]
        a_copy = a.copy()
        b_copy = b.copy()
        result = example_function(a, b)
        assert result == [1, 2, 3, 4], f"List concatenation expected [1,2,3,4], got {result}"
        # Ensure original inputs were not mutated (x+y returns a new list)
        assert a == a_copy and b == b_copy, "example_function should not mutate input lists"


# Negative Tests
class TestNegative:
    """Tests to verify error handling and type checking."""

    def test_type_error_on_incompatible_types(self):
        """Test that mixing incompatible operand types raises a TypeError (e.g., str + int)."""
        with pytest.raises(TypeError):
            _ = example_function("a", 1)  # str + int is not supported and should raise TypeError

    def test_none_input(self):
        '''Test with None as input, expecting a TypeError'''
        with pytest.raises(TypeError, match="unsupported operand type"):
            example_function(None, 1)  # Expect TypeError because None cannot be added to an integer

    def test_propagates_operand_exceptions(self):
        """Test that exceptions raised inside operand __add__ are propagated."""
        class BadAdd:
            def __add__(self, other: Any) -> Any:
                raise ValueError("custom add error")

        bad = BadAdd()
        with pytest.raises(ValueError) as excinfo:
            _ = example_function(bad, 1)
        assert "custom add error" in str(excinfo.value), "Exceptions raised by operand __add__ should propagate"
```