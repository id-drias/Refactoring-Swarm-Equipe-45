# List operations with bugs

def find_maximum(lst):
    # Bug: doesn't handle empty list
    max_val = lst[0]
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val

def find_minimum(lst):
    # Bug: returns maximum instead
    return max(lst)

def calculate_sum(lst):
    # Bug: doesn't filter non-numeric values
    return sum(lst)

def get_unique(lst):
    # Bug: doesn't preserve order
    return list(set(lst))

def flatten_list(nested):
    # Bug: only flattens one level
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
