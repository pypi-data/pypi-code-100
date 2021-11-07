import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# sys.path.append('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
# os.chdir('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
# fpathU = 'D:/Lorien/OPEN_MAT/_autoai/data/U.mat'
# fpathY = 'D:/Lorien/OPEN_MAT/_autoai/data/Y.mat'
sys.path.append('/home/user/Desktop/Saso/OPEN_MAT/Project/aislab')
os.chdir('/home/user/Desktop/Saso/OPEN_MAT/Project/aislab')

from aislab.gnrl.sf import *

a = np.array([[1, 0, 1, 0],  # Indexes 0 and 2 == 
            [0, 1, 1, 0],   # Indexes 1 and 2 == 1
            [0, 1, 0, 1],   # Indexes 1 and 3 == 1
            [0, 1, 1, 1]])
ir, ic = find(a, 3, 'last')
print(a)
print('rows:', ir)
print('cols:', ic)

a = np.array([1, 0, 1, 1, 0, 0, 1])
ind = find(a, 3, 'first')
print(a)
print('indexes:', ind)
