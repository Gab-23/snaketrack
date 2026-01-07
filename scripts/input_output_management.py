def parse_input(rule):
    stripped_lines = []
    with open(rule) as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()                                                            # strip lines to work with strings
            stripped_lines.append(stripped_line)
    return [lines, stripped_lines]

def write_rule(lines_updated, outputDir, ruleName):                                             
    outputPath = outputDir + ruleName                                                               # define path to write new rule
    with open(outputPath, "w") as f:                                                       
        for line in lines_updated:
            f.write(line)

