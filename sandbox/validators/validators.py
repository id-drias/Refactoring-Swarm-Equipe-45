# Validation functions with bugs

def is_valid_email(email):
    # Bug: too simple validation
    return "@" in email

def is_valid_phone(phone):
    # Bug: doesn't handle different formats
    return len(phone) == 10

def is_valid_password(password):
    # Bug: only checks length
    return len(password) >= 8

def is_valid_username(username):
    # Bug: allows special characters
    return len(username) >= 3

def is_positive_number(value):
    # Bug: doesn't handle string numbers
    return value > 0
