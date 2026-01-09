import os
import re
import argparse

from tracking_dependencies import *
from line_manipulation import *

parser = argparse.ArgumentParser()  
parser.add_argument('--rulesDir',      dest='rulesDir',                      required=True,                  type=str,    help='Add rulesDir')
parser.add_argument('--outputDir',     dest='outputDir',                     required=True,                  type=str,    help='Add outputDir')
parser.add_argument('--change',        dest='change',                                                        type=str,    help='Add change')
parser.add_argument('--oldPattern',    dest='oldPattern',    nargs = "*",                                    type=str,    help='Add oldPattern')
parser.add_argument('--newPattern',    dest='newPattern',    nargs = "*",                                    type=str,    help='Add newPattern')
parser.add_argument('--oldName',       dest='oldName',       nargs = "?",                                    type=str,    help='Add oldName')
parser.add_argument('--newName',       dest='newName',       nargs = "?",                                    type=str,    help='Add newName')
parser.add_argument('--lowerBound',    dest='lowerBound',    nargs = "?",                                    type=str,    help='Add lowerBound')
parser.add_argument('--upperBound',    dest='upperBound',    nargs = "?",                                    type=str,    help='Add upperBound')
parser.add_argument('--verbose',       dest='verbose',                                                                    help='Add verbose',         action="store_true")

args = parser.parse_args()

category = args.change

oldPattern = [] if args.oldPattern == None else args.oldPattern
newPattern = [] if args.newPattern == None else args.newPattern
oldName = [] if args.oldName == None else args.oldName
newName = [] if args.newName == None else args.newName
lowerBound = [] if args.lowerBound == None else args.lowerBound
upperBound = [] if args.upperBound == None else args.upperBound

verbose = args.verbose

bool_mismatching_bounds = ((lowerBound == [] and upperBound != []) or (upperBound == [] and lowerBound != []))
bool_category_modify_filename = category == "modify_filename"
bool_category_add_wildcard = category == "add_wildcard"
bool_category_remove_wildcard = category == "remove_wildcard"
bool_category_modify_wildcard = category == "modify_wildcard"
bool_existing_lowerBound = lowerBound != []
bool_existing_upperBound = upperBound != []
bool_existing_oldName = oldName != []
bool_existing_newName = newName != []
bool_existing_oldPattern = oldPattern != []
bool_existing_newPattern = newPattern != []

# define exceptions related to arguments
if bool_mismatching_bounds:
    raise KeyError(f"Cannot specify --lowerBound without specifying --upperBound and viceversa")

if bool_category_modify_filename and (bool_existing_lowerBound or bool_existing_upperBound):
    raise KeyError(f"Cannot specify --lowerBound AND / OR --upperBound when --change is {category}")
    
if bool_category_modify_filename and (not bool_existing_oldName or not bool_existing_newName):
    raise KeyError(f"Must specify --oldName AND --newName when --change is {category}")
    
if bool_category_modify_filename and (bool_existing_oldPattern or bool_existing_newPattern):
    raise KeyError(f"Must specify NEITHER --oldPattern NOR --newPattern when --change is {category}")
    
if bool_category_add_wildcard and (not bool_existing_newPattern or bool_existing_oldPattern):
    raise KeyError(f"Must specify ONLY --newPattern when --change is {category}")

if bool_category_remove_wildcard and (not bool_existing_oldPattern or bool_existing_newPattern):
    raise KeyError(f"Must specify ONLY --oldPattern when --change is {category}")
    
if bool_category_modify_wildcard and not (bool_existing_oldPattern and bool_existing_newPattern):
    raise KeyError(f"Must specify --oldPattern AND --newPattern when --change is {category}")
    
if (bool_category_add_wildcard or bool_category_remove_wildcard or bool_category_modify_wildcard) and (bool_existing_oldName or bool_existing_newName):
    raise KeyError(f"Must specify NEITHER --oldName NOR --newName when --change is {category}")

# handle IO directories
if not os.path.isdir(args.rulesDir):
    raise NameError(f"{args.rulesDir} does not exist")

if not os.path.isdir(args.outputDir):
    if verbose:
        print(f"[log: Creating {args.outputDir}]")
    os.makedirs(args.outputDir)
    
rules_basenames = os.listdir(args.rulesDir)
rules_paths = [args.rulesDir + x for x in rules_basenames]
dependencies = track_dependencies(rules_paths, rules_basenames, upperBound, lowerBound)

for idx in range(len(dependencies)):
    dependency_path = args.rulesDir + dependencies[idx]
    dependency_basename = dependencies[idx]
    if verbose:
        print(f"[log: Processing {dependency_basename} ]")
    lines, stripped_lines = parse_input(dependency_path)
    if idx > 0:
        prev_dependency_path = args.rulesDir + dependencies[idx-1]
        prev_dependency_basename = dependencies[idx-1]
        prev_input_output_dic = get_input_output([prev_dependency_path], [prev_dependency_basename])[2]
    else:
        prev_input_output_dic = None
    input_output_log_dic = get_input_output_log_dic(stripped_lines, category, prev_input_output_dic, upperBound, verbose, 
                                                    oldPattern = oldPattern, newPattern = newPattern, 
                                                    oldName = oldName, newName = newName)
    lines_updated = update_lines(lines, input_output_log_dic)
    write_rule(lines_updated, args.outputDir, dependency_basename)

new_rules_basenames = os.listdir(args.outputDir)
new_rules_paths = [args.outputDir + x for x in rules_basenames]
new_dependencies = track_dependencies(new_rules_paths, new_rules_basenames, upperBound, lowerBound)

exit_code = 1 - (dependencies == new_dependencies)
exit(exit_code)

# TODO: 
#    {{}} can be wildcards too
#    unittest

# for sort dag and refactor dag: 
#   reuse these functions to detect wildcards and to track changes
#   define the string as a class
#   class DependencyString
#       contains: 
#             wc ranges
#             non wc ranges
#             function to convert
#             function to sort
#             function to refactor
#             function to add, modify and remove in class
