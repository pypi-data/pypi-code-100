from numpy.matlib import repmat
from collections import defaultdict
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'

sys.path.append(wpath)
os.chdir(wpath)

from aislab.gnrl.sf import *
from aislab.md_reg.linest import *
from aislab.md_reg.rreg import *
from aislab.dp_feng.normlz import stdn

# Number of observations
N = 1600
m = 2
r = 2
pm0 = np.zeros((r, 1))
na = ones((r, r))*2
nb = ones((r, m))*2

num = np.array([0, 0.25, -0.75])        # autoregressions
num1 = num + np.array([0, 0.3, 0.3])    # autoregressions
den = np.array([1, -0.4, 0.6])          # exogenous inputs
den1 = den + np.array([0, 0.3, 0.3])    # exogenous inputs

v1 = np.reshape(np.hstack([np.tile(den[1:], r*r), np.tile(num[1:], r*m)]), (2*r*r + 2*r*m, 1))
v2 = np.reshape(np.hstack([np.tile(den1[1:], r*r), np.tile(num1[1:], r*m)]), (2*r*r + 2*r*m, 1))
ps = np.hstack([v1 @ np.ones((1, 200)), v2 @ np.ones((1, 200))])
ps = np.tile(ps, 4)                     # time-varying behavior
# ps = np.repmat(ps(:, 1), 1, N)        # time-invariant behavior
z = ps.shape[0]


# ------ Congiguration parameters ------
pm0 = np.zeros((r, 1))
par0 = {'na': na, 'nb': nb}#, 'pm0': pm0}
# par = {'mod': 'non'}
# par = {'mod': 'pdm', 'trPmin': 1e-0, 's': 1}
# par = {'mod': 'ctr', 'trP': 4}
# par = {'mod': 'ccm', 'P': np.diag([0.5, 0.5, 0.5, 0.5])}
# par = {'mod': 'cff', 'rc': repmat(0.95, r, 1)}
par = {'mod': 'vff', 'Ne': 10, 'se': repmat(0.1, r, 1), 'rvmin': repmat(0.5, r, 1), 'rv': repmat(1, r, 1), 'me1': [], 'ee': []}

par = {**par0, **par}

# ------ Data Generation ------
np.random.randn(1)
U = np.random.uniform(size=(N, m))
np.random.randn(2)
E, st = stdn(np.random.randn(N, r))
E = E * 0.05
nn = np.max(np.hstack((na, nb)))
Y = arx_apl(U, Y=None, pm=ps, na=na, nb=nb, pm0=pm0, sim=True, ltv=True, E=E)

# ------ Initial Conditions ------
pm = np.zeros((z, N))
P = 1e1 * np.eye(len(pm))
trp = np.zeros((N - nn + 2))

# ------ Parameters Estimation ------
for k in range(nn, N):
    pmk, P, par = rls(U[k-nn:k+1, :], Y[k-nn:k+1, :], pm[:, k-1], P, par)
    pm[:, k] = pmk.flatten()
    trp[k] = np.trace(P)

# ------ Visualization ------
plt.plot(ps.T)
plt.plot(pm.T)
#plt.plot(trp)

Ym = np.zeros((N, r))
for k in range(nn, N):
    Fi = dmpv(U[k-nn:k+1, :], Y[k-nn:k+1, :], par=par)
    Ym[k, :] = (Fi@c_(pm[:, k])).T

VAF = vaf(Y, Ym)
print(c_(VAF))

plt.plot(Y)
plt.plot(Ym)
plt.show()

yy = np.hstack((c_(Y[:100,0]), c_(Ym[:100,0])))
pp = np.hstack((c_(ps[1,:]), c_(pm[1,:])))
