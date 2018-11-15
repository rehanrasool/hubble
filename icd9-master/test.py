from icd9 import ICD9

# feel free to replace with your path to the json file
tree = ICD9('codes.json')

# list of top level codes (e.g., '001-139', ...)
toplevelnodes = tree.children
toplevelcodes = [node.code for node in toplevelnodes]
print '\n'.join(toplevelcodes)