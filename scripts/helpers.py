def parse_input(rule):
    stripped_lines = []
    with open(rule) as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()                                                        # strip lines to work with strings
            stripped_lines.append(stripped_line)
    return [lines, stripped_lines]
    
    
def apply_changes(stripped_lines, category, **diffs):
    headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]                 # get headers of snakemake rule, list of tuples with (name, index)
    input_output_log = ["output:","input:", "log:"]                                             # define input, output, log headers
    input_output_log_dic = {}                                                                   # initialize empty dict
    for iol in input_output_log:                                                                # for each iol header
        if iol in [x[0] for x in headers]:                                                      # some rules might miss some of these headers
            start_idx = [x[1] + 1 for x in headers if iol == x[0]][0]                           # the start index of files is the next index of the header
            end_idx = headers[[headers.index(x) + 1 for x in headers if iol == x[0]][0]][1]     # the end index of files is the index of the next header
            range_idxs = range(start_idx, end_idx)                                              # define range of lines where filenames are
            for idx in range_idxs:                                                              # iterate
                # modify lines and store in dictionary
                modified_line = modify_line(stripped_lines[idx].replace('\"',''), category, diffs)
                # todo: keep track of variables being assigned
                input_output_log_dic[idx] = "\t" + '\"' + modified_line + '\"' + "\n"
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
            return string_new
        else:
            raise ValueError(f"oldPattern [{len(olds)} elements] and newPattern [{len(news)} elements] have different lengths")
    elif category == "modify_filename":
        old = diffs["oldName"]
        new = diffs["newName"]
        string_new = string.replace(old, new) 
        return string_new
    
def update_lines(lines, input_output_log_dic):
    for idx in range(len(lines)):                                                               # for each line
        if idx in list(input_output_log_dic.keys()):                                            # if the line is one we modified
            lines[idx] = input_output_log_dic[idx]                                              # change it
        else:
            lines[idx] = lines[idx]
    return lines
    
def write_rule(lines, outputDir, ruleName):                                             
    outputPath = outputDir + ruleName                                                           # define path to write new rule
    print(f'[log: Writing {outputPath} ]')
    with open(outputPath, "w") as f:                                                       
        for line in lines:
            f.write(line)
