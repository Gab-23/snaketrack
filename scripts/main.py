import os
import re
import argparse
from helpers import * 

parser = argparse.ArgumentParser()  
parser.add_argument('--rulesDir',      dest='rulesDir',                   required=True,    type=str,    help='Add rulesDir')
parser.add_argument('--outputDir',     dest='outputDir',                  required=True,    type=str,    help='Add outputDir')
parser.add_argument('--change',        dest='change',                                       type=str,    help='Add change')
parser.add_argument('--oldPattern',    dest='oldPattern',    nargs = "*",                   type=str,    help='Add oldPattern')
parser.add_argument('--newPattern',    dest='newPattern',    nargs = "*",                   type=str,    help='Add newPattern')
parser.add_argument('--oldName',       dest='oldName',       nargs = "?",                   type=str,    help='Add oldName')
parser.add_argument('--newName',       dest='newName',       nargs = "?",                   type=str,    help='Add newName')
parser.add_argument('--lowerBound',    dest='lowerBound',    nargs = "?",                   type=str,    help='Add newName')


args = parser.parse_args()

rules_basenames = os.listdir(args.rulesDir)
rules_paths = [args.rulesDir + x for x in rules_basenames]
category = args.change

oldPattern = [] if args.oldPattern == None else args.oldPattern
newPattern = [] if args.newPattern == None else args.newPattern
oldName = [] if args.oldName == None else args.oldName
newName = [] if args.newName == None else args.newName
lowerBound = [] if args.lowerBound == None else args.lowerBound

if category != "add_wildcard":
    for idx in range(len(rules_paths)):                                              # scan rulesDir
        rule_path = rules_paths[idx]
        rule_basename = rules_basenames[idx]
        print(f'[log: Processing {rule_path} ]')
        lines, stripped_lines = parse_input(rule_path)
        input_output_log_dic = apply_changes(stripped_lines, category, oldPattern = oldPattern, newPattern = newPattern, oldName = oldName, newName = newName)
        lines_updated = update_lines(lines, input_output_log_dic)
        write_rule(lines_updated, args.outputDir, rule_basename)
        
else:
    dependencies = track_dependencies(rules_paths, rules_basenames, category, lowerBound)
    #for idx in range(len(dependencies)):                                              # scan rulesDir
    #    dependency_path = dependencies[idx]
    #    dependency_basename = ...
    #    print(f'[log: Processing {dependency_basename} ]')
    #    lines, stripped_lines = parse_input(rule_path)
    #    input_output_log_dic = apply_changes(stripped_lines, category, newPattern = newPattern, lowerBound = lowerBound)
    #    lines_updated = update_lines(lines, input_output_log_dic)
    #    write_rule(lines_updated, args.outputDir, rule_basename)
