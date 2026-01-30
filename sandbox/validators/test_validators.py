# Tests for validators.py
import pytest
from validators import is_valid_email, is_valid_phone, is_valid_password, is_valid_username, is_positive_number


def test_is_valid_email():
    assert is_valid_email("user@example.com") == True
    assert is_valid_email("test.email@domain.org") == True
    assert is_valid_email("invalid-email") == False
    assert is_valid_email("@nodomain.com") == False
    assert is_valid_email("noatsign.com") == False


def test_is_valid_phone():
    assert is_valid_phone("1234567890") == True
    assert is_valid_phone("123-456-7890") == True
    assert is_valid_phone("(123) 456-7890") == True
    assert is_valid_phone("123") == False
    assert is_valid_phone("") == False


def test_is_valid_password():
    assert is_valid_password("SecurePass123!") == True
    assert is_valid_password("Abcd1234") == True
    assert is_valid_password("short") == False
    assert is_valid_password("nouppercase1!") == False
    assert is_valid_password("NOLOWERCASE1!") == False


def test_is_valid_username():
    assert is_valid_username("john_doe") == True
    assert is_valid_username("user123") == True
    assert is_valid_username("ab") == False
    assert is_valid_username("invalid@user!") == False


def test_is_positive_number():
    assert is_positive_number(5) == True
    assert is_positive_number(0.5) == True
    assert is_positive_number(0) == False
    assert is_positive_number(-5) == False
    with pytest.raises(TypeError):
        is_positive_number("5")
