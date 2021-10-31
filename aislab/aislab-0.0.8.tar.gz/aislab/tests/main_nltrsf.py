import numpy as np
import os
import sys

# sys.path.append('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
# os.chdir('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
sys.path.append('/home/user/Desktop/Saso/OPEN_MAT/_autoai_for_git')
os.chdir('/home/user/Desktop/Saso/OPEN_MAT/_autoai_for_git')

from sf import *
from dp_proc import *

# Generate data
N = 1000
x = rand((N,1), l=0, h=3, seed=0)
y = c_(np.log(1 + x)) + randn((N,1), m=0, s=0.2, seed=0)

tr = ['pow2', 'pow3', 'sqrt', 'rcpr', 'log']

crit = 'pears'
tfmdl = nltrsf(x, y, tr, crit)
xt = tfmdl['xt']


print(np.hstack((tfmdl['tr_all'], tfmdl['crt_all'])))
print('Best:', np.hstack((tfmdl['tr_best'], tfmdl['crt_best'])))

print('Pearson(xt, x):', np.corrcoef(xt.T, y.T)[0,1])