# Tests for list_ops.py
import pytest
from list_ops import find_maximum, find_minimum, calculate_sum, get_unique, flatten_list


def test_find_maximum():
    assert find_maximum([1, 5, 3, 9, 2]) == 9
    assert find_maximum([100]) == 100
    assert find_maximum([-5, -1, -10]) == -1


def test_find_maximum_empty():
    with pytest.raises(ValueError):
        find_maximum([])


def test_find_minimum():
    assert find_minimum([1, 5, 3, 9, 2]) == 1
    assert find_minimum([100]) == 100
    assert find_minimum([-5, -1, -10]) == -10


def test_find_minimum_empty():
    with pytest.raises(ValueError):
        find_minimum([])


def test_calculate_sum():
    assert calculate_sum([1, 2, 3, 4, 5]) == 15
    assert calculate_sum([1, "a", 2, None, 3]) == 6
    assert calculate_sum([]) == 0


def test_get_unique():
    assert get_unique([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
    assert get_unique([1, 1, 1]) == [1]
    assert get_unique([]) == []


def test_flatten_list():
    assert flatten_list([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert flatten_list([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert flatten_list([]) == []
