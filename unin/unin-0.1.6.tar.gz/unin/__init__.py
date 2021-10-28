#imports essential functions from the vandal package.
from vandal.misc.global_functions import *
from vandal import hub, eoq, montecarlo
#imports functions and modules from other public packages.
import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import datetime
import math
import os,re

#replace 'vandal' in text with 'unin' where is appears in the vandal module files.
files = os.path.abspath(eoq.__file__), os.path.abspath(hub.__file__), os.path.abspath(montecarlo.__file__) 

for file in files:
    open_file = open(file,'r')
    read_file = open_file.read()
    regex = re.compile('vandal')
    read_file = regex.sub('unin', read_file)
    write_file = open(file,'w')
    write_file.write(read_file)