import os
import sys
# import numpy as np
import matplotlib.pyplot as plt

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
sys.path.append(wpath)
os.chdir(wpath)

import matplotlib.pyplot as plt
from aislab.gnrl.measr import *

N = 1000
#x = c_(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
x = randn((N, 1), seed=0)*100
R = corf(x)
C = covf(x)
fig, axs = plt.subplots(2)
fig.suptitle('Auto correlation and covariance function')
axs[0].plot(np.arange(N+1), R)
axs[1].plot(np.arange(N+1), C)
