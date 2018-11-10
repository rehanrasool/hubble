import numpy as np
import pandas as pd
import json

def phenotype_transfer(file, outputName):
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
    with open(outputName, 'w') as outfile:
        json.dump(data, outfile)

fileName = input('CSV file path: ')
outputName = input('output file name: ')
file = pd.read_csv(fileName)
phenotype_transfer(file, outputName)