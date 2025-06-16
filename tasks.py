import csv
from io import StringIO

_cache = {}

def task1(search, data):
    """
    Looks for a row in CSV data that matches the given search criteria,
    and returns the 'value' from that row. Returns '-1' if no match found.

    Args:
        search (dict): Dictionary with keys and values to match in the CSV (except 'value').
        data (str): CSV data as a string, with columns including 'value'.

    Returns:
        str: The 'value' from the matching row, or '-1' if nothing matches.

    Example:
        data = 'side,currency,value\\nIN,PLN,1\\nIN,EUR,2\\nOUT,ANY,3'
        task1({'side': 'IN', 'currency': 'PLN'}, data)  # returns '1'
    """

    # If we've already parsed this data before, just reuse it
    if data in _cache:
        rows = _cache[data]
    else:
        # Parse the CSV string into a list of dicts
        s = StringIO(data)
        reader = csv.DictReader(s)
        rows = []
        for row in reader:
            # Clean up whitespace and quotes from each value
            clean_row = {k: v.strip().strip("'\"") if v is not None else v for k, v in row.items()}
            rows.append(clean_row)
        # Cache the parsed rows so we don't parse again next time
        _cache[data] = rows

    # If no data, just return '-1'
    if not rows:
        return '-1'

    # Get all the keys except 'value' — those are the fields we search by
    key_fields = set(rows[0].keys()) - {'value'}
    search_keys = set(search.keys())

    # Make sure the search keys match what we expect
    if search_keys != key_fields:
        raise Exception('Key mismatch')

    # Go through each row and check if it matches the search criteria
    for row in rows:
        # Check all keys one by one
        if all(row[key] == str(search[key]) for key in search_keys):
            # Found a match — return the 'value'
            return row['value']

    # No match found
    return '-1'


# Example usage:
data = 'side,currency,value\nIN,PLN,1\nIN,EUR,2\nOUT,ANY,3'

print(task1({'side': 'IN', 'currency': 'GBP'}, data))  # Output: '-1'
print(task1({'side': 'IN', 'currency': 'PLN'}, data))  # Output: '1'
print(task1({'side': 'IN', 'currency': 'EUR'}, data))  # Output: '2'
print(task1({'side': 'OUT', 'currency': 'ANY'}, data)) # Output: '3'



def task2(search_list, data):
    """
    Calculates a weighted average of 'value' fields from CSV data for given search criteria.

    The function:
    - Parses CSV data once and caches the parsed rows for reuse.
    - For each search dict in search_list, finds the first matching row.
    - Applies weights: 20 if 'value' is even, 10 if odd.
    - Returns the weighted average as a string formatted to 1 decimal place.
    - Returns '0.0' if no matches found.

    Args:
        search_list (list of dict): Each dict contains key-value pairs to match rows in CSV.
        data (str): CSV data as a string, with columns including keys and a 'value' column.

    Returns:
        str: Weighted average of matched 'value's or '0.0' if none matched.

    Example:
        search_list = [
            {'a': 1, 'b': 2},
            {'a': 3, 'b': 4}
        ]
        data = "a,b,value\n1,2,10\n3,4,15\n"
        task2(search_list, data)  # returns '12.5'
    """

    # If we've already parsed this data before, just reuse it to save time
    if data in _cache:
        rows = _cache[data]
    else:
        # Parse the CSV string into a list of dicts
        s = StringIO(data)
        reader = csv.DictReader(s)
        rows = []
        for row in reader:
            # Clean whitespace and remove quotes from each value
            clean_row = {k: v.strip().strip("'\"") if v is not None else v for k, v in row.items()}
            rows.append(clean_row)
        # Cache the parsed rows for next time
        _cache[data] = rows

    # If no data, return zero as string
    if not rows:
        return '0.0'

    # Figure out which columns are keys (everything except 'value')
    key_names = set(rows[0].keys()) - {'value'}

    # Convert all search values to strings once, so we don't do it repeatedly later
    prepared_search_list = [{k: str(v) for k, v in search.items()} for search in search_list]

    total_weighted_value = 0
    total_weight = 0

    # For each search dict, find the first matching row in data
    for search in prepared_search_list:
        for row in rows:
            # Check if all key columns match the search values
            match = True
            for key in key_names:
                if row[key] != search[key]:
                    match = False
                    break
            if match:
                val = int(row['value'])
                # Weight 20 if even, 10 if odd
                weight = 20 if val % 2 == 0 else 10
                total_weighted_value += val * weight
                total_weight += weight
                break  # Found match for this search, move to next

    # If no matches at all, return zero
    if total_weight == 0:
        return '0.0'

    # Calculate weighted average and format nicely
    weighted_avg = total_weighted_value / total_weight
    return f"{weighted_avg:.1f}"


# Example usage:
with open('find_match_average.dat', 'r', encoding='utf-8') as f:
    data = f.read()
    
search_list = [
    {'a': 862984, 'b': 29105, 'c': 605280, 'd': 678194, 'e': 302120},
    {'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}
]

result = task2(search_list, data)
print(result)