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

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/reg/data_reg2.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.md_reg.linest import *
# from aislab.gnrl.bf import *


dat = pd.read_csv(dpath, header=None).to_numpy()
U = dat[:, :-5]
Y = dat[:,-5:]

# shortening Y columns (only first two remain) - to reduce log size
Y = np.delete(Y, [2, 3, 4], axis=1)
# enter outliers: multiply first 10 elements in first column by 50
a = 10
Y[0:a, 0] = Y[0:a, 0] * 50

N, r = Y.shape
m = U.shape[1]

# MODEL 1
na = 2
nb = 2
nc = 2
pm0 = 0
Pm1 = lspm(U, Y, na, nb, pm0, na=na, pm0=pm0)
Ym1 = lspm_apl(U, Y, Pm1, na=na, pm0=pm0)

# MODEL 2 RobLS
maxiter = 100
dvaf = 1e-6
hst = 1
mdl2 = roblspm(U, Y, na, nb, pm0, maxiter, dvaf, hst)
Pm = mdl2['Pm']
VAFW = mdl2['st']['vafw']
VAF = mdl2['st']['vaf0']
Ym2 = lspm_apl(U, Y, mdl2)

n = max(na, nb)
vaf_model_1 = vaf(Y[a + n:][:], Ym1[a:][:])
vaf_model_2 = vaf(Y[a + n:][:], Ym2[a:][:])
print('VAF MODEL 1')
print(c_(vaf_model_1))
print('VAF MODEL 2')
print(c_(vaf_model_2))

# for item in vaf_model_2:
#    print ("--",item.round(3),"--",end='\n')
#    
## ADDITIONAL PLOT
#    plt.title('RED = SALES, GREEN = ITERATIONS OF PM, \n\
#              BLUE = MODEL 1, PURPLE = MODEL 2 (ROB_LS)')
#    plt.xlabel('Days')
#    plt.ylabel('Sales')
#    # plots each iteration of PM
#    h = Pm.shape[1]
#    for i in range(0,h):
#        Ymi = dv2dm(mdl_YM[:,i],r)
#        Ymi = Ymi[a+1:,:]
#        plt.plot(Ymi, 'g',antialiased=True,linewidth = 0.5, alpha = 1)
#    # plots Y
#    Y_to_plot = Y[a+n:,:]
#    plt.plot(Y_to_plot, 'r', antialiased = True, linewidth = 0.8)
#    # plots Ym1
#    Ym1_to_plot = Ym1[a:,:]
#    plt.plot(Ym1_to_plot, 'b', antialiased = True, 
#             linewidth = 3, alpha = 0.2)
#    # plots Ym2
#    Ym2_to_plot = Ym2[a:,:]
#    plt.plot(Ym2_to_plot, 'm', antialiased = True, 
#             linewidth = 3, alpha = 0.5)
#  
#    plt.show()
