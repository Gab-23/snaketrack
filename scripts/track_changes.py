import difflib

def identify_wildcards(values, ranges, cumulative_idx = 0):
    if len(values) == 0:
        return ranges
    else:
        opening = values.index("{")
        closing = values.index("}")
        if opening < closing:
            ranges.append((opening+cumulative_idx, closing+cumulative_idx+1))
        else:
            pass
        break_idx = closing+1
        cumulative_idx = cumulative_idx + break_idx
        values = values[break_idx:]
        return identify_wildcards(values, ranges, cumulative_idx)

string_a = "file1_{aa}_{bb}_{cc}"
string_b = "file2_{bc}_{cb}_{dd}"

change_tracker = difflib.ndiff(string_a, string_b) 
categories = []
values = []
for index, element in enumerate(change_tracker):
    change_report = [x for x in element]
    category = change_report[0]
    categories.append(category)
    value = change_report[2]
    values.append(value)

ranges = []
ranges = identify_wildcards(values, ranges)
for range in ranges:
    unique_changes = set(categories[range[0]:range[1]])
    bool_add = "+" in unique_changes
    bool_remove = "-" in unique_changes
    if  bool_add and bool_remove:
        category = "modify_wildcard"
    elif bool_add and not bool_remove:
        category = "add_wildcard"
    elif bool_remove and not bool_add:
        category = "remove_wildcard"
    else:
        category = None
    print(category)
