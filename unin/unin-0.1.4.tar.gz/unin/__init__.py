#imports essential functions from the vandal package.
from vandal.misc.global_functions import *
from vandal import hub, eoq, montecarlo
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import datetime
import math

import os, fnmatch
def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

findReplace('vandal', 'vandal', 'unin', '*.py')