import numpy as np
import pandas as pd
import sys
import os

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.gnrl.sf import *
from aislab.md_fsel.swlogr import *
from aislab.op_nlopt.cstm import *
from aislab.md_reg import *

np.set_printoptions(precision = 15, linewidth = 1e5, threshold = 1e10)
pd.options.display.precision = 15
pd.options.display.max_rows = int(1e20)

# Generate data
N = 1000
m = 9   # with intercept p = 10
pm = randn((m+1, 1), seed=0)
x = rand((N, m), seed=0)                # factors /independent variables/
w = rand((N, 1), l=0.5, h=2, seed=1)    # weight
y = lgr_apl(np.hstack((ones((N, 1)), x)), pm)                      # dependent variable
cnames = ['var_1', 'var_2', 'var_3', 'var_4', 'var_5', 'var_6', 'var_7', 'var_8', 'var_9']      # variables names

met = 'SWR' # 'BR' # 'FR' #
mtp = 'empty' # 'full' # 'init' #
ivi = np.arange(1,int(np.floor(x.shape[1] / 3))+1)  # initial ivi - Indexes of Variables In the model

tic()
model = swlogr(x, y, w, cnames=cnames, SLE=1, SLS=1, met=met, mtp=mtp, ivi=ivi, maxiter=100, dsp_op=2)
toc()

for i in range(len(model)):   print(model[i]['st']['ovr']['VAF'])

for i in range(len(model)):   print(model[i]['st']['ovr']['AIC'])

spm,_ = sort(pm)
spm1,_ = sort(model[-1]['pm'])
print((spm - spm1)/spm*100)