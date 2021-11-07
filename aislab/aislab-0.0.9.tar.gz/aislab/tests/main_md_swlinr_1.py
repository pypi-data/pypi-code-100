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
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/swlogr/Credissimo_Dataset_GBR_Dum.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.md_fsel.swlinr import *
from aislab.gnrl.sf import *

np.set_printoptions(precision = 15, linewidth = 1e5, threshold = 1e10)
pd.options.display.precision = 15
pd.options.display.max_rows = int(1e20)

# Load data
dat = pd.read_csv(dpath)
x = dat.iloc[:,  :-2].values
w = c_(dat['weight_factor'].values)
y = c_(dat['Good'].values)

cnames = dat.columns.tolist()[:-2]
# cnames = ['var_' + s for s in list(map(str, range(1, x.shape[1] + 1)))]

par = {}
par['cnames'] = cnames
par['s_min'] = 1e-12    # minimum singular value
par['SLE'] = 0.05
par['SLS'] = 0.05
par['pm0'] = 1
par['dsp'] = 'all' # 'no'  # 'ovr'  # 'all'  #
par['crit_nbm'] = ['Fp>4', 'Cp', 'AIC'] # [] #
par['mtp'] = 'full' # 'init' # 'empty' #
par['met'] = 'SWR' # 'BR'  # 'FR' #

par['ivi'] = c_(np.arange(1,int(np.floor(x.shape[1] / 3))+1))
par['val_prc'] = 20 # percent of the data to use for validation (the rest is used for model dev)

tic()
model = swlinr(x, y, w, par)
toc()
