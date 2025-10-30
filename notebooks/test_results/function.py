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