import numpy as np
import pandas as pd
import sys
import os

# sys.path.append('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
# os.chdir('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
sys.path.append('/home/user/Desktop/Saso/OPEN_MAT/_autoai_for_git')
os.chdir('/home/user/Desktop/Saso/OPEN_MAT/_autoai_for_git')

from sf import *
from md_reg import *

x = rand((100, 5), seed=0)
e = randn((100, 1), seed=0)*0
x = np.hstack((x, c_(x[:,0] + x[:,1]) + e))

res = vif(x)

print(res)