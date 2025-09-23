"""
Test suite for the divide_numbers function.

This suite covers positive and negative test cases,
boundary conditions, edge cases, and error handling.
"""

import pytest
import math
from decimal import Decimal

def divide_numbers(a, b):
    """
    Divide two numbers with error handling

    Args:
        a (float): Numerator
        b (float): Denominator

    Returns:
        float: Result of division

    Raises:
        ValueError: If denominator is zero
        TypeError: If inputs are not numeric
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numeric")

    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


# Positive test cases
class TestPositiveCases:
    """
    Test suite for positive test cases
    """
    def test_divide_numbers_positive_integers(self):
        """Test normal division with positive integers"""
        result = divide_numbers(10, 2)
        assert result == 5.0, "Should correctly divide positive integers"

    def test_divide_numbers_positive_floats(self):
        """Test normal division with positive floats"""
        result = divide_numbers(7.5, 2.5)
        assert result == 3.0, "Should correctly divide positive floats"

    def test_divide_numbers_negative_numerator(self):
        """Test division with a negative numerator"""
        result = divide_numbers(-10, 2)
        assert result == -5.0, "Should correctly divide with negative numerator"

    def test_divide_numbers_negative_denominator(self):
        """Test division with a negative denominator"""
        result = divide_numbers(10, -2)
        assert result == -5.0, "Should correctly divide with negative denominator"

    def test_divide_numbers_negative_both(self):
        """Test division with both arguments negative"""
        result = divide_numbers(-10, -2)
        assert result == 5.0, "Should correctly divide with both negative numbers"


# Boundary test cases
class TestBoundaryCases:
    """
    Test suite for boundary test cases
    """
    def test_divide_numbers_small_denominator(self):
        """Test division with a very small positive denominator"""
        result = divide_numbers(1, 1e-10)
        assert result == 1e10, "Should handle division by a very small number"

    def test_special_float_values_nan_and_inf(self):
        """Verify behavior with NaN and Infinity inputs"""
        result_nan = divide_numbers(1.0, float("nan"))
        assert math.isnan(result_nan), "Expected result to be NaN when denominator is NaN"

        result_inf = divide_numbers(float("inf"), 2.0)
        assert math.isinf(result_inf) and result_inf > 0, "Expected positive infinity when numerator is +inf"

        result_neg_inf = divide_numbers(float("-inf"), 2.0)
        assert math.isinf(result_neg_inf) and result_neg_inf < 0, "Expected negative infinity when numerator is -inf"


# Edge case test cases
class TestEdgeCases:
    """
    Test suite for edge cases
    """
    def test_divide_numbers_zero_numerator(self):
        """Test division with zero numerator"""
        result = divide_numbers(0, 5)
        assert result == 0.0, "Should correctly divide zero by a number"

    def test_divide_numbers_denominator_one(self):
        """Test division with denominator equal to one"""
        result = divide_numbers(7, 1)
        assert result == 7.0, "Should correctly return the numerator when denominator is one"

    def test_bool_is_subclass_of_int(self):
        """Verify behavior when using boolean values (True and False)"""
        result_true = divide_numbers(True, 2)
        assert result_true == 0.5, "Expected True to be treated as 1, so True/2 == 0.5"

        result_false = divide_numbers(False, 3)
        assert result_false == 0.0, "Expected False to be treated as 0, so False/3 == 0.0"

        with pytest.raises(ValueError) as exc:
            divide_numbers(1, False)
        assert str(exc.value) == "Cannot divide by zero", "Expected ValueError when denominator is False (zero)"


# Negative test cases
class TestNegativeCases:
    """
    Test suite for negative test cases (error handling)
    """
    def test_divide_numbers_zero_division_error(self):
        """Test when the denominator is zero"""
        with pytest.raises(ValueError) as excinfo:
            divide_numbers(10, 0)
        assert "Cannot divide by zero" in str(excinfo.value)

    def test_divide_numbers_type_error(self):
        """Test when non-numeric arguments are passed"""
        with pytest.raises(TypeError) as excinfo:
            divide_numbers("10", 2)
        assert "Both arguments must be numeric" in str(excinfo.value)

    def test_non_numeric_types_raise_type_error(self):
        """Passing non-numeric types should raise TypeError"""
        with pytest.raises(TypeError) as exc:
            divide_numbers(10, "2")
        assert str(exc.value) == "Both arguments must be numeric", "Expected TypeError when denominator is a string"

    def test_decimal_instances_not_accepted_type_error(self):
        '''Decimal instances should not be automatically accepted (function only allows int/float)'''
        with pytest.raises(TypeError) as exc:
            divide_numbers(Decimal("3.0"), 1)
        assert str(exc.value) == "Both arguments must be numeric", "Expected TypeError when using Decimal for numerator"

    def test_object_with_float_method_not_autocoerced(self):
        '''Ensure objects implementing __float__ are not silently accepted; explicit int/float required'''
        class CustomNumber:
            def __float__(self):
                return 3.0

        with pytest.raises(TypeError) as exc:
            divide_numbers(CustomNumber(), 1)
        assert str(exc.value) == "Both arguments must be numeric", "Expected TypeError for objects that are not int/float even if they implement __float__"