```python
"""
Test suite for the divide_numbers function.

This file contains pytest tests to verify the functionality of the
divide_numbers function, including positive and negative cases,
boundary conditions, and error handling.
"""

import pytest
import math
from your_module import divide_numbers  # Replace your_module

# Positive test cases
def test_divide_positive_integers():
    """Test division with positive integers."""
    result = divide_numbers(10, 2)
    assert result == 5.0, "Should return correct quotient for positive integers"


def test_divide_positive_floats():
    """Test division with positive floats."""
    result = divide_numbers(7.5, 2.5)
    assert math.isclose(result, 3.0), "Should return correct quotient for positive floats"


def test_divide_negative_numbers():
    """Test division with negative numbers."""
    result = divide_numbers(-10, -2)
    assert result == 5.0, "Should handle both negative numbers correctly"


def test_divide_negative_numerator():
    """Test division with a negative numerator."""
    result = divide_numbers(-10, 2)
    assert result == -5.0, "Should handle negative numerator correctly"


def test_divide_negative_denominator():
    """Test division with a negative denominator."""
    result = divide_numbers(10, -2)
    assert result == -5.0, "Should handle negative denominator correctly"


# Boundary test cases
def test_divide_zero_numerator():
    """Test division with a zero numerator."""
    result = divide_numbers(0, 5)
    assert result == 0.0, "Should return 0 when numerator is 0"


def test_divide_by_one():
    """Test division by exactly one."""
    result = divide_numbers(7, 1)
    assert result == 7.0, "Should correctly divide 7 by 1 and return 7.0"


# Negative test cases (error handling)
def test_divide_by_zero_raises_value_error():
    """Test division by zero, expecting a ValueError."""
    with pytest.raises(ValueError) as excinfo:
        divide_numbers(10, 0)
    assert "Cannot divide by zero" in str(excinfo.value), "Should raise ValueError for division by zero"


@pytest.mark.parametrize("a,b", [
    ("10", 2),     # string numerator
    (10, "2"),     # string denominator
    (None, 1),     # None numerator
    (1, None),     # None denominator
    ([1,2], 2),    # list numerator
    (1, {"x":1}),  # dict denominator
])
def test_divide_non_numeric_types_raise_type_error(a, b):
    """Test that non-numeric inputs raise TypeError with expected message."""
    with pytest.raises(TypeError) as excinfo:
        divide_numbers(a, b)
    assert "Both arguments must be numeric" in str(excinfo.value), (
        f"Expected TypeError message 'Both arguments must be numeric' for inputs {a!r}, {b!r}; "
        f"got {str(excinfo.value)!r}"
    )


# Edge cases
def test_divide_large_numbers():
    """Test division with large numbers."""
    result = divide_numbers(1e10, 2)
    assert result == 5e9, "Should handle large numbers correctly"


def test_divide_booleans():
    """Test boolean inputs are treated as numeric (True -> 1, False -> 0)."""
    # True should behave like 1
    result_true = divide_numbers(True, 2)
    assert result_true == 0.5, "Expected True / 2 to equal 0.5 (True treated as 1)"

    # False as numerator should produce 0.0 (0 / 2)
    result_false = divide_numbers(False, 3)
    assert result_false == 0.0, "Expected False / 3 to equal 0.0 (False treated as 0)"


def test_divide_nan_and_infinity():
    """Test handling of NaN and infinity inputs."""
    nan_value = float("nan")
    inf_value = float("inf")

    # NaN propagated through division: result should be NaN
    result_nan = divide_numbers(nan_value, 1.0)
    assert math.isnan(result_nan), "Expected division of NaN to produce NaN"

    # Division by infinity should yield 0.0 (or -0.0 depending on sign)
    result_div_inf = divide_numbers(1.0, inf_value)
    assert math.isclose(result_div_inf, 0.0, rel_tol=0.0, abs_tol=1e-300), "Expected 1.0 / inf to be 0.0 (or nearly 0)"


def test_divide_extremely_large_values():
    """Test behavior with extremely large values possibly producing infinity."""
    large = 1e308
    small = 1e-308

    # large / small may overflow to infinity in IEEE-754 double precision
    result = divide_numbers(large, small)
    assert isinstance(result, float), "Expected result to be a float for large division"
    if math.isinf(result):
        assert result > 0, f"Expected positive infinity for {large}/{small}, got {result!r}"
    else:
        assert result > 1e300, f"Expected a very large number for {large}/{small}, got {result!r}"
```