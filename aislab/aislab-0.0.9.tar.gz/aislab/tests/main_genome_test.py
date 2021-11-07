import re
import os
import sys
import numpy as np
import pandas as pd

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.dp_feng.binenc import *
from aislab.gnrl import *

np.set_printoptions(precision=15)
np.set_printoptions(threshold=10000)
np.set_printoptions(linewidth=10000)
pd.options.display.max_rows = int(1e20)

M = int(500000)
N = int(1000)

X = rand((M, N), l=1, h=4, tp='int', seed=0);    x = rand((N, 1), l=1, h=4, tp='int', seed=0).flatten()
tic()
F = N - np.sum(X == x.T, axis=1)
toc()
# M = 500000                      # number of mathes
# N = 1000                        # genome piece length
# Elapsed time: ~ 1 second
# L = 5e11 = M*1e6
# => 1e6 sec = 278 h - single thread
# => ~3h per x --> 100 threads
# => ~3e6h all x-es

# L = int(M*N)
# X = rand((L,), l=1, h=4, tp='int', seed=0);    x = rand((N, 1), l=1, h=4, tp='int', seed=0).flatten()
# tic()
# F = N - np.sum(hnkl(X, N) == x.T, axis=1)
# toc()
# # M = int(200)
# # N = int(1000)
# # Elapsed time: 2.923557 seconds.


sF, iF = sort(F)
bestF = sF[:100]
bestInd = iF[:100]


# M = 700000                      # number of mathes
# N = 1000                        # genome piece length


