import os
import sys
import numpy as np
import pandas as pd

# wpath = '/home/.../binning'
# dpath = '/home/.../binning/data_bn1.csv'
wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/data_bn1.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.dp_feng.binenc import *
from aislab.gnrl import *


# Data load
dat = pd.read_csv(dpath)
x = dat.iloc[:,:3].values
w = c_(dat.iloc[:,3].values)
y = dat.iloc[:,4:].values

# Data types
xtp = np.array(['num', 'ord', 'nom'])
ytp = np.array(['num', 'bin', 'ord', 'nom'])

ix = [1]
iy = [1]
#iy = [0, 1, 2, 3]

x = c_(x[:, ix])
if len(iy) == 1: y = c_(y[:, iy])
else:            y = y[:, iy];
xtp = xtp[ix]
ytp = ytp[iy]

# UNSUPERVISED BINNING
# hyperparameters for UBinning
# md - desired number of bins (excluding Missing, Other and SpecialValue-s
# pd - desired percentage of population
# xtp - data type of independent variable
# ytp - data type of dependent variable
# nmin - minimal number of (weighted) records
# met - enr - equal number of records,   erv - equal ranges of values,   epp - equal percentage of population
# sv - special values
# if xtp == 'ord':
#     sv = [1., 2.]  # special values
#     ux = np.unique(x[~np.isnan(x)])
#     for i in sv: ux = list(filter(lambda a: a != i, ux))
#     mt_order = ux[::-1]
# else:
#     mt_order = []

tic()
ub = ubng(x, xtp, w, y=y, ytp=ytp)
print('ubng time: ', toc(0))

# SUPERVISED BINNING
# hyperparameters for SBinning
# md - desired number of bins (excluding Missing, Other and SpecialValue-s
# xtp - data type of independent variable
# ytp - data type of dependent variable
# skip_mos - ['m', 'o', 'sv']
# met_dist - 'manh', 'eucl' - distance between clusters in dependant space
# met - 'co1y', 'hclust', 'pclust'
# nmin_uy - min number of obs in bin per each (ascending ordered) unique value of y
# mar
# pt
# ba
# maxprm
# dGBInd
# tolmindGBInd
# mt
# minB
# tolminB

tic()
sb, D1 = sbng(ub, xtp, ytp)
print('sbng: ', toc(0))

# Stats_end
tic()
n, nw, syy, syy2, wy = bns2arr(sb)
print('stats_end: ', toc(0))

my = syy.flatten()/nw.flatten()
df = pd.DataFrame({'n':n.flatten(), 'nw':nw.flatten(), 'sy':syy.flatten(), 'my':my})
print(df)

xe = enc_apl(sb, x, xtp, 'dv')
