import pytest
from function import divide_numbers
import math

def test_divide_numbers_positive_integers():
    """Test normal division with positive integers."""
    # Category: positive
    result = divide_numbers(10, 2)
    assert result == 5.0, "Should return the correct quotient for positive integers"

def test_divide_numbers_positive_floats():
    """Test normal division with positive floats."""
    # Category: positive
    result = divide_numbers(7.5, 2.5)
    assert result == 3.0, "Should return the correct quotient for positive floats"

def test_divide_numbers_mixed_signs():
    """Test division with mixed positive and negative numbers."""
    # Category: positive
    result1 = divide_numbers(-10, 2)
    assert result1 == -5.0, "Should return the correct quotient for negative numerator"
    result2 = divide_numbers(10, -2)
    assert result2 == -5.0, "Should return the correct quotient for negative denominator"

def test_divide_numbers_fractional_result():
    """Test division that results in a fraction."""
    # Category: positive
    result = divide_numbers(1, 2)
    assert result == 0.5, "Should return the correct fractional quotient"

def test_divide_numbers_zero_numerator():
    """Test division with zero as the numerator."""
    # Category: edge_case
    result = divide_numbers(0, 5)
    assert result == 0.0, "Should return zero when the numerator is zero"

def test_divide_numbers_large_numbers():
    """Test division with very large numbers."""
    # Category: boundary
    result = divide_numbers(1e10, 1e5)
    assert result == 1e5, "Should handle large numbers correctly"

def test_divide_numbers_very_small_over_very_large_underflow():
    """Test handling of extreme float ratios which may underflow to 0.0."""
    # Category: edge_case
    tiny = 1e-308
    huge = 1e308
    result = divide_numbers(tiny, huge)
    assert result == 0.0, f"Expected {tiny} / {huge} to underflow to 0.0, got {result!r}"

def test_divide_numbers_with_infinity_and_nan():
    """Test behavior with special float values (inf and nan)."""
    # Category: edge_case
    result_inf = divide_numbers(123.0, float("inf"))
    assert result_inf == 0.0, f"Expected 123.0 / inf to be 0.0, got {result_inf!r}"

    result_nan = divide_numbers(1.0, float("nan"))
    assert math.isnan(result_nan), "Expected division by NaN to produce NaN"

def test_divide_numbers_divide_by_zero():
    """Test division by zero, expecting a ValueError."""
    # Category: negative
    with pytest.raises(ValueError) as excinfo:
        divide_numbers(10, 0)
    assert str(excinfo.value) == "Cannot divide by zero", "Should raise ValueError when dividing by zero"

def test_divide_numbers_non_numeric_inputs():
    """Test division with non-numeric inputs, expecting a TypeError."""
    # Category: negative
    with pytest.raises(TypeError) as excinfo:
        divide_numbers("a", 2)
    assert str(excinfo.value) == "Both arguments must be numeric", "Should raise TypeError when numerator is not numeric"

    with pytest.raises(TypeError) as excinfo:
        divide_numbers(10, "b")
    assert str(excinfo.value) == "Both arguments must be numeric", "Should raise TypeError when denominator is not numeric"

def test_divide_numbers_bool_handling():
    """Test boolean inputs (True/False)."""
    # Category: security
    result_true_num = divide_numbers(True, 2)
    assert result_true_num == 0.5, f"Expected True (1) / 2 to be 0.5, got {result_true_num!r}"

    with pytest.raises(ValueError) as excinfo:
        divide_numbers(1, False)
    assert str(excinfo.value) == "Cannot divide by zero", "Using False as denominator should raise ValueError because False == 0"