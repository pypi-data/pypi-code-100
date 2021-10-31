import os
import sys
import numpy as np
import pandas as pd

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/data_bn0.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.dp_feng.binenc import *
from aislab.gnrl import *

np.set_printoptions(precision=15)
np.set_printoptions(threshold=10000)
np.set_printoptions(linewidth=10000)
pd.options.display.max_rows = int(1e20)

# Data load
dat = pd.read_csv(dpath)
x = dat.iloc[:,:3].values
w = c_(dat.iloc[:,3].values)
y = dat.iloc[:,4:].values

# Data types
xtp = np.array(['num', 'ord', 'nom'])
ytp = np.array(['num', 'bin', 'ord', 'nom'])

ix = [2]
iy = [1]
# iy = [0, 1, 2, 3];

x = c_(x[:, ix])
if len(iy) == 1: y = c_(y[:, iy])
else:            y = y[:, iy];

# UNSUPERVISED BINNING
# hyperparameters for UBinning
par_ub = {}
par_ub['md'] = 100          # desired number of bins (excluding Missing, Other and SpecialValue-s
par_ub['pd'] = 1            # desired percentage of population
par_ub['xtp'] = xtp[ix]     # data type of independent variable
par_ub['ytp'] = ytp[iy]     # data type of dependent variable
par_ub['nmin'] = 50         # minimal number of (weighted) records
par_ub['met'] = 'enr' # 'erv' # 'epp' #     # enr - equal number of records,   erv - equal ranges of values,   epp - equal percentage of population
par_ub['sv'] = [1., 2.]       # special values
if 'ord' in par_ub['xtp']:
    ux = np.unique(x[~np.isnan(x)])
    for i in par_ub['sv']: ux = list(filter(lambda a: a != i, ux))
    par_ub['mt_order'] = ux[::-1]
# UBinning
tic()
ub = ubng(x, par_ub['xtp'], w)
#ub = ubng(x, w, par_ub)  # todo: collect stats for y if needed (staty = True) and skip stbnsy()
print('ubng time: ', toc(0))
# UB stats
tic()
ub = stbnsy(ub, x, y, w, xtp[ix], [ytp[iy]])   # todo: encoding & add info in sb in a separate step
ub_st, ub = stbng('ub', ub, xtp[ix], [ytp[iy]], x, y, w)
print('bng_apl: ', toc(0))

# SUPERVISED BINNING
# hyperparameters for SBinning
par_sb = {}
par_sb['md'] = 5                        # desired number of bins (excluding Missing, Other and SpecialValue-s
par_sb['xtp'] = xtp[ix]                 # data type of independent variable
par_sb['ytp'] = ytp[iy]                 # data type of dependent variable
par_sb['skip_mos'] = ['m', 'o', 'sv']
par_sb['met_dist'] = 'manh' #'eucl'     # distance between clusters in dependant space
par_sb['met'] = 'co1y' # 'hclust' # 'pclust' #
par_sb['nmin_uy'] = [50, 50] # min number of obs in bin per each (ascending ordered) unique value of y
par_sb['mar'] = np.inf
par_sb['pt'] = 0.05
par_sb['ba'] = 0
par_sb['maxprm'] = 20000
par_sb['dGBInd'] = 5;20
par_sb['tolmindGBInd'] = 5
par_sb['mt'] = np.nan
par_sb['minB'] = 50
par_sb['tolminB'] = 20
# SBinning
tic()
[sb, D1] = sbng(ub, xtp[ix], [ytp[iy]])
print('sbng: ', toc(0))
# SB stats
tic()
sb = stbnsy(sb, x, y, w, xtp[ix], [ytp[iy]])              # todo: encoding & add info in sb in a separ_sbate step
sb_st, sb = stbng('sb', sb, xtp[ix], [ytp[iy]], x, y, w)
print('bng_apl: ', toc(0))

# Stats_end
tic()
[n, nw, syy, syy2, wy] = bns2arr(sb)
[x, w] = mdep(syy, nw, wy)
D = dist1(x, w, 'manh', 'ord')[0]
dist = np.append(np.nan, D)
print('stats_end: ', toc(0))


