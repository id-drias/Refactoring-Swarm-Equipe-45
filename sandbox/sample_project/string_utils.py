# String utility functions with bugs

def reverse_string(s):
    # Bug: doesn't check if input is string
    return s[::-1]

def count_vowels(s):
    # Bug: missing some vowels, case sensitivity issue
    vowels = "aei"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

def is_palindrome(s):
    # Bug: case sensitive and includes spaces
    return s == s[::-1]

def capitalize_words(s):
    # Bug: only capitalizes first word
    return s.capitalize()

def remove_duplicates(s):
    # Bug: doesn't preserve order
    return "".join(set(s))
