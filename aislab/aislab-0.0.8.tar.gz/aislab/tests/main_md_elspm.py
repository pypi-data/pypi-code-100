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
dpathU = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/reg/U.csv'
dpathY = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/reg/Y.csv'

sys.path.append(wpath)
os.chdir(wpath)

from aislab.md_reg.linest import *
from aislab.gnrl.sf import *

U = pd.read_csv(dpathU, header=None).to_numpy()
Y = pd.read_csv(dpathY, header=None).to_numpy()

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
    title = str('Product ' + str(col + 1))
    plt.figure(col)
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Sales')

    x = range(0, Y.shape[0] - 2)
    y_data = Y[:-2, col]

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
