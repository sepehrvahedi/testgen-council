"""
Final optimized test suite for example_function.

This suite covers positive, negative, boundary, and edge cases
to ensure comprehensive functionality and error handling.
"""

import pytest
import sys

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
    """Tests for normal positive scenarios."""

    def test_positive_integers(self):
        """Test normal addition with positive integers."""
        result = example_function(2, 3)
        assert result == 5, f"Expected 2 + 3 to equal 5, got {result}"
        assert isinstance(result, int), f"Expected result type int for integer inputs, got {type(result)}"

    def test_negative_integers(self):
        """Test addition with negative integers."""
        result = example_function(-5, -3)
        assert result == -8, "Should return the correct sum of negative integers"

    def test_mixed_positive_negative(self):
        """Test addition with mixed positive and negative integers."""
        result = example_function(5, -3)
        assert result == 2, "Should return the correct sum of mixed positive and negative integers"


# Boundary Tests
class TestBoundary:
    """Tests for boundary conditions."""

    def test_addition_with_zero(self):
        """Test addition with zero as one of the inputs."""
        result = example_function(0, 5)
        assert result == 5, "Should correctly handle addition with zero"

    def test_large_numbers(self):
        """Test addition with large numbers."""
        large_number = 10**12
        result = example_function(large_number, 1)
        assert result == large_number + 1, "Should correctly handle addition of very large integers"

    def test_max_int_value(self):
        """Test boundary condition with the maximum integer value."""
        max_int_value = sys.maxsize
        result = example_function(max_int_value, 0)
        assert result == max_int_value, "Should correctly handle addition with the maximum integer value without overflow (Python handles large ints)"


# Edge Case Tests
class TestEdgeCases:
    """Tests for edge case scenarios."""

    def test_large_integers_no_overflow(self):
        """Test extremely large integers — Python supports arbitrary precision so no overflow expected."""
        a = 10**100  # very large integer
        b = 10**100 + 1
        expected = a + b
        result = example_function(a, b)
        assert result == expected, "Summing very large integers should produce the mathematically correct result"
        assert isinstance(result, int), "Result of adding two ints should remain an int even if very large"


# Negative Tests
class TestNegative:
    """Tests for invalid input and error conditions."""

    def test_invalid_input_string(self):
        """Test addition with string inputs and expect a TypeError."""
        with pytest.raises(TypeError, match="unsupported operand type"):
            example_function("a", 1)  # Expect TypeError because string and int cannot be added

    def test_float_input(self):
        """Test with float input, which violates the function's expected int type."""
        result = example_function(1.5, 2)
        assert isinstance(result, float), "Should return a float when a float is passed, indicating invalid input handling"
        assert result != 3, "The result should not match integer addition due to type mismatch"

    def test_none_raises_typeerror(self):
        """Passing None is not supported; addition should raise a TypeError."""
        with pytest.raises(TypeError):
            _ = example_function(None, 1)

# Security Tests
class TestSecurity:
    """Tests for security related issues (e.g., exception propagation)."""

    def test_custom_add_raises_propagates_exception(self):
        """If a custom object's __add__ raises an exception, it should propagate."""
        class MaliciousAdd:
            def __init__(self, msg="boom"):
                self.msg = msg
            def __add__(self, other):
                raise RuntimeError(self.msg)

        with pytest.raises(RuntimeError) as excinfo:
            _ = example_function(MaliciousAdd("exploit"), 1)
        assert "exploit" in str(excinfo.value), "Exceptions raised in user-defined __add__ should propagate unchanged"