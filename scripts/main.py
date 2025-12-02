input_output_log_dic = get_input_output_log(stripped_lines)
for idx in range(len(lines)):                                                               # for each line
    if idx in list(input_output_log_dic.keys()):                                            # if the line is one we modified
        lines[idx] = input_output_log_dic[idx]                                              # change it
    else:
        lines[idx] = lines[idx]

