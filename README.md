![image](snaketrack_logo.png)

# Welcome to Snaketrack!

Snaketrack is a python-based tool to track and propagate changes to filenames in snakemake DAGs and to refactor the filenames structure, in order to keep your DAG nice and tidy!

## Functionalities:
- Propagate the addition, removal or modification of wildcards in a snakemake DAG
- Safely modify filenames without breakage of wildcards
- Sorting wildcards alphabetically
- Keeping filenames tidy and wildcards-only

## How to Install:

## How to Use:

The general structure of a snaketrack command is the following:

```
python3 scripts/main.py \ 
    --rulesDir rulesDir \
    --outputDir outputDir \ 
    --category category \
    [--oldPattern oldPattern] \
    [--newPattern newPattern] \
    [--oldName old Name] \
    [--newName newName] \
    [--lowerBound lowerBound] \
    [--upperBound upperBound] \
    [--verbose]
```

Where:
- **rulesDir** is the folder in which snakemake rules are deposited
- **outputDir** is the folder in which to write the modified rules (will be created if non-existing)
- **category** is the type of change to apply to the DAG.
- **oldPattern** is the wildcard to remove / modify
- **newPattern** is the wildcard to add / the modified version of the wildcard
- **oldName** is the filename to modify
- **newName** is the modifed version of the filename

You can choose among 4 different categories:
- **add_wildcard**
```
python3 scripts/main.py \ 
    --rulesDir rulesDir \
    --outputDir outputDir \            
    --category add_wildcard \
    --newPattern newPattern \
    [--lowerBound lowerBound] \
    [--upperBound upperBound] \
    [--verbose]
```
- **remove_wildcard**
```
python3 scripts/main.py \ 
    --rulesDir rulesDir \
    --outputDir outputDir \            
    --category remove_wildcard \
    --oldPattern oldPattern \
    [--lowerBound lowerBound] \
    [--upperBound upperBound] \
    [--verbose]
```
- **modify_wildcard**
```
python3 scripts/main.py \ 
    --rulesDir rulesDir \
    --outputDir outputDir \            
    --category modify_wildcard \
    --oldPattern oldPattern \
    --newPattern newPattern \
    [--lowerBound lowerBound] \
    [--upperBound upperBound] \
    [--verbose]
```
- **modify_filename**
```
python3 scripts/main.py \ 
    --rulesDir rulesDir \
    --outputDir outputDir \            
    --category modify_filename \
    --oldName old Name \
    --newName newName \
    [--verbose]
```




