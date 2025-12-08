def parse_input(rule):
    stripped_lines = []
    with open(rule) as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()                                                            # strip lines to work with strings
            stripped_lines.append(stripped_line)
    return [lines, stripped_lines]
    
def track_dependencies(rules_paths, rules_basenames, category, lowerBound):
    import re
    input_pool = set()
    output_pool = set()
    for idx in range(len(rules_paths)):                                                             # scan rulesDir
        rule_path = rules_paths[idx]
        rule_basename = rules_basenames[idx]
        print(f'[log: Tracking dependencies {rule_path} ]')
        lines, stripped_lines = parse_input(rule_path)
        headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]                 
        input_output = ["output:","input:"]                                                     
        input_output_dic = {}
        for io in input_output:
            input_output_dic[io] = []
            if io in [x[0] for x in headers]:                                                        
                start_idx = [x[1] + 1 for x in headers if io == x[0]][0]                               
                end_idx = headers[[headers.index(x) + 1 for x in headers if io == x[0]][0]][1]         
                range_idxs = range(start_idx, end_idx)                                                  
                for idx in range_idxs:
                    to_append = re.sub(r"(.*?)=", "", stripped_lines[idx]).replace(",", "")
                    input_output_dic[io].append(to_append)
                    if io == "input:":
                        print(to_append)
                        input_pool.add(to_append)
                    else:
                        output_pool.add(to_append)
                                                                                                    
    print(input_pool)
    print(output_pool)
    return input_output_dic
    
def apply_changes(stripped_lines, category, **diffs):
    headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]                     # get headers of snakemake rule, list of tuples with (name, index)
    input_output_log = ["output:","input:", "log:"]                                                 # define input, output, log headers
    input_output_log_dic = {}                                                                       # initialize empty dict
    for iol in input_output_log:                                                                    # for each iol header
        if iol in [x[0] for x in headers]:                                                          # some rules might miss some of these headers
            start_idx = [x[1] + 1 for x in headers if iol == x[0]][0]                               # the start index of files is the next index of the header
            end_idx = headers[[headers.index(x) + 1 for x in headers if iol == x[0]][0]][1]         # the end index of files is the index of the next header
            range_idxs = range(start_idx, end_idx)                                                  # define range of lines where filenames are
            for idx in range_idxs:                                                                  # iterate
                # modify lines and store in dictionary
                modified_line = modify_line(stripped_lines[idx], category, diffs)
                input_output_log_dic[idx] = "\t" + "\t" + modified_line + "\n"
        else:
            pass
    return input_output_log_dic
    
def modify_line(string, category, diffs):
    # todo: category = track_changes(old_string, new_string)
    if category == None:
        return string
    elif category == "add_wildcard":
        # check for wildcard
        pass
    elif category == "remove_wildcard":
        # check for wildcard
        for diff in diffs["oldPattern"]:
            string_new = string.replace(diff, "")
        if string != string_new:
            print(f'[log: << {string} ]')
            print(f'[log: >> {string_new} ]')
        return string_new
    elif category == "modify_wildcard":
        # check for wildcard
        olds = diffs["oldPattern"]
        news = diffs["newPattern"]
        if len(olds) == len(news):
            for idx in range(len(diffs["oldPattern"])):
                old = diffs["oldPattern"][idx]
                new = diffs["newPattern"][idx]
                string_new = string.replace(old, new)
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
