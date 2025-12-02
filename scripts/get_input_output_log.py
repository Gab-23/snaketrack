def get_input_output_log(stripped_lines):    
    headers = [(x,stripped_lines.index(x)) for x in stripped_lines if ":" in x]             # get headers of snakemake rule, list of tuples with (name, index)
    input_output_log = ["output:","input:", "log:"]                                         # define input, output, log headers
    input_output_log_dic = {}                                                               # initialize empty dict
    for iol in input_output_log:                                                            # for each iol header
        start_idx = [x[1] + 1 for x in headers if iol == x[0]][0]                           # the start index of files is the next index of the header
        end_idx = headers[[headers.index(x) + 1 for x in headers if iol == x[0]][0]][1]     # the end index of files is the index of the next header
        range_idxs = range(start_idx, end_idx)                                              # define range of lines where filenames are
        for idx in range_idxs:                                                              # iterate
            input_output_log_dic[idx] = "\t" + '\"' + modify_line(stripped_lines[idx].replace('\"',''), ...) + '\"' + "\n"      # modify them and store in dictionary
    return input_output_log_dic                                                                                                 # return        

