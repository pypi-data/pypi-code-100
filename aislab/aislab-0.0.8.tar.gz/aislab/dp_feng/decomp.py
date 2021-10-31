"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from aislab.gnrl.sf import *
####################################################################################
# def trnd():
####################################################################################
def permdl(x, T=7, Ne=None):
    T = int(T)
    N = len(x)
    n = np.floor(N/T).astype(int)
    S = x[:n*T].reshape(n, T)
    if N > n*T:
        ss = np.empty((1, np.ceil(N/T).astype(int)*T - N))
        ss[:] = np.nan
        S = np.vstack((S, np.hstack((x[n*T:].T, ss))))
    pm = np.nanmean(S, axis=0)
    ind = T if len(x) % T == 0 else len(x) % T
    pm = np.roll(pm, -ind)
    return pm
####################################################################################
# 	T determination = f(Rxx), f(fft), ...
