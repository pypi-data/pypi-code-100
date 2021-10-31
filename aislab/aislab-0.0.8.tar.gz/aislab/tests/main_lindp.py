"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import os
import sys

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'

sys.path.append(wpath)
os.chdir(wpath)

from aislab.gnrl.sf import *

N = 10
X1 = rand((N, 7), tp='int', seed=0)
X1 = np.array([[ 1,  2,  3,  4,   5,  6,  7,  8,  9,  10],
               [ 2,  4,  6,  8,  10,  2,  4,  6,  8,  10],
               [ 3,  6,  3,  6,   3,  6,  3,  6,  3,   6],
               [ 1, -2,  3, -4,   5, -6,  7, -8,  9, -10],
               [-2,  4, -6,  8, -10,  2, -4,  6, -8,  10],
               [ 3, -6,  3, -6,   3, -6,  3, -6,  3,  -6],
               [ 3,  6, -3, -6,   3,  6, -3, -6,  3,   6]]).T
X2 = X1[:,:3]*0.5
X = np.hstack((X1[:,:3], X2, X1[:,3:]))

Xnld, ld, nld = lindp(X)

print('Linearly dependent columns:', ld)
print('Linearly independent columns:', nld)

# Check for linearly dependence in Xnld
Xnld2, ld2, nld2 = lindp(Xnld)
print('Check for linearly dependence in Xnld')
print('Linearly dependent columns:', ld2)
print('Linearly independent columns:', nld2)
