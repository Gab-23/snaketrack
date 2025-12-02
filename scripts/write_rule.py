def write_rule(lines, output_dir, ruleName):                                             
    output_path = output_dir + ruleName                                                     # define path to write new rule
    with open(output_path, "w") as f:                                                       
        for line in lines:
            f.write(element)
