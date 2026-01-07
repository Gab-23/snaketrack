from input_output_management import *
from line_manipulation import *

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
    dependencies = [k for k,v in rules_dic.items() for x in v["input:"] if x in current_outputs]    # recursively look for a rule with input = to other rule output
    if len(dependencies) == 0:
        return dependency_chain
    else:
        return sort_dependencies(dependencies[0], rules_dic[dependencies[0]], rules_dic, dependency_chain)

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

