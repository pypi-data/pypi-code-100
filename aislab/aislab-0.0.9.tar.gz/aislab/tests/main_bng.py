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

#N = 10000
#np.random.seed(10)
#ux = np.array([13])
#np.random.seed(10)
#r1 = np.random.random(N)
#x = np.reshape(np.round(1 + r1*(ux[0] - 1)), (N,1))
## x[0:round(0.4*N)] =  1e10 # np.nan
#np.random.seed(0)
#y1 = x/np.std(x[~np.isnan(x)]) + np.round(np.random.random((N, 1)), 2)
#np.random.seed(2)
#y2 = np.random.randint(2, size=(N,1))
#np.random.seed(3)
#y3 = np.random.randint(11, size=(N,1))
#np.random.seed(4)
#y4 = np.random.randint(604, size=(N,1))
#y = np.column_stack((y1,y2,y3,y4))
#w = np.full((N,1), 5.)
#ytp = ['num','bin','ord','nom']
#SV = []

#import scipy.io as spio
#dat = spio.loadmat('D:/Lorien/OPEN_MAT/_autoai/data/data_bn.mat', squeeze_me=True)
#x = dat['x'][:,3]
#y = dat['y']
#w = dat['w']*5
#N = x.shape[0]
#x = np.reshape(x, (N, 1))
#y = np.reshape(y, (N, 1))
#w = np.reshape(w, (N, 1))
#ytp = ['num']
#SV = []

# Data load
dat = pd.read_csv(dpath)
x = dat.iloc[:,:3].values
w = c_(dat.iloc[:,3].values)
y = dat.iloc[:,4:].values

ytp = np.array(['num', 'bin', 'ord', 'nom'])
xtp = np.array(['num', 'ord', 'nom'])
ix = 0;
iy = [0, 1, 2, 3];

x = x[:, ix]
y = y[:, iy]
xtp = xtp[ix]
N = x.shape[0]
w = np.reshape(w, (N, 1))
x = np.reshape(x, (N, 1))

# UNSUPERVISED BINNING
# hyperparameters for UBinning
# md - desired number of bins (excluding Missing, Other and SpecialValue-s
# pd - desired percentage of population
# xtp - data type of independent variable
# ytp - data type of dependent variable
# nmin - minimal number of (weighted) records
# met - enr - equal number of records,   erv - equal ranges of values,   epp - equal percentage of population
# sv - special values

tic()
ub = ubng(x, xtp, w, y=y, ytp=ytp)
print('binning /ubng/: ', toc(0))

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
if xtp == 'ord':
    sv = [1., 2.]  # special values
    ux = np.unique(x[~np.isnan(x)])
    for i in sv: ux = list(filter(lambda a: a != i, ux))
    mt_order = ux[::-1]
else:
    mt_order = []

tic()
ub = stbnsy(ub, x, y, w, xtp, ytp)
# todo: encoding to add info in sb in a separate step
ub_st, ub = stbng('ub', ub, xtp, ytp, x, y, w)
print('stats /stbnsy, stbng/: ', toc(0))

## Visualization
## T = viz(sb, n, nw, syy, syy2, dist, par)
#[n, nw, syy, syy2, wy] = bns2arr(ub)
#[x1, w1] = mdep(syy, nw, wy)
#D = dist1(x1, w1, par['met_dist'], 'ord')[0]
#dist = np.append(np.nan, D)
#my = syy.flatten()/nw.flatten()
#df = pd.DataFrame({'my':my, 'dist':dist.flatten(), 'nw':nw.flatten(), 'n':n.flatten()})
#print(df)
##print(df.iloc[ind,:])
##ind = my.argsort(axis=0)

tic()
[sb, D1] = sbng(ub, xtp, ytp, met='hclust')
print('binning /sbng/: ', toc(0))

tic()
sb = stbnsy(sb, x, y, w, xtp, ytp)
# todo: encoding to add info in sb in a separate step
sb_st, sb = stbng('sb', sb, xtp, ytp, x, y, w)
print('stats /stbnsy, stbng/: ', toc(0))

[n, nw, syy, syy2, wy] = bns2arr(sb)
[x, w] = mdep(syy, nw, wy)
D = dist1(x, w, 'manh', 'ord')[0]
dist = np.append(np.nan, D)
print('stats_end /bns2arr, mdep, dist1/: ', toc(0))

## Visualization
## T = viz(sb, n, nw, syy, syy2, dist, par)
#my = syy.flatten()/nw.flatten()
#df = pd.DataFrame({'my':my, 'dist':dist.flatten(), 'nw':nw.flatten(), 'n':n.flatten()})
#print(df)
##print(df.iloc[ind,:])
##ind = my.argsort(axis=0)
