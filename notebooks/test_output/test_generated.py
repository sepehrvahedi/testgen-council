import pytest
from function import divide_numbers
import math

# Positive Tests
def test_divide_numbers_valid_division():
    """Verify normal division works with integers."""
    # Category: positive
    result = divide_numbers(10, 2)
    assert result == 5.0, "Normal division should work correctly"

def test_divide_numbers_float_division():
    """Verify dividing floats."""
    # Category: positive
    result = divide_numbers(5.5, 2.5)
    assert result == 2.2, "Float division should work correctly"

def test_divide_numbers_numerator_zero():
    """Verify dividing zero by a number."""
    # Category: positive
    result = divide_numbers(0, 5)
    assert result == 0.0, "Dividing zero should return zero"

def test_divide_numbers_negative_numbers():
    """Verify dividing negative numbers."""
    # Category: positive
    result = divide_numbers(-10, -2)
    assert result == 5.0, "Negative division failed"

def test_divide_numbers_mixed_negative_positive():
    """Verify dividing negative by positive and vice versa."""
    # Category: positive
    result = divide_numbers(-10, 2)
    assert result == -5.0, "Mixed division failed"
    result = divide_numbers(10, -2)
    assert result == -5.0, "Mixed division failed"

def test_divide_numbers_inverse_property():
    """Verify that dividing a number by itself returns 1.0."""
    # Category: positive
    result = divide_numbers(5, 5)
    assert result == 1.0, "Division identity property failed: a / a should equal 1.0"

def test_divide_numbers_commutativity_with_reciprocal():
    """Verify that dividing by b is equivalent to multiplying by reciprocal of b."""
    # Category: positive
    b = 4
    a = 10
    result1 = divide_numbers(a, b)
    result2 = a * (1.0 / b)
    assert abs(result1 - result2) < 1e-9, "Commutativity with reciprocal failed"

# Negative Tests (Error Handling)
def test_divide_numbers_denominator_zero():
    """Verify that dividing by zero raises a ValueError."""
    # Category: negative
    with pytest.raises(ValueError) as excinfo:
        divide_numbers(5, 0)
    assert "Cannot divide by zero" in str(excinfo.value)

def test_divide_numbers_invalid_type_string():
    """Verify that passing a string raises a TypeError."""
    # Category: negative
    with pytest.raises(TypeError) as excinfo:
        divide_numbers(5, "a")
    assert "Both arguments must be numeric" in str(excinfo.value)

def test_divide_numbers_invalid_type_list():
    """Verify that passing a list raises a TypeError."""
    # Category: negative
    with pytest.raises(TypeError) as excinfo:
        divide_numbers(5, [1,2,3])
    assert "Both arguments must be numeric" in str(excinfo.value)

def test_divide_numbers_invalid_type_none():
    """Verify that passing None raises a TypeError."""
    # Category: negative
    with pytest.raises(TypeError) as excinfo:
        divide_numbers(5, None)
    assert "Both arguments must be numeric" in str(excinfo.value)

def test_divide_numbers_non_numeric_a():
    """Verify TypeError is raised when numerator is non-numeric."""
    # Category: negative
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers("chaos_in_numbers", 5)

def test_divide_numbers_non_numeric_b():
    """Verify TypeError is raised when denominator is non-numeric."""
    # Category: negative
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(10, "divide_and_conquer")

# Boundary Tests
def test_divide_numbers_large_numbers():
    """Verify dividing very large numbers."""
    # Category: boundary
    a = 1e20
    b = 1e10
    result = divide_numbers(a, b)
    assert result == 1e10, "Large number division failed"

def test_divide_numbers_small_numbers():
    """Verify division with small numbers (close to zero, but not zero)."""
    # Category: boundary
    a = 1
    b = 1e-10
    result = divide_numbers(a, b)
    assert result == a / b, "Division with very small numbers should return the correct result"

def test_divide_numbers_large_denominator():
    """Verify dividing by a very large denominator."""
    # Category: boundary
    result = divide_numbers(1, 1e308)  # 1 divided by a very large number
    assert result == 1e-308 or result == 0.0, "Expected 1 divided by 1e308 to be approximately 1e-308 or underflow to 0.0 due to float limits"

# Edge Case Tests
def test_divide_numbers_very_small_numbers():
    """Verify dividing very small numbers."""
    # Category: edge_case
    a = 1e-10
    b = 1e-5
    result = divide_numbers(a, b)
    assert math.isclose(result, 1e-05), "Very small number division failed"

def test_divide_numbers_float_representation_issue():
    """Verify handling of potential float representation issues."""
    # Category: edge_case
    a = 0.1 + 0.2
    b = 0.3
    result = divide_numbers(a, b)
    assert math.isclose(result, 1.0), "Float representation issue"

def test_divide_numbers_b_is_almost_zero_but_not_zero():
    """Verify that dividing by a number very close to zero does not raise ValueError, but leads to very large result."""
    # Category: edge_case
    b = 1e-300
    result = divide_numbers(1, b)
    assert result > 1e200

def test_divide_numbers_division_by_one():
    """Verify that dividing by one returns the original number."""
    # Category: edge_case
    a = 42
    result = divide_numbers(a, 1)
    assert result == a, "Dividing by one should return the original number (identity property)"

def test_divide_numbers_with_infinity():
    """Verify division behavior with infinite values."""
    # Category: edge_case
    result1 = divide_numbers(float('inf'), 2)
    result2 = divide_numbers(5, float('inf'))
    
    assert result1 == float('inf'), "inf / finite should be inf"
    assert result2 == 0.0, "finite / inf should be 0"

def test_divide_numbers_with_negative_zero():
    """Verify behavior with negative zero (float -0.0)."""
    # Category: edge_case
    result1 = divide_numbers(5, -0.0)
    result2 = divide_numbers(-5, -0.0)
    
    assert result1 == float('-inf'), "5 / -0.0 should be -inf"
    assert result2 == float('inf'), "-5 / -0.0 should be inf"

def test_divide_numbers_nan_numerator():
    """Verify that the function processes NaN as a numerator."""
    # Category: edge_case
    result = divide_numbers(math.nan, 2)
    assert math.isnan(result), "Expected NaN result"

# Security Tests
def test_divide_numbers_with_nan():
    """Test division with NaN values to check propagation."""
    # Category: security
    nan_value = float('nan')
    result = divide_numbers(nan_value, 1)
    assert math.isnan(result), "Division involving NaN should propagate NaN"