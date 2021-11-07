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

np.set_printoptions(precision=4)
np.set_printoptions(threshold=10000)
np.set_printoptions(linewidth=10000)
pd.options.display.max_rows = int(1e20)

# Data load
dat = pd.read_csv(dpath)
x = dat.iloc[:,:3].values
w = c_(dat.iloc[:,3].values)
y = dat.iloc[:,4:].values

# Set binning parameters
ytp = np.array(['num', 'bin', 'ord', 'nom'])
xtp = np.array(['num', 'ord', 'nom'])
ix = 2;
iy = 1; # 1 - bin
ubmet = 'enr' # 'erv' # 'epp' # 
SV = []# [1, 2];

par = {}
# ub
par['md'] = 100
par['pd'] = 1
par['xtp'] = xtp[ix]
par['ytp'] = [ytp[iy]]
par['nmin'] = 50
par['met'] = ubmet
par['sv'] = SV
# sb
#par['md'] = 10 # set below
par['skip_mos'] = ['m', 'o', 'sv']
par['met_dist'] = 'manh' #'eucl'
par['met_enc'] = 'my'
par['mt_order'] = []
par['nmin_uy'] = [50, 50] # min number of obs in bin per each (ascending ordered) unique value of y
par['mar'] = np.inf
par['pt'] = 0.05
par['ba'] = 0
par['maxprm'] = 20000
par['dGBInd'] = 20
par['tolmindGBInd'] = 5
par['mt'] = 1
par['minB'] = 50
par['tolminB'] = 20

# Prep data for binning
x = x[:, ix]
y = y[:, iy]
N = x.shape[0]
w = np.reshape(w, (N, 1))
x = np.reshape(x, (N, 1))
y = np.reshape(y, (N, 1))
if 'ord' in par['xtp']:
    ux = np.unique(x[~np.isnan(x)])
    for i in par['sv']: ux = list(filter(lambda a: a != i, ux))
    par['mt_order'] = ux[::-1]

# UNSUPERVISED BINNING
tic()
ub = ubng(x, par['xtp'], w)
#ub = ubng(x, w, par)
ub = stbnsy(ub, x, y, w, xtp[ix], [ytp[iy]])
ub_st, ub = stbng('ub', ub, xtp[ix], [ytp[iy]], x, y, w)
print('ubng time: ', toc(0))

# Visualization
# todo: T = viz(sb, n, nw, syy, syy2, dist, par)
[n, nw, syy, syy2, wy] = bns2arr(ub)
[x1, w1] = mdep(syy, nw, wy)
D = dist1(x1, w1, par['met_dist'], 'ord')[0]
dist = np.append(np.nan, D)
my = syy.flatten()/nw.flatten()
df = pd.DataFrame({'n':n.flatten(), 'nw':nw.flatten(), 'sy':syy.flatten(), 'dist':dist.flatten(), 'my':my})
print(df)
#print(df.iloc[ind,:])
#ind = my.argsort(axis=0)

# SUPERVISED BINNING
par['met'] = 'co1y' # 'hclust' # 'pclust' # 
par['md'] = 6
tic()
[sb, D1] = sbng(ub, xtp[ix], [ytp[iy]])
sb = stbnsy(sb, x, y, w, xtp[ix], [ytp[iy]])
sb_st, sb = stbng('sb', sb, xtp[ix], [ytp[iy]], x, y, w)
print('sbng: ', toc(0))

# Visualization
# todo: T = viz(sb, n, nw, syy, syy2, dist, par)
[n, nw, syy, syy2, wy] = bns2arr(sb)
[x1, w1] = mdep(syy, nw, wy)
D = dist1(x1, w1, 'manh', 'ord')[0]
dist = np.append(np.nan, D)
my = syy.flatten()/nw.flatten()
df = pd.DataFrame({'n':n.flatten(), 'nw':nw.flatten(), 'sy':syy.flatten(), 'dist':dist.flatten(), 'my':my})
print(df)

# df = pd.DataFrame({'binning':['ub', 'sb'], 'Gini':[ub_st[0]['Gini'], sb_st[0]['Gini']], 'Chi2':[ub_st[0]['Chi2'], sb_st[0]['Chi2']]})
# print(df)

par['met_enc'] = 'my'
xe_my = enc_apl(sb, x, xtp[ix], 'my')
# par['met_enc'] = 'woe'
# xe_woe = enc_apl(sb, x, par)
par['met_enc'] = 'dv'
xe_dv = enc_apl(sb, x, xtp[ix], 'dv')

res = np.hstack((x, xe_my, xe_dv))
print(res[:20,:])

