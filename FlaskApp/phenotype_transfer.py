import numpy as np
import pandas as pd
import json
import glob
import os

def phenotype_transfer(file, outputName=None):
    data = {}
    fileName= file.columns[1]
    data[fileName] = {}
    for i in range(len(file.values)):
        keyName = file.values[i][0]
        values = []
        iterate = 1
        while iterate < len(file.columns.values) and not pd.isnull(file.iloc[i,iterate]):
            values.append(file.values[i][iterate])
            iterate+=1
        data[fileName][keyName] = values
    # with open(outputName, 'w') as outfile:
    # return json.dump(data, outfile)
    return json.dumps(data)

# fileName = input('CSV file path: ')
# outputName = input('output file name: ')
# file = pd.read_csv(fileName)
# phenotype_transfer(file, outputName)

def find_phenotype(phenotype):
    print("looking for: %s" % phenotype)
    path = "phenotypes/"
    files = os.listdir(path)
    output = []
    for file in files:
        read_file = pd.read_csv(path + file)
        result = phenotype_transfer(read_file)
        print(result)
        output.append(result) # TODO use phenotype
    return output

# find_phenotype("asthma")
