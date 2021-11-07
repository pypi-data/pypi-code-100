import numpy as np
import pandas as pd
import sys
import os

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/data_bn.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.gnrl.sf import *
from aislab.md_fsel.swlogr import *
from aislab.md_reg import *

np.set_printoptions(precision = 15, linewidth = 1e5, threshold = 1e10)
pd.options.display.precision = 15
pd.options.display.max_rows = int(1e20)

# Load data
dat = pd.read_csv(dpath)
x = dat.iloc[:,  :-2].values    # factors /independent variables/
w = c_(dat['w'].values)         # weight
y = c_(dat['y'].values)         # dependent variable
cnames = dat.columns.tolist()[:-2]  # variables names

met = 'SWR' # 'BR' # 'FR' #
mtp = 'empty' # 'full' # 'init' #
ivi = np.arange(1,int(np.floor(x.shape[1] / 3))+1)  # initial ivi - Indexes of Variables In the model

tic()
model = swlogr(x, y, w, cnames=cnames, met=met, mtp=mtp, ivi=ivi, maxiter=100, dsp_op=2)
toc()
