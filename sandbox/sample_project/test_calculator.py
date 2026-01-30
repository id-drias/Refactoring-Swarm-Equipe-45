# Tests for calculator.py
import pytest
from calculator import add, subtract, multiply, divide, power


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_add_none():
    with pytest.raises(TypeError):
        add(None, 5)


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(5, 5) == 0
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0
    assert multiply(-2, 3) == -6


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(9, 3) == 3.0


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)


def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(2, -1) == 0.5
