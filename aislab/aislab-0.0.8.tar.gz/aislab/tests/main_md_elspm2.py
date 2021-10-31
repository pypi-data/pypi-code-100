"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'


sys.path.append(wpath)
os.chdir(wpath)

from aislab.md_reg.linest import *
from aislab.gnrl.sf import *
from aislab.gnrl.bf import *

# Data Generation
N=100
m = 2
r = 1
pm0 = np.zeros((r, 1))
na = ones((r, r))*2
nb = ones((r, m))*2
nc = ones((r, r))*2

bi = np.array([ 0.25, -0.75])   # autoregression
ai = np.array([-0.4,   0.1 ])   # exogenous inputs
ci = np.array([ 0.6,  -0.2 ])   # MA residuals

pab = np.hstack((np.tile(ai, r), np.tile(bi, m)))
pab = c_(np.tile(pab, r))
# ------ Data Generation ------
U = rand((N, m), seed=0)
Y = arx_apl(U, Y=None, pm=pab, na=na, nb=nb, pm0=pm0, sim=True)
se = np.std(Y)
E = randn((N, r), m=0, s=se, seed=0)
pc = np.tile(ci, m)
pc = c_(np.tile(pc, r))
ps = np.vstack((pab, pc))
Y = armax_apl(U, Y=None, E=E, pm=ps, na=na, nb=nb, nc=nc, pm0=pm0, sim=True)

N, r = Y.shape
m = U.shape[1]

# MODEL ARX
na = 2
nb = 2
nc = 2
pm0 = 0
Pm1 = lspm(U, Y, na, nb, pm0)
Ym1 = arx_apl(U, Y, Pm1, na, nb, pm0)

Pmc = np.zeros((r*nc, r))
Pm = np.vstack((Pm1, Pmc))
n = int(max((na, nb)))

# MODEL ARMAX
opt_maxiter = 50
opt_taux = 1e-6
opt_tauf = 1e-6
opt_dsp = 0
# the list contains the matrix E and a vector Pm
Pm2, E = elspm(U, Y, na, nb, nc, pm0)
Ym2 = armax_apl(U, Y, E, Pm2, na, nb, nc, pm0)

vaf_model_1 = vaf( Y[n:][:], Ym1)
vaf_model_2 = vaf( Y[n:][:], Ym2)

# plot Y vs Y from Models
for col in range(0, Y.shape[1]):
    title = str('model out ' + str(col + 1))
    plt.figure(col)
    plt.title(title)
    plt.xlabel('time')
    plt.ylabel('y')

    x = range(0, Y.shape[0] - 2)
    y_data = Y[n:, col]

    y_mdl_1 = Ym1[:, col]
    y_mdl_2 = Ym2[:, col]

    plt.plot(x, y_data, alpha=0.3)
    plt.plot(x, y_mdl_1)
    plt.plot(x, y_mdl_2)
    plt.show()

print('VAF MODEL: ARX')
for item in vaf_model_1: print(item.round(3), end='\n')
print('\nVAF MODEL: ARMAX')
for item in vaf_model_2: print(item.round(3), end='\n')
