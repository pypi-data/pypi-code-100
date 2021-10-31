# S T E P W I S E   L I N E A R  R E G R E S S I O N
#--------------------------------------
# Author: Alexander Efremov
# Date:   05.09.2009
# Course: Multivariable Control Systems
#--------------------------------------

import numpy as np
import pandas as pd
import sys
import os

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/data_bn.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.md_fsel.swlinr import *
from aislab.gnrl.sf import *
from aislab.dp_clean import filmdl

np.set_printoptions(precision = 15, linewidth = 1e5, threshold = 1e10)
pd.options.display.precision = 15
pd.options.display.max_rows = int(1e20)

# Load data
dat = pd.read_csv(dpath)
x = dat.iloc[:,:274].values
w = c_(dat.iloc[:,274].values)
y = c_(dat.iloc[:,275].values)
cnames = dat.columns.tolist()[:274]

cnd = np.sum(x, axis=0) < np.sum(1 - x, axis=0)
ss = np.sum(x, axis=0)*cnd + np.sum(1 - x, axis=0)*(1 - cnd)
# x = x[:, :9]

par = {}
par['cnames'] = cnames
par['s_min'] = 1e-12    # minimum singular value
par['SLE'] = 0.05
par['SLS'] = 0.05
par['pm0'] = 1
par['dsp'] = 'all'      #'no'; 'ovr'; 'all';
par['crit_nbm'] = ['Cp', 'AIC'] # [] #
par['mtp'] =  'init' # 'empty' # 'full' #
par['met'] = 'SWR' # 'BR' # 'FR' #
par['ivi'] = c_(np.array([])).astype(int)
par['val_prc'] = 0
# par['ivi'] = c_(np.arange(1,int(np.floor(x.shape[1] / 3))+1))
#par.nbm_crit = np.array([])

tic()
model = swlinr(x, y, w, par)
toc()

# met = 'SWR'
# mtp = 'init'
# ivi = c_(np.array([])).astype(int)
# tic()
# model = swlinr(x, y, w, cnames=cnames, met=met, mtp=mtp, ivi=ivi)
# toc()
