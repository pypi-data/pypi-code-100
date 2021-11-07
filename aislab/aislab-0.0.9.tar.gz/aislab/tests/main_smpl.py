import numpy as np
import pandas as pd
import os
import time

import sys
sys.path.append('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
os.chdir('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')

from sf import *
from dp_smpl import *

# Load data
import scipy.io as spio
dat = spio.loadmat('D:/Lorien/OPEN_MAT/_autoai/data/data_bn0.mat', squeeze_me=True)
x = dat['x']
y = dat['y'][:, 1]
w = dat['w']

N = x.shape[0]
x = np.hstack((x, rand((N, 1), 1, 5, tp='int', seed=0) + 3))
x = np.hstack((x, rand((N, 1), 1, 2, tp='int', seed=0) - 10))
x = np.hstack((x, rand((N, 1), 1, 3, tp='int', seed=0)*2))

#x1 = smplrnd(x)
x1 = smplrnd(x, 20, seed=0)
print(N, x1.shape[0], round(x1.shape[0]/N*100, 2))

###############################################################################
xk = [3, 4]
prc = [100, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#xk = [3, 4, 5]
#prc = [100, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 20, 30, 40, 50, 60, 70, 80, 90, 100]
xs, ws = smplstr(x, prc, xk, seed=0)

# Checkout the result
uxk = {}
ni = np.full((len(xk), 1), np.nan)
h = 0
for i in xk: 
    uxk[h] = np.unique(x[:,i])
    ni[h] = len(uxk[h])
    h += 1
    
mk = len(xk)
Ni = np.full((int(np.prod(ni)), 1), np.nan)
Nsi = np.full((int(np.prod(ni)), 1), np.nan)
sk = np.empty([0,len(xk)])
s = strata(uxk, sk, 0, len(xk))
h = 0
for si in range(len(s)):
    c1 = np.full((x.shape[0],1), True)
    c2 = np.full((xs.shape[0],1), True)
    i = 0
    for sii in s[si,:]:
        c1 = c1 & c_(x[:,xk[i]]==sii)
        c2 = c2 & c_(xs[:,xk[i]]==sii)
        i += 1
    Ni[h] =  sum(c1)
    Nsi[h] =  sum(c2)
    h += 1
print(s)
print(np.hstack((Ni, Nsi, np.round(Nsi/Ni*100, 2))))
###############################################################################
met = 'rand' # 'syst'# 'strat' # 'cnn' # 'enn'
xs, ws = usmpl(x, met=met, prc=10, seed=0)
print(N, xs.shape[0], round(xs.shape[0]/N*100, 2))

met = 'strat'
xk = [3, 4, 5]
prc = [100, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 20, 30, 40, 50, 60, 70, 80, 90, 100, 100, 20, 30, 40, 50, 60, 70, 80, 90, 100]
xs, ws = usmpl(x, met=met, prc=prc, ixk=xk, seed=0)

# Checkout the result
uxk = {}
ni = np.full((len(xk), 1), np.nan)
h = 0
for i in xk: 
    uxk[h] = np.unique(x[:,i])
    ni[h] = len(uxk[h])
    h += 1
    
mk = len(xk)
Ni = np.full((int(np.prod(ni)), 1), np.nan)
Nsi = np.full((int(np.prod(ni)), 1), np.nan)
sk = np.empty([0,len(xk)])
s = strata(uxk, sk, 0, len(xk))
h = 0
for si in range(len(s)):
    c1 = np.full((x.shape[0],1), True)
    c2 = np.full((xs.shape[0],1), True)
    i = 0
    for sii in s[si,:]:
        c1 = c1 & c_(x[:,xk[i]]==sii)
        c2 = c2 & c_(xs[:,xk[i]]==sii)
        i += 1
    Ni[h] =  sum(c1)
    Nsi[h] =  sum(c2)
    h += 1
print(s)
print(np.hstack((Ni, Nsi, np.round(Nsi/Ni*100, 2))))
