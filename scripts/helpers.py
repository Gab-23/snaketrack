def parse_input(rule):
    stripped_lines = []
    with open(rule) as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()                                                            # strip lines to work with strings
            stripped_lines.append(stripped_line)
    return [lines, stripped_lines]
    
def get_ranges(headers, io): 
    start_idx = [x[1] + 1 for x in headers if io == x[0]][0]                               
    end_idx = headers[[headers.index(x) + 1 for x in headers if io == x[0]][0]][1]         
    range_idxs = range(start_idx, end_idx)
    return range_idxs
    
def get_input_output(rules_paths, rules_basenames):
    import re
    input_pool = set()                                                                              # initialize input set
    output_pool = set()                                                                             # initialize output set
    rules_dic = {}
    for idx in range(len(rules_paths)):                                                             # scan rulesDir
        rule_path = rules_paths[idx]
        rule_basename = rules_basenames[idx]
        lines, stripped_lines = parse_input(rule_path)
        headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]                 
        input_output = ["output:","input:"]                                                     
        input_output_dic = {}
        for io in input_output:
            input_output_dic[io] = []                                                               # each rule starts with empty io
            if io in [x[0] for x in headers]:                                                        
                range_idxs = get_ranges(headers, io)                                        
                for idx in range_idxs:
                    to_append = re.sub(r"(.*?)=", "", stripped_lines[idx]).replace(",", "")         # remove variable assignment
                    input_output_dic[io].append(to_append)
                    if io == "input:":
                        input_pool.add(to_append)                                                   # add everything to io pool
                    else:
                        output_pool.add(to_append)
        rules_dic[rule_basename] = input_output_dic
    return([input_pool, output_pool, rules_dic])
    
def sort_dependencies(rule_basename, dic, rules_dic, dependency_chain):
    dependency_chain.append(rule_basename)
    current_outputs = dic["output:"]
    dependencies = [k for k,v in rules_dic.items() for x in v["input:"] if x in current_outputs]
    if len(dependencies) == 0:
        return dependency_chain
    else:
        return sort_dependencies(dependencies[0], rules_dic[dependencies[0]], rules_dic, dependency_chain)
    # TODO: handle exceptions
    
def track_dependencies(rules_paths, rules_basenames, upperBound, lowerBound):
    input_pool, output_pool, rules_dic = get_input_output(rules_paths, rules_basenames)
    dependency_chain = []
    if upperBound == []:
        return rules_basenames
    else:
        starting_rules = {rule:dependencies for rule,dependencies in rules_dic.items() if rule == upperBound}
    for rulename, dic in starting_rules.items():
        dependency_chain = sort_dependencies(rulename, dic, rules_dic, dependency_chain)
        if lowerBound == []:
            return dependency_chain[:]
        else:
            return dependency_chain[:(dependency_chain.index(lowerBound)+1)]
    
def get_input_output_log_dic(stripped_lines, category, prev_input_output_dic, verbose, **diffs):
    headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]                     # get headers of snakemake rule, list of tuples with (name, index)
    input_output_log = ["output:","input:", "log:"]                                                 # define input, output, log headers
    input_output_log_dic = {}                                                                       # initialize empty dict
    for iol in input_output_log:                                                                    # for each iol header
        if iol in [x[0] for x in headers]:                                                          # some rules might miss some of these headers
            range_idxs = get_ranges(headers, iol)                                                   # define range of lines where filenames are
            for idx in range_idxs:                                                                  # iterate
                if len(range_idxs) > 1 and iol == "input:":                                         # if there is more than one input
                    if list(prev_input_output_dic.values())[0]["output:"][0] in stripped_lines[idx]:
                        modified_line = modify_line(stripped_lines[idx], category, verbose, diffs)
                        input_output_log_dic[idx] = "\t" + "\t" + modified_line + "\n"
                    else:
                        input_output_log_dic[idx] = "\t" + "\t" + stripped_lines[idx] + "\n"
                else:                                                                               # modify lines and store in dictionary
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
    bool_4 = '"' not in diff
    if bool_1 and bool_2 and bool_3 and bool_4:
        return True
    else:
        return False
    
def modify_line(string, category, verbose, diffs):
    #TODO: category = track_changes(old_string, new_string)
    if category == None:
        return string
    elif category == "add_wildcard":
        for diff in diffs["newPattern"]:
            if is_wildcard(diff):
                string_new = add_wildcard(string, diff)
            else:
                raise ValueError(f"{diff} is not a properly formatted wildcard!")
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
                raise ValueError(f"{diff} is not a properly formatted wildcard!")
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
                    raise ValueError(f"{new} is not a properly formatted wildcard!")
                elif bool_new and not bool_old:
                    raise ValueError(f"{old} is not a properly formatted wildcard!")
                else:
                    raise ValueError(f"{old} and {new} are not properly formatted wildcards!")
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
        string_new = string.replace(old, new)
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
    
def write_rule(lines_updated, outputDir, ruleName):                                             
    outputPath = outputDir + ruleName                                                           # define path to write new rule
    with open(outputPath, "w") as f:                                                       
        for line in lines_updated:
            f.write(line)
