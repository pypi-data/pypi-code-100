import numpy as np
import math
from numpy.lib.npyio import genfromtxt
import pandas as pd
import runpy
import os
import time

def Matrix(rows, cols):
    matrix = np.zeros((rows, cols))
    return matrix

def Clear():
    os.system('cls')

def MatrixRandom(matrix, floor, roof, style="float", decimals=3):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if style == "float":
                matrix[x][y] = np.random.uniform(floor,roof)
            if style == "int": 
                matrix[x][y] = np.random.randint(floor,roof)
    return matrix.round(decimals)

def printify(nparray, title="Matrix", indent=5, linespacing=0, coordinates=False):
    print(f"\n{title}\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for x in range(len(nparray)):
        printrow = [f"Row: {x}", indent*(" ")]
        for y in range(len(nparray[x])):
            if coordinates:
                printrow.append(f'{x}.{y}: ')
            printrow.append(nparray[x][y])
            for _ in range(indent-(len(list(str(nparray[x][y]))))):
                printrow.append("")
        print(str(printrow).replace("[","").replace("]","").replace("'","").replace(",",""), linespacing*"\n")

def toPandas(inarray):
    result = pd.DataFrame(inarray)
    return result

def toNumpy(inarray):
    if isinstance(inarray, pd.DataFrame):
        result = inarray.to_numpy()
        return result
    else:
        result = np.array(inarray)
        return result

def writeCSV(matrix, filename):
    np.savetxt(filename, matrix, delimiter=",")

def readCSV(filename):
    return genfromtxt(filename, delimiter=',')

def sigmoid(x):
    sig = 1 / (1 + math.exp(-x))
    return sig

def dsigmoid(y):
    dsigmoid = y * (1-y)
    return dsigmoid