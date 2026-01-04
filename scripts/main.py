import os
import re
import argparse
from helpers import * 

parser = argparse.ArgumentParser()  
parser.add_argument('--rulesDir',      dest='rulesDir',                      required=True,                  type=str,    help='Add rulesDir')
parser.add_argument('--outputDir',     dest='outputDir',                     required=True,                  type=str,    help='Add outputDir')
parser.add_argument('--change',        dest='change',                                                        type=str,    help='Add change')
parser.add_argument('--oldPattern',    dest='oldPattern',    nargs = "*",                                    type=str,    help='Add oldPattern')
parser.add_argument('--newPattern',    dest='newPattern',    nargs = "*",                                    type=str,    help='Add newPattern')
parser.add_argument('--oldName',       dest='oldName',       nargs = "?",                                    type=str,    help='Add oldName')
parser.add_argument('--newName',       dest='newName',       nargs = "?",    required=True,                  type=str,    help='Add newName')
parser.add_argument('--lowerBound',    dest='lowerBound',    nargs = "?",    required=True,                  type=str,    help='Add lowerBound')
parser.add_argument('--upperBound',    dest='upperBound',    nargs = "?",                                    type=str,    help='Add upperBound')
parser.add_argument('--verbose',       dest='verbose',                                                                    help='Add verbose',         action="store_true")

args = parser.parse_args()

rules_basenames = os.listdir(args.rulesDir)
rules_paths = [args.rulesDir + x for x in rules_basenames]
category = args.change

oldPattern = [] if args.oldPattern == None else args.oldPattern
newPattern = [] if args.newPattern == None else args.newPattern
oldName = [] if args.oldName == None else args.oldName
newName = [] if args.newName == None else args.newName
lowerBound = [] if args.lowerBound == None else args.lowerBound
upperBound = [] if args.upperBound == None else args.upperBound

verbose = args.verbose

dependencies = track_dependencies(rules_paths, rules_basenames, upperBound, lowerBound)
print(dependencies)
for idx in range(len(dependencies)):
    dependency_path = args.rulesDir + dependencies[idx]
    dependency_basename = dependencies[idx]
    if verbose:
        print(f'[log: Processing {dependency_basename} ]')
    lines, stripped_lines = parse_input(dependency_path)
    if idx > 0:
        prev_dependency_path = args.rulesDir + dependencies[idx-1]
        prev_dependency_basename = dependencies[idx-1]
        prev_input_output_dic = get_input_output([prev_dependency_path], [prev_dependency_basename])[2]
    else:
        prev_input_output_dic = None
    input_output_log_dic = get_input_output_log_dic(stripped_lines, category, prev_input_output_dic, verbose, oldPattern = oldPattern, newPattern = newPattern, oldName = oldName, newName = newName)
    lines_updated = update_lines(lines, input_output_log_dic)
    write_rule(lines_updated, args.outputDir, dependency_basename)

new_rules_basenames = os.listdir(args.outputDir)
new_rules_paths = [args.outputDir + x for x in rules_basenames]
new_dependencies = track_dependencies(new_rules_paths, new_rules_basenames, upperBound, lowerBound)
print(new_dependencies)
exit_code = 1 - (dependencies == new_dependencies)
exit(exit_code)
