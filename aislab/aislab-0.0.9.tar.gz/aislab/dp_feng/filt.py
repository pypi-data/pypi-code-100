"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from aislab.gnrl.sf import *

## filtering
# fltlp():
# flthp():
# fltbr():

#def fltgauss(X, n=None, z=None, mod=None):
#    # Gaussian weights filter - for standard normal distribution
#    # X - data(matrix)
#    # n - affects the number of filter parameters: p = 2 n + 1
#    # z - affects the values pf filter parameters
#    #
#    # --------------------------------------
#    # Author: Alexander Efremov
#    # Course: Multivariable Control Systems
#    # Date: 14 Jul 2004
#    # --------------------------------------
#
#    if np.array(mod).size == 0: mod = '2side'
#    if len(X.shape) == 1:
#        N = X.shape[0]
#        m = 1
#        X = X.reshape(N, 1)
#    elif len(X.shape) == 2:
#        N, m = X.shape
#
#    if np.array(n).size == 0:
#        n = np.round(min(0.9*N, 2*N**0.5))
#        if np.remainder(n, 2) == 0: n = n + 1
#    if np.size(z) == 0: z = 3
#
#    if n is not None:
#        a = np.arange(int(-n), int(n))*(z / int(n))
#        a = a.reshape(126, 1)
#    else:
#        a = 1
#    p = np.exp(-0.5*a**2) / (2*np.pi)
#    p = p / sum(p)
#    p = p.reshape(int(2*n), 1)
#    y = np.zeros((N, m))
#
#    if mod == 'left':
#        p = p[1:int(n)]/np.sum(p[1:int(n)])
#        X = [np.tile(np.mean(X[1:int(n), :]), int(n), 1, X)]
#        ind = np.transpose(1, N)*np.ones(1, n) + np.ones(N, 1)*np.array([0, n - 1])
#        for j in range(1, m):  y[:, j] = X[ind + (j - 1)*(N + n)]*p
##    elif mod == 'right':
##        p = p[int(n) + 1:-1]
##        X = X, np.matlib.repmat(np.mean(X[len(X) - int(n) + 1: -1, :]), int(n), 1)
##        ind = np.transpose(1, N)*np.ones(1, int(n)) + np.ones(N, 1)*np.array([0, int(n) - 1])
##        for j in range(1, m):  y[:, j] = X[ind + (j - 1)*(N + n)]*p
#    elif mod == '2side':
#        xx = np.zeros((int(X.shape[0] + (2*n)), X.shape[1]))
#        xx[:int(n), :] = np.tile(X[:int(n), :].mean(axis=0), (int(n), 1))
#        xx[int(n):int(-n), :] = X
#        xx[int(-n):, :] = np.tile(X[int(-n):, :].mean(axis=0), (int(n), 1))
#        X = xx
#        l = np.arange(0, N)
#        ll = np.ones(l.shape[0], dtype=int)
#        ll = ll*l
#        ll = np.transpose([ll])
#        b = np.arange(1, 2*n + 1)
#        nn = np.ones(b.shape[0], dtype=int)
#        nn = nn*b
#        nn = nn + ll
#        ind = nn
#        ind = np.array(ind, dtype=int)
#        for j in range(0, m):
#            y[:] = np.dot((X[ind + (j - 1)*(N + 2*int(n))]).reshape(1000, 126), p)
#
#    return y, p
#######################################################################################
# mavg
# def fltma(X, n=1, pm=np.ones((1, 1))):
def fltma(x, n=np.nan, w=np.ones((0, 0))):
    if np.isnan(n) and w.size == 0: 
        print("In MAVG(): Window size n or weights w not provided...")
        return None
    if w.size == 0: w = np.ones((n, 1))
    N = len(x)
    x = x.reshape(-1, 1)
    w = w.reshape(-1, 1)
    if n < 2: n = 2
    if N < n:
        xt = x.T@w[:N]/max(1e-12, np.sum(w[:N]))
    else:
        X = hnkl(x, n)
        xt = X@w/max(1e-12, np.sum(w))
    return xt

###################################################################################
# other filters: 	low-pass, high-pass, reject. filters...
# 			iir (infinite impulse response), fir (finite impulse response)
#                      ...


