# Calculator module with bugs

def add(a, b):
    # Bug: doesn't handle None values
    return a + b

def subtract(a, b):
    # Bug: wrong operation
    return a + b

def multiply(a, b):
    # Bug: missing return statement
    result = a * b

def divide(a, b):
    # Bug: no zero division handling
    return a / b

def power(base, exp):
    # Bug: doesn't handle negative exponents properly
    result = 1
    for i in range(exp):
        result = result * base
    return result
