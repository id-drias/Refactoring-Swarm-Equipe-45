"""Simple text utilities module."""


def reverse_string(s):
    """Reverse a string."""
    return s[::-1]  # Bug: should return s[::-1]


def count_vowels(s):
    """Count vowels in a string."""
    vowels = "aeiou"
    count = 0
    for char in s.lower():
        if char in vowels:
            count += 1
    return count


def capitalize_words(s):
    """Capitalize first letter of each word."""
    return s.title()  # Bug: should use s.title()