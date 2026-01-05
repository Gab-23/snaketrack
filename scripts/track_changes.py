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

def track_changes(oldString, newString):
    import difflib
    change_tracker = difflib.ndiff(oldString, newString)                        # track differences between the two strings
    types = []                                                                  # initialize empty lists
    values = []
    for index, element in enumerate(change_tracker):                            # iterate over the differences
        change_report = [x for x in element]                                    # extract list containing differences
        category = change_report[0]                                             # category is the first element of the list
        types.append(category)
        value = change_report[2]                                                # value is the third element of the list
        values.append(value)
    
    ranges = identify_wildcards(values, [])                                     # track changes for identification of wildcards
    categories = []
    diffs_list = []
    for range in ranges:                                                        # iterate over them
        diffs = {}
        types_subset = types[range[0]:range[1]]
        values_subset = values[range[0]:range[1]]
        unique_changes = set(types_subset)                                      # take the unique set of changes
        bool_add = "+" in unique_changes
        bool_remove = "-" in unique_changes
        if  bool_add and bool_remove:
            category = "modify_wildcard"
            diffs["oldPattern"] = ["".join([values_subset[idx] for idx,elem in enumerate(types_subset) if elem == " " or elem == "-"])]
            diffs["newPattern"] = ["".join([values_subset[idx] for idx,elem in enumerate(types_subset) if elem == " " or elem == "+"])]
        elif bool_add and not bool_remove:
            category = "add_wildcard"
            diffs["newPattern"] = ["".join([values_subset[idx] for idx,elem in enumerate(types_subset) if elem == " " or elem == "+"])]
        elif bool_remove and not bool_add:
            category = "remove_wildcard"
            diffs["oldPattern"] = ["".join([values_subset[idx] for idx,elem in enumerate(types_subset) if elem == " " or elem == "-"])]
        else:
            category = None
        categories.append(category)
        diffs_list.append(diffs)
    print(categories)
    print(diffs_list)


oldString = "file1_{aa}_{bb}_{cc}_{ee}"
newString = "file2_{bc_{cb}_{dd}"
track_changes(oldString, newString)

# TODO: handle exceptions:
#       check for wildcards changes
#       handle non wildcards changes
#       log to user the changes
#       handle case of { or } in {}         --> broken wildcard exception



# for sort dag and refactor dag: 
#   reuse these functions to detect wildcards and to track changes
