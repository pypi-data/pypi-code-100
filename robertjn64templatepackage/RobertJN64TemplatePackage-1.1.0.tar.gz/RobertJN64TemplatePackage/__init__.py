"""
This code here has some functions that we will call in our tests.
"""

import os.path as path


def add(a, b):
    return a + b

def error():
    raise Exception("HELP THIS IS AN ERROR")

def openFile():
    with open(path.dirname(__file__) + '/afile.txt') as f:
        return f.read().strip('\n')

def printTable():
    import tabulate as t
    print(t.tabulate([[1,2,3]], ['a', 'b', 'c']))