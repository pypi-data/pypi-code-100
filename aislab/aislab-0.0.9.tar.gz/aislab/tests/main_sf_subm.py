import numpy as np
import sys
import os

# sys.path.append('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
# os.chdir('D:\\Lorien\\OPEN_MAT\\_autoai_for_git')
sys.path.append('/home/user/Desktop/Saso/OPEN_MAT/_autoai_for_git')
os.chdir('/home/user/Desktop/Saso/OPEN_MAT/_autoai_for_git')
from sf import *

N=10
p = 0.5
x1= rand((N, N))
i = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
j = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
res1 = submat(x1, i, j)

x2 = rand((N, N)).flatten()
i = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
j = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
res2 = submat(x2, i, j)

x3 = rand((N, 1))
i = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
j = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
res3 = submat(x3, i, j)

x4 = rand((1, N))
i = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
j = np.sort(np.random.choice(np.arange(N), int(p*N), replace=False))
res4 = submat(x4, i, j)

# timeit subm(x, i, j)
