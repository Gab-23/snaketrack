def identify_wildcards(values, ranges, cumulative_idx = 0):
    not_bool_opening = "{" not in values
    not_bool_closing = "}" not in values
    if not_bool_opening and not_bool_closing:
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

def get_comp_ranges(ranges):
    lower = [x[0] for x in ranges]
    upper = [x[1] for x in ranges]
    init_idx = 0
    comp_ranges = []
    for idx in range(len(lower)):
        if idx == init_idx:
            comp_range = (init_idx,lower[idx])
            comp_ranges.append(comp_range)
        else:
            comp_range = (upper[idx-1],lower[idx])
            comp_ranges.append(comp_range)
    return comp_ranges

def track_changes(oldName, newName):
    import difflib
    change_tracker = difflib.ndiff(oldName, newName)                            # track differences between the two strings
    types = []                                                                  # initialize empty lists
    values = []
    for index, element in enumerate(change_tracker):                            # iterate over the differences
        change_report = [x for x in element]                                    # extract list containing differences
        category = change_report[0]                                             # category is the first element of the list
        types.append(category)
        value = change_report[2]                                                # value is the third element of the list
        values.append(value)
    bool_opening_values = "{" in values
    bool_closing_values = "}" in values
    if bool_opening_values and bool_closing_values:
        ranges = identify_wildcards(values, [])                                 # track changes for identification of wildcards
    else:
        ranges = []
    categories = []
    diffs_list = []
    if len(ranges) > 0: 
        for range in ranges:                                                        # iterate over them
            diffs = {}
            types_subset = types[range[0]:range[1]]
            values_subset = values[range[0]:range[1]]
            old = "".join([values_subset[idx] for idx,elem in enumerate(types_subset) if elem == " " or elem == "-"])
            new = "".join([values_subset[idx] for idx,elem in enumerate(types_subset) if elem == " " or elem == "+"])
            unique_changes = set(types_subset)                                      # take the unique set of changes
            bool_add = "+" in unique_changes
            bool_remove = "-" in unique_changes
            if  bool_add and bool_remove:
                old_count_bool = old.count("{") == old.count("}")
                new_count_bool = new.count("{") == new.count("}")
                if old_count_bool and new_count_bool:
                    category = "modify_wildcard"
                    diffs["oldPattern"] = [old]
                    diffs["newPattern"] = [new]
                elif new_count_bool and not old_count_bool:
                    raise ValueError(f"Broken wildcard detected in {old}")
                elif old_count_bool and not new_count_bool:
                    raise ValueError(f"Broken wildcard detected in {new}")
            elif bool_add and not bool_remove:
                new_count_bool = new.count("{") == new.count("}")
                if new_count_bool:
                    category = "add_wildcard"
                    diffs["newPattern"] = [new]
                else:
                    raise ValueError(f"Broken wildcard detected in {new}")
            elif bool_remove and not bool_add:
                old_count_bool = old.count("{") == old.count("}")
                if old_count_bool:
                    category = "remove_wildcard"
                    diffs["oldPattern"] = [old]
                else:
                    raise ValueError(f"Broken wildcard detected in {old}")
            else:
                category = None
            categories.append(category)
            diffs_list.append(diffs)
        comp_ranges = get_comp_ranges(ranges)
    else:
        comp_ranges = [(0,len(values))]
        for comp_range in comp_ranges:
            comp_types_subset = types[comp_range[0]:comp_range[1]]
            comp_values_subset = values[comp_range[0]:comp_range[1]]
            comp_string = "".join([comp_values_subset[idx] for idx,elem in enumerate(comp_types_subset)])
            bool_opening = "{" in comp_string
            bool_closing = "}" in comp_string
            if bool_opening or bool_closing:
                raise ValueError(f"Broken wildcard detected in {comp_string}")
    return newName
