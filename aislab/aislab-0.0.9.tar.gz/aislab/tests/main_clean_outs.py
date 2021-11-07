import sys
import os
import copy
import matplotlib.pyplot as plt

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.gnrl.sf import *
from aislab.gnrl.datgen import *
from aislab.dp_clean.outs import *

# Generate data - x matrix
N = 1000
seed = 10           # seed parameter
rw = (0, 5)         # frequencies range
rfi = (0, 2*np.pi)  # phases range
ra = (30, 100)      # amplitudes range
rc = (0, 500)       # constant components range
se = 0.05           # noise standard deviation
# generates harmonic signals with random parameters and adds noise
x0 = harmnc((N, 1), rw, rfi, ra, rc, se, seed)
print('Original mx:', np.mean(x0))

print('--- MY detection of outliers ---')
# Add >> outliers
x = copy.deepcopy(x0)
ind = [0, 1, 2, 3, 4]; val = max(x0)*3; x[ind] = val
xc, ix = cap(x=x, pc=99, tolp=1)
print('mx_>>outs =', np.mean(x), '    mxc =', np.mean(xc))

# Add << outliers
x = copy.deepcopy(x0)
ind = [0, 1, 2, 3, 4]; val = -min(x0)*3; x[ind] = val
xf, ix = floor(x=x, pc=1, tolp=1)
print('mx_<<outs =', np.mean(x), '    mxf =', np.mean(xf))

# Add >> and << outliers
x = copy.deepcopy(x0)
ind = [0, 1, 2, 3, 4]; val = -min(x0)*3; x[ind] = val
ind = [5, 6, 7, 8, 9]; val =  max(x0)*3; x[ind] = val
xc, ixc = cap(x=x, pc=99, tolp=1)
print('mx_<<>>outs =', np.mean(x), '    mxc =', np.mean(xc))
xf, ixf = floor(x=xc, pc=1, tolp=1)
print('mx_<<>>outs =', np.mean(x), '    mxf =', np.mean(xf))

print('--- STD detection of outliers ---')
# Add >> outliers
ind = [0, 1, 2, 3, 4]; val = max(x0)*3; x[ind] = val
xc, ix = cap(x=x, n=1, tolp=1, met='sdx')
print('mx_outs =', np.mean(x), '    mxc =', np.mean(xc))

plt.plot(x0)
plt.plot(x)
plt.plot(xc)
plt.show()