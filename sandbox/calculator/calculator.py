def _validate_numeric_inputs(a, b):
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numbers")

def add(a, b):
    _validate_numeric_inputs(a, b)
    return a + b

def subtract(a, b):
    _validate_numeric_inputs(a, b)
    return a - b

def multiply(a, b):
    _validate_numeric_inputs(a, b)
    return a * b

def divide(a, b):
    _validate_numeric_inputs(a, b)
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base, exp):
    _validate_numeric_inputs(base, exp)
    return base ** exp