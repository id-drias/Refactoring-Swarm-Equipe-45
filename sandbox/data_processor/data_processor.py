# Data processing functions with bugs

def filter_even_numbers(numbers):
    # Bug: filters odd instead of even
    return [n for n in numbers if n % 2 != 0]

def sort_descending(lst):
    # Bug: sorts ascending
    return sorted(lst)

def merge_dicts(dict1, dict2):
    # Bug: overwrites instead of merging properly
    return dict1

def get_average(numbers):
    # Bug: doesn't handle empty list
    return sum(numbers) / len(numbers)

def remove_none_values(lst):
    # Bug: also removes zeros and empty strings
    return [x for x in lst if x]
