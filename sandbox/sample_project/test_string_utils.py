# Tests for string_utils.py
import pytest
from string_utils import reverse_string, count_vowels, is_palindrome, capitalize_words, remove_duplicates


def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("a") == "a"
    assert reverse_string("") == ""


def test_reverse_string_invalid():
    with pytest.raises(TypeError):
        reverse_string(123)


def test_count_vowels():
    assert count_vowels("hello") == 2
    assert count_vowels("HELLO") == 2
    assert count_vowels("xyz") == 0
    assert count_vowels("aeiouAEIOU") == 10


def test_is_palindrome():
    assert is_palindrome("racecar") == True
    assert is_palindrome("Race Car") == True
    assert is_palindrome("hello") == False
    assert is_palindrome("A man a plan a canal Panama") == True


def test_capitalize_words():
    assert capitalize_words("hello world") == "Hello World"
    assert capitalize_words("python programming") == "Python Programming"
    assert capitalize_words("a") == "A"


def test_remove_duplicates():
    assert remove_duplicates("aabbcc") == "abc"
    assert remove_duplicates("hello") == "helo"
    assert remove_duplicates("") == ""
