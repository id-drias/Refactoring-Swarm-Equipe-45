# Tests for utils.py
import pytest
from utils import calculate_average, find_max, greet, is_even, safe_divide


def test_calculate_average():
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0
    assert calculate_average([10, 20]) == 15.0


def test_calculate_average_empty():
    # Should handle empty list gracefully
    with pytest.raises(ValueError):
        calculate_average([])


def test_find_max():
    assert find_max([1, 5, 3, 9, 2]) == 9
    assert find_max([100]) == 100


def test_find_max_empty():
    # Should handle empty list gracefully  
    with pytest.raises(ValueError):
        find_max([])


def test_greet(capsys):
    result = greet("World")
    captured = capsys.readouterr()
    assert "Hello, World" in captured.out
    assert result == "Hello, World"  # Should return the greeting


def test_is_even():
    assert is_even(2) == True
    assert is_even(4) == True
    assert is_even(3) == False
    assert is_even(7) == False


def test_safe_divide():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(9, 3) == 3.0


def test_safe_divide_by_zero():
    # Should handle division by zero gracefully
    with pytest.raises(ValueError):
        safe_divide(10, 0)
