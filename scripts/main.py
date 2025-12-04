import os
import argparse
from helpers import * 

parser = argparse.ArgumentParser()  
parser.add_argument('--rulesDir',   dest='rulesDir',                required=True, type=str, help='Add rulesDir')
parser.add_argument('--outputDir',  dest='outputDir',               required=True, type=str, help='Add outputDir')
parser.add_argument('--change',     dest='change',                                 type=str, help='Add change')
parser.add_argument('--oldPattern', dest='oldPattern', nargs = "*",                type=str, help='Add oldPattern')
parser.add_argument('--newPattern', dest='newPattern', nargs = "*",                type=str, help='Add newPattern')
parser.add_argument('--oldName',    dest='oldName',    nargs = "?",                type=str, help='Add oldName')
parser.add_argument('--newName',    dest='newName',    nargs = "?",                type=str, help='Add newName')

args = parser.parse_args()

rules_basenames = os.listdir(args.rulesDir)
rules_paths = [args.rulesDir + x for x in rules_basenames]
category = args.change

oldPattern = [] if args.oldPattern == None else args.oldPattern
newPattern = [] if args.newPattern == None else args.newPattern
oldName = [] if args.oldName == None else args.oldName
newName = [] if args.newName == None else args.newName

for idx in range(len(rules_paths)):                                              # scan rulesDir
    rule_path = rules_paths[idx]
    rule_basename = rules_basenames[idx]
    print(f'[log: Processing {rule_path} ]')
    lines, stripped_lines = parse_input(rule_path)
    input_output_log_dic = apply_changes(stripped_lines, category, oldPattern = oldPattern, newPattern = newPattern, oldName = oldName, newName = newName)
    lines = update_lines(lines, input_output_log_dic)
    write_rule(lines, args.outputDir, rule_basename)
