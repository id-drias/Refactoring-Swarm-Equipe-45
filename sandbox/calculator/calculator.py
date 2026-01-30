def add(a, b):
    if a is None or b is None:
        raise TypeError("Both inputs must be numbers")
    return a + b

def subtract(a, b):
    if a is None or b is None:
        raise TypeError("Both inputs must be numbers")
    return a - b

def multiply(a, b):
    if a is None or b is None:
        raise TypeError("Both inputs must be numbers")
    return a * b

def divide(a, b):
    if a is None or b is None:
        raise TypeError("Both inputs must be numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base, exp):
    if base is None or exp is None:
        raise TypeError("Both inputs must be numbers")
    if exp < 0:
        return 1 / power(base, -exp)
    result = 1
    for _ in range(exp):
        result = result * base
    return result