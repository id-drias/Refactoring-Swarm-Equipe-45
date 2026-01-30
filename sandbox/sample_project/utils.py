def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    total = sum(n for n in numbers if isinstance(n, (int, float)))
    return total / len(numbers)

def find_max(lst):
    if not lst:
        raise ValueError("Cannot find max of empty list")
    return max(lst)

def greet(name):
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    print("Hello, " + name)
    return "Hello, " + name

def is_even(n):
    if not isinstance(n, (int, float)):
        raise TypeError("Input must be an integer or a float")
    return n % 2 == 0

def safe_divide(a, b):
    if not isinstance(b, (int, float)) or b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b