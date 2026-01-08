from track_changes import *

def get_ranges(headers, io):                                                                        # get index from header to next header
    start_idx = [x[1] + 1 for x in headers if io == x[0]][0]                               
    end_idx = headers[[headers.index(x) + 1 for x in headers if io == x[0]][0]][1]         
    range_idxs = range(start_idx, end_idx)
    return range_idxs
        
def get_input_output_log_dic(stripped_lines, category, prev_input_output_dic, upperBound, verbose, **diffs):
    headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]                     # get headers of snakemake rule, list of tuples with (name, index)
    input_output_log = ["output:","input:", "log:"]                                                 # define input, output, log headers
    input_output_log_dic = {}                                                                       # initialize empty dict
    for iol in input_output_log:                                                                    # for each iol header
        if iol in [x[0] for x in headers]:                                                          # some rules might miss some of these headers
            range_idxs = get_ranges(headers, iol)                                                   # define range of lines where filenames are
            if len(range_idxs) > 1 and iol == "input:" and upperBound != []:                        # if there is more than one input and upperBound is specified
                for idx in range_idxs:                                                              # iterate
                    if any([x in stripped_lines[idx] for x in list(prev_input_output_dic.values())[0]["output:"]]):
                        modified_line = modify_line(stripped_lines[idx], category, verbose, diffs)
                        input_output_log_dic[idx] = "\t" + "\t" + modified_line + "\n"
                    else:
                        input_output_log_dic[idx] = "\t" + "\t" + stripped_lines[idx] + "\n"
            else:                                                                                   # modify lines and store in dictionary
                for idx in range_idxs:
                    modified_line = modify_line(stripped_lines[idx], category, verbose, diffs)
                    input_output_log_dic[idx] = "\t" + "\t" + modified_line + "\n"
        else:
            pass
    return input_output_log_dic

def add_wildcard(string, diff):
    parts = string.split("/")
    basename = parts[-1]
    basename = diff + "_" + basename
    parts[-1] = basename
    return "/".join(parts)

def is_wildcard(diff):
    bool_1 = type(diff) == str
    bool_2 = diff[0] == "{"
    bool_3 = diff[-1] == "}"
    bool_4 = diff.count("{") == 1                                                                                   # modify here, should be max {{}}
    bool_5 = diff.count("}") == 1
    bool_6 = '"' not in diff
    if bool_1 and bool_2 and bool_3 and bool_4 and bool_5 and bool_6:
        return True
    else:
        return False
    
def modify_line(string, category, verbose, diffs):
    if category == None:
        return string
    elif category == "add_wildcard":
        for diff in diffs["newPattern"]:
            if is_wildcard(diff):
                string_new = add_wildcard(string, diff)
            else:
                raise NameError(f"{diff} is not a properly formatted wildcard!")
        if verbose:
            if string != string_new:
                print(f'[log: << {string} ]')
                print(f'[log: >> {string_new} ]')
        return string_new
    elif category == "remove_wildcard":
        for diff in diffs["oldPattern"]:
            if is_wildcard(diff):
                string_new = string.replace(diff, "")
            else:
                raise NameError(f"{diff} is not a properly formatted wildcard!")
        if verbose:
            if string != string_new:
                print(f'[log: << {string} ]')
                print(f'[log: >> {string_new} ]')
        return string_new
    elif category == "modify_wildcard":
        olds = diffs["oldPattern"]
        news = diffs["newPattern"]
        if len(olds) == len(news):
            for idx in range(len(diffs["oldPattern"])):
                old = diffs["oldPattern"][idx]
                bool_old = is_wildcard(old)
                new = diffs["newPattern"][idx]
                bool_new = is_wildcard(new)
                if bool_old and bool_new:
                    string_new = string.replace(old, new)
                elif bool_old and not bool_new:
                    raise NameError(f"{new} is not a properly formatted wildcard!")
                elif bool_new and not bool_old:
                    raise NameError(f"{old} is not a properly formatted wildcard!")
                else:
                    raise NameError(f"{old} and {new} are not properly formatted wildcards!")
            if verbose:
                if string != string_new:
                    print(f'[log: << {string} ]')
                    print(f'[log: >> {string_new} ]')
            return string_new
        else:
            raise ValueError(f"oldPattern [{len(olds)} elements] and newPattern [{len(news)} elements] have different lengths")
    elif category == "modify_filename":
        old = diffs["oldName"]
        new = diffs["newName"]
        new_validated = track_changes(old, new)
        string_new = string.replace(old, new_validated)
        if verbose:
            if string != string_new:
                print(f'[log: << {string} ]')
                print(f'[log: >> {string_new} ]')
        return string_new
    
def update_lines(lines, input_output_log_dic):
    lines_copy = lines.copy()
    for idx in range(len(lines_copy)):                                                          # for each line
        if idx in list(input_output_log_dic.keys()):                                            # if the line is one we modified
            lines_copy[idx] = input_output_log_dic[idx]                                         # change it
        else:
            lines_copy[idx] = lines[idx]
    return lines_copy
