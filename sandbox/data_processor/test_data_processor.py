# Tests for data_processor.py
import pytest
from data_processor import filter_even_numbers, sort_descending, merge_dicts, get_average, remove_none_values


def test_filter_even_numbers():
    assert filter_even_numbers([1, 2, 3, 4, 5, 6]) == [2, 4, 6]
    assert filter_even_numbers([1, 3, 5]) == []
    assert filter_even_numbers([2, 4, 6]) == [2, 4, 6]
    assert filter_even_numbers([]) == []


def test_sort_descending():
    assert sort_descending([3, 1, 4, 1, 5]) == [5, 4, 3, 1, 1]
    assert sort_descending([1]) == [1]
    assert sort_descending([]) == []


def test_merge_dicts():
    assert merge_dicts({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_dicts({"a": 1}, {"a": 2}) == {"a": 2}
    assert merge_dicts({}, {"b": 2}) == {"b": 2}


def test_get_average():
    assert get_average([1, 2, 3, 4, 5]) == 3.0
    assert get_average([10, 20]) == 15.0


def test_get_average_empty():
    with pytest.raises(ValueError):
        get_average([])


def test_remove_none_values():
    assert remove_none_values([1, None, 2, None, 3]) == [1, 2, 3]
    assert remove_none_values([None, None]) == []
    assert remove_none_values([0, "", None, "hello"]) == [0, "", "hello"]
