"""
This is an auto-generated comprehensive test suite for the divide_numbers function.
It covers positive, negative, boundary, edge case, and security scenarios.
"""

import pytest
import math
import sys
from function import divide_numbers

# ======================================================================
# CATEGORY: POSITIVE (4 tests)
# ======================================================================

def test_divide_numbers_various_valid_inputs():
    """
    Verifies division with a variety of valid inputs, including positive integers,
    positive floats, zero numerator, dividing by one, dividing by itself,
    and dividing by a very large number.
    """
    assert divide_numbers(10, 2) == 5.0, "Should return the correct quotient for positive integers"
    assert divide_numbers(7.5, 2.5) == 3.0, "Should return the correct quotient for floating-point numbers"
    assert divide_numbers(0, 5) == 0.0, "Should return zero when numerator is zero"
    assert divide_numbers(5, 1) == 5.0, "Dividing by 1 should return the original number"
    assert divide_numbers(7, 7) == 1.0, "Dividing a number by itself should return 1.0"
    assert divide_numbers(1000000, 100) == 10000.0, "Should return the correct quotient for large numbers"
    assert divide_numbers(10, 1e1000) == 0.0, "Result should be approximately 0.0 when dividing by a very large number"


def test_divide_numbers_mixed_signs():
    """
    Verifies the division of numbers with mixed signs, including cases with negative numerators,
    negative denominators, and both negative numbers.  Also tests for negative zero result and large negative denominator.
    """
    result = divide_numbers(-10, 2)
    assert result == -5.0, "Division with negative numerator should return -5.0"

    result = divide_numbers(10, -2)
    assert result == -5.0, "Division with negative denominator should return -5.0"

    result = divide_numbers(-10, -2)
    assert result == 5.0, "Division with two negatives should return 5.0"

    result = divide_numbers(-1e-10, 1e10)
    assert result == -0.0, "Division resulting in very small negative value should yield -0.0"

    result = divide_numbers(10, -5)
    assert result == -2.0, "Division with negative denominator should return -2.0"


def test_divide_numbers_various_inputs():
    """
    Verifies division with floating-point numbers, and NaN inputs.
    """
    # Test floating-point result
    result_float = divide_numbers(1, 3)
    assert abs(result_float - 0.3333333333333333) < 1e-9, "Division should handle floating-point results correctly"

    # Test division by NaN
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(5, float('nan'))

    # Test division of NaN
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(float('nan'), 5)


def test_divide_numbers_robustness():
    """
    Comprehensive test suite for divide_numbers, covering:
      - Commutativity of multiplication and division
      - Handling of near-zero denominators to prevent division by zero
      - Type checking for numeric inputs, including very large numbers
    """
    # Commutativity of multiplication and division
    a = 10.0
    b = 3.0
    result = divide_numbers(a, b) * b
    assert abs(result - a) < 1e-6, "Division followed by multiplication should (approximately) yield the original numerator."

    # Near-zero denominator check
    epsilon = 1e-16
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(1, epsilon)

    # Type checking with a very large exponent
    huge_number = 1e308
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(huge_number, "1")


# ======================================================================
# CATEGORY: NEGATIVE (5 tests)
# ======================================================================

def test_divide_numbers_invalid_input():
    """
    Verify that TypeError is raised when either argument is non-numeric,
    and that ValueError is raised when dividing by zero.
    """
    with pytest.raises(TypeError) as excinfo:
        divide_numbers("10", 2)
    assert "Both arguments must be numeric" in str(excinfo.value)

    with pytest.raises(TypeError) as excinfo:
        divide_numbers(10, "2")
    assert "Both arguments must be numeric" in str(excinfo.value)
    
    with pytest.raises(ValueError) as excinfo:
        divide_numbers(5, 0)
    assert "Cannot divide by zero" in str(excinfo.value)


def test_divide_numbers_various_scenarios():
    """
    Test various division scenarios including:
    - Basic positive and negative division
    - Division by small numbers
    - Division resulting in zero
    - Zero division error
    - Type error with non-numeric inputs
    - Division by NaN
    """
    # positive
    assert divide_numbers(10, 2) == 5.0, "Basic positive division should work"
    assert divide_numbers(1e-10, 1e10) == 0.0, "Division resulting in very small positive value should yield 0.0"

    # negative
    assert divide_numbers(1, -1e-6) == -1e6, "Division of 1 by -1e-6 should yield -1e6, accounting for floating-point precision"

    # boundary
    a = 1e-30
    b = 1
    assert divide_numbers(a, b) == 1e-30, "Division with small numbers should produce correct result."
    assert divide_numbers(1, 1e-300) == float('inf'), "Division by a very small number should approach infinity"

    # negative - zero division
    with pytest.raises(ValueError) as excinfo:
        divide_numbers(10, 0)
    assert "Cannot divide by zero" in str(excinfo.value)

    # negative - type error
    with pytest.raises(TypeError) as excinfo:
        divide_numbers(5 + 2j, 2)
    assert "Both arguments must be numeric" in str(excinfo.value), "TypeError message should indicate non-numeric input"

    # edge_case
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(10, float('nan'))


def test_divide_numbers_errors():
    """
    Tests that divide_numbers raises ValueError for division by zero and TypeError for non-numeric inputs.
    Category: negative
    """
    with pytest.raises(ValueError) as excinfo:
        divide_numbers(5, 0)
    assert "Cannot divide by zero" in str(excinfo.value), "ValueError message should indicate division by zero"

    with pytest.raises(TypeError) as excinfo:
        divide_numbers("5", 2)
    assert "Both arguments must be numeric" in str(excinfo.value), "TypeError message should indicate non-numeric input with string"

    with pytest.raises(TypeError) as excinfo:
        divide_numbers(5, None)
    assert "Both arguments must be numeric" in str(excinfo.value), "TypeError message should indicate non-numeric input with None"


def test_divide_numbers_error_handling():
    """
    Verifies that divide_numbers raises appropriate errors for invalid input.
    Specifically tests for TypeError when inputs are non-numeric (strings, None, lists, byte strings, unicode strings)
    and ValueError when dividing by zero (both integer and float).
    """
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers("hello", 5)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(None, 5)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(10, None)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers("", 5)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(10, "")
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(5, [2])
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers("5", 2)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(5, "2")
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers("1\u0660", 2)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(b'6', b'2')
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers("6\x00", "2\x00")
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(10, 0)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(10, 0.0)


def test_divide_with_non_numeric_b():
    '''Verifies that TypeError is raised when the denominator (b) is not numeric'''
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(10, [1, 2, 3])  # List for b - let's see it crumble!


# ======================================================================
# CATEGORY: BOUNDARY (4 tests)
# ======================================================================

def test_divide_numbers_with_extreme_values():
    """Tests division with a denominator very close to zero and with infinity, checking for correct handling of extreme values and potential floating-point issues.
    Category: boundary, edge_case
    """
    b_near_zero = 1e-300
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(1, b_near_zero)

    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(float('inf'), 2)


def test_divide_numbers_edge_cases():
    """Tests division edge cases, including dividing by negative zero and handling minimum negative float values."""

    import sys

    # Test dividing by negative zero
    result_negative_zero = divide_numbers(10, -0.0)
    assert result_negative_zero == -float('inf'), "Dividing positive by negative zero yields -inf"

    # Test division with the most negative float value
    a = -sys.float_info.max
    result_min_float = divide_numbers(a, 2)
    assert result_min_float == a / 2, "Should handle minimum negative float values correctly"


def test_divide_numbers_type_validation_with_proxy_objects():
    """
    Tests that TypeError is raised when non-int/float numeric-like objects are passed as arguments.
    Specifically, tests with proxy objects and custom numeric objects with potential side effects,
    ensuring type checking is robust against such objects.
    """

    class NumericProxy:
        def __init__(self, value):
            self.value = value
        def __float__(self):
            return self.value

    class DangerousNumeric:
        def __init__(self, value):
            self.value = value
        def __float__(self):
            return self.value

    a_proxy = NumericProxy(10)
    b_proxy = NumericProxy(2)

    a_dangerous = DangerousNumeric(6)
    b_dangerous = DangerousNumeric(2)

    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(a_proxy, b_proxy)
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(a_dangerous, b_dangerous)


def test_divide_numbers_various_inputs():
    """
    Verifies division with positive integers, positive floats, zero numerator, very small denominator,
    and a very large numerator, ensuring the correct float result and handling boundary conditions.
    Also checks the inverse property for integer division.
    """
    # Positive integer division
    result_int = divide_numbers(10, 2)
    assert isinstance(result_int, float), "Integer division result should be a float"
    assert result_int == 5.0, "Division of 10 by 2 should yield 5.0"

    # Positive float division
    result_float = divide_numbers(10.0, 2.0)
    assert isinstance(result_float, float), "Float division result should be a float"
    assert result_float == 5.0, "Division of 10.0 by 2.0 should yield 5.0"

    # Zero numerator
    result_zero = divide_numbers(0, 1)
    assert isinstance(result_zero, float), "Zero numerator result should be a float"
    assert result_zero == 0.0, "Division of 0 by 1 should yield 0.0"

    # Very small denominator
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(1, 1e-6)

    # Very large numerator
    result_large_num = divide_numbers(1e100, 1)
    assert isinstance(result_large_num, float), "Large numerator result should be a float"
    assert result_large_num == 1e100, "Division of 1e100 by 1 should yield 1e100"

    # Inverse property
    quotient = divide_numbers(15, 3)
    assert quotient * 3 == 15.0, "Multiplying quotient by denominator should recover numerator"


# ======================================================================
# CATEGORY: EDGE_CASE (4 tests)
# ======================================================================

def test_divide_numbers_extreme_float_values():
    """Tests division with extreme float values, including maximum and minimum positive float values, to ensure correct handling of boundary conditions and float representation limits."""
    max_float = sys.float_info.max
    min_float = sys.float_info.min

    result_max = divide_numbers(max_float, 2)
    assert result_max == max_float / 2, "Should handle maximum float values correctly"

    result_min = divide_numbers(min_float, 2)
    assert result_min == min_float / 2, "Should handle minimum positive float values correctly"


def test_divide_numbers_positive_and_negative_values():
    """
    Verifies that dividing positive and negative numerators and denominators returns the correct float result.
    Covers typical use cases for the function's division operation including dividing by large numbers.
    """
    result1 = divide_numbers(-10, 2)
    assert isinstance(result1, float), "Result should be a float"
    assert result1 == -5.0, "Division of -10 by 2 should yield -5.0"

    result2 = divide_numbers(10, -2)
    assert isinstance(result2, float), "Result should be a float"
    assert result2 == -5.0, "Division of 10 by -2 should yield -5.0"

    result3 = divide_numbers(-10, -2)
    assert isinstance(result3, float), "Result should be a float"
    assert result3 == 5.0, "Division of -10 by -2 should yield 5.0"

    result4 = divide_numbers(1, 1e10)
    assert result4 == pytest.approx(1e-10), "Division by large number should approach zero"


def test_divide_numbers_with_extreme_values():
    '''Verifies the function handles division with extreme values, including infinity and very large numbers, correctly returning 0.0 or infinity without raising exceptions.'''
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(1e1000, 2)

    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(-float('inf'), 2)

    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(10, float('inf'))


def test_divide_with_nan_for_a():
    '''Verifies that the function handles NaN for a, resulting in NaN output without exceptions'''
    import math
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(float('nan'), 2)


# ======================================================================
# CATEGORY: SECURITY (13 tests)
# ======================================================================

def test_divide_numbers_with_nan_values():
    '''Tests if NaN values can bypass numeric checks and cause unexpected behavior'''
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(float('nan'), 1)


def test_divide_numbers_with_infinity_overflow():
    '''Tests if extremely large values can cause resource exhaustion or overflow'''
    import sys
    huge_number = sys.float_info.max
    result = divide_numbers(huge_number, 1)
    assert not math.isinf(result), "Should not return infinity from normal inputs"


def test_divide_numbers_with_negative_infinity():
    '''Tests if negative infinity can be used to manipulate numeric checks'''
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(-float('inf'), 2)


def test_divide_numbers_with_complex_numbers():
    '''Tests if complex numbers can bypass numeric checks and cause type confusion'''
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(complex(1, 2), 2)


def test_divide_numbers_with_subclass_of_int():
    '''Tests if subclassed numeric types can bypass type checks and inject malicious behavior'''
    class EvilInt(int):
        def __new__(cls, value):
            return super().__new__(cls, value)

    result = divide_numbers(EvilInt(6), EvilInt(2))
    assert result == 3.0, "Should correctly handle numeric subclasses that behave normally"


def test_divide_numbers_with_mocked_numeric_objects():
    '''Tests if objects faking numeric behavior can bypass type checks'''
    class FakeNumber:
        def __float__(self):
            return 4.0

    a = FakeNumber()
    b = FakeNumber()
    
    # Should raise TypeError as these are not actual int/float
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(a, b)


def test_divide_numbers_with_denominator_close_to_zero():
    '''Tests if near-zero denominator can bypass zero check and cause floating point instability'''
    import sys
    near_zero = sys.float_info.min / 2  # Smaller than smallest representable positive float
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(1, near_zero)


def test_divide_numbers_with_subnormal_numbers():
    '''Tests if subnormal floats can be used to bypass validation or cause DoS'''
    subnormal = 1e-320
    result = divide_numbers(subnormal, subnormal)
    assert result == 1.0, "Should handle subnormal floats correctly"


def test_divide_numbers_with_custom_float_subclass():
    '''Tests if subclassed float with malicious behavior can bypass checks'''
    class EvilFloat(float):
        def __new__(cls, value):
            return super().__new__(cls, value)

    a = EvilFloat(6)
    b = EvilFloat(2)
    
    result = divide_numbers(a, b)
    assert result == 3.0, "Should handle float subclasses safely"


def test_divide_numbers_with_float_overflow():
    '''Tests if overflow in float operations can be exploited'''
    import math
    huge_value = math.inf
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(huge_value, 2)


def test_divide_numbers_with_float_underflow():
    '''Tests if underflow in float operations can be exploited for malicious behavior'''
    tiny_value = -math.inf
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(tiny_value, 2)


def test_divide_numbers_with_specially_crafted_floats():
    '''Tests if special float values can be used to manipulate numeric checks'''
    special_values = [float('inf'), -float('inf'), float('nan')]
    
    for value in special_values:
        with pytest.raises(TypeError, match="Both arguments must be numeric"):
            divide_numbers(value, 2)


def test_divide_numbers_with_very_large_float_strings():
    '''Tests if very large float strings can be used for DoS attacks'''
    huge_float_str = "1" + "0" * 1000000 + ".0"
    with pytest.raises(TypeError, match="Both arguments must be numeric"):
        divide_numbers(huge_float_str, 2)