import os
rules = os.listdir(".")                                                                     # scan rulesDir
rule = rules[0]                                                                             # get rule

with open(rule) as f:
    lines = f.readlines()
    stripped_lines = []
    for line in lines:
        stripped_line = line.strip()                                                        # strip lines to work with strings
        stripped_lines.append(stripped_line)

