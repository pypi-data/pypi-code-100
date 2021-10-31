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

# MODEL 1
# Only AR
na = np.full((r, r), 2)
nb = np.full((r, m), 0)
pm0 = c_(np.array([1,1,1,1,1]))
pm1 = lspv(U, Y, na, nb, pm0)
Ym1 = arx_apl(U, Y, pm1, na, nb, pm0)

# MODEL 2
# ARX
na = np.full((r, r), 2)
nb = np.full((r, m), 2)
pm2 = lspv(U, Y, na, nb, pm0)
Ym2 = arx_apl(U, Y, pm2, na, nb, pm0)

# MODEL 3
# roll shifts rows 1 up and duplicates last row
U = np.roll(U, -1, axis=0)
pm3 = lspv(U, Y, na, nb, pm0)
Ym3 = arx_apl(U, Y, pm3, na, nb, pm0)

# MODEL 4
# replaces all negative values with 0
Ym4 = Ym3.clip(min=0)

n = int(np.max([np.max(na), np.max(nb)]))
vaf_model_1 = vaf(Y[n:][:], Ym1)
vaf_model_2 = vaf(Y[n:][:], Ym2)
vaf_model_3 = vaf(Y[n:][:], Ym3)
vaf_model_4 = vaf(Y[n:][:], Ym4)

# plot Y vs Y from Models
for col in range(0,Y.shape[1]):
    title = str('Product '+str(col+1))    
    plt.figure(col)    
    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Sales')
    
    x = range(0,Y.shape[0]-2)
    y_data = Y[:-2,col]
    
    y_mdl_1 = Ym1[:,col]
    y_mdl_2 = Ym2[:,col]
    y_mdl_3 = Ym3[:,col]
    y_mdl_4 = Ym4[:,col]
    
    plt.plot(x,y_data,alpha=0.3)
    plt.plot(x,y_mdl_1)
    plt.plot(x,y_mdl_2)
    plt.plot(x,y_mdl_3)
    plt.plot(x,y_mdl_4)
    
    plt.show()

print('VAF MODEL 1')
for item in vaf_model_1: print(item.round(3), end='\n')
print('\nVAF MODEL 2')
for item in vaf_model_2: print(item.round(3), end='\n')
print('\nVAF MODEL 3')
for item in vaf_model_3: print(item.round(3), end='\n')
print('\nVAF MODEL 4')
for item in vaf_model_4: print(item.round(3), end='\n')

VAF = pd.DataFrame({'M1':vaf_model_1, 'M2':vaf_model_2, 'M3':vaf_model_3, 'M4':vaf_model_4}).values.T
print(VAF)