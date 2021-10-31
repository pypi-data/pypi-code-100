import os
import sys
# import numpy as np
import matplotlib.pyplot as plt

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.dp_clean.miss import *
from aislab.gnrl.datgen import *
from aislab.gnrl.sf import *

# Generate data - x matrix
N = 100
m = 10
nna = m*10          # number of nan-s
seed = 10           # seed parameter
rw = (0, 5)         # frequencies range
rfi = (0, 2*np.pi)  # phases range
ra = (30, 100)      # amplitudes range
rc = (0, 500)       # constant components range
se = 0.05           # noise standard deviation
# generates harmonic signals with random parameters and adds noise
x = harmnc((N, m-1), rw, rfi, ra, rc, se, seed)
# introduce partial dependence between columns in x
pm = rand((m-1, 1), l=-1, h=1, seed=0)
xx = x@pm
e = randn((N, 1), 0, 1, seed=seed)*np.std(xx)*se
xx = xx + e
x = np.hstack((x, xx))
print('mx - without nans:', np.mean(x, axis=0))
# Add nan-s
rrows = [rand((nna,), 0, N-1, tp='int', seed=0)]
rcols = [rand((nna,), 0, m-1, tp='int', seed=0)]
ix0 = np.hstack((rrows, rcols))
# plt.plot(x)
x0 = copy.deepcopy(x)
x[rrows, rcols] = np.nan # insert randomly 100 nan-s in x
print('na_count:', np.count_nonzero(np.isnan(x)))

x1, ix1 = filconst(x, met='mean')
x2, ix2 = filmdl(x)

# After filmdl()
plt.plot(x1)
plt.plot(x2)
plt.plot(x)
plt.show()
ii = 0
dx_mean = x0[:, ii] - x1[:, ii]
dx_mdl = x0[:, ii] - x2[:, ii]
# plt.plot(dx_mean)
# plt.plot(dx_mdl)
# print('x - x_mx: ', dx_mean)
# print('x - x_mdl: ', dx_mdl)

print('na_count:', np.count_nonzero(np.isnan(x1)))
print('SSdx_mean:', np.std(dx_mean, axis=0))
print('SSdx_mdl:', np.std(dx_mdl, axis=0))

