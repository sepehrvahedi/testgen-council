import pytest
from function import example_function
import sys

def test_example_function_positive_addition():
    '''Test normal addition of two positive integers'''
    # Category: positive
    result = example_function(3, 5)
    assert result == 8, "Should correctly add two positive integers"

def test_example_function_negative_numbers():
    '''Test addition of two negative integers'''
    # Category: positive
    result = example_function(-4, -6)
    assert result == -10, "Should correctly add two negative integers"

def test_example_function_mixed_numbers():
    '''Test addition of a positive and a negative integer'''
    # Category: positive
    result = example_function(10, -3)
    assert result == 7, "Should correctly add a positive and a negative integer"

def test_example_function_addition_with_zero():
    '''Test addition involving zero'''
    # Category: boundary
    result = example_function(5, 0)
    assert result == 5, "Should correctly handle addition with zero"

def test_example_function_large_integers():
    '''Test addition of very large integers'''
    # Category: edge_case
    big1 = 10**50
    big2 = 10**50
    expected = big1 + big2
    result = example_function(big1, big2)
    assert result == expected, f"Sum of two very large ints should be {expected}, got {result}"

def test_example_function_smallest_integers():
    '''Test addition of the smallest possible integers'''
    # Category: edge_case
    result = example_function(-sys.maxsize, -1)  # sys.maxsize is the largest, so -sys.maxsize is the smallest on most systems
    expected = -sys.maxsize - 1
    assert result == expected, f"Should correctly add very small integers, expected {expected}"

def test_example_function_non_integer_string():
    '''Test error handling with non-integer string inputs'''
    # Category: negative
    with pytest.raises(TypeError) as exc_info:
        example_function("a", 5)
    assert "unsupported operand type(s) for +: 'str' and 'int'" in str(exc_info.value), "Should raise TypeError for string input"

def test_example_function_non_integer_float():
    '''Test error handling with float inputs'''
    # Category: negative
    with pytest.raises(TypeError) as exc_info:
        example_function(3.5, 4)
    assert "unsupported operand type(s) for +: 'float' and 'int'" in str(exc_info.value), "Should raise TypeError for float input"

def test_example_function_none_raises_typeerror():
    """Negative case: None cannot be added to an int; TypeError should be raised"""
    # Category: negative
    with pytest.raises(TypeError):
        example_function(None, 1)