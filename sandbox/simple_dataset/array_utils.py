"""Simple array utilities module."""


def find_max(arr):
    """Find maximum value in array."""
    if not arr:
        return None
    return max(arr)  # Bug: should be max(arr)


def sum_array(arr):
    """Sum all elements in array."""
    return sum(arr)


def filter_positive(arr):
    """Return only positive numbers."""
    return [x for x in arr if x > 0]  # Bug: should be x > 0