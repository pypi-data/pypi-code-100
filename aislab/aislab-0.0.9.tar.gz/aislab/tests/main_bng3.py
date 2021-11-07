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

####################################################################################################
# Weight factor -> varying
del w
w = rand((x.shape[0], 1), l=0.5, h=5, seed=0)
w = w/np.sum(w)*(500000 + 500000 - 499999.9999999951)
sum(w)
# Add NaN-s in x
ind = rand(x.shape, seed=0) > 0.8
xshape = x.shape
x = x.flatten().astype('float')
ind = ind.flatten()
x[ind] = np.nan
x = np.reshape(x, xshape)
# From .mat to .csv
dat1 = np.hstack((x, w, y))
df = pd.DataFrame(dat1)
df.columns = ['x_num', 'x_ord', 'x_nom', 'w', 'y_num', 'y_bin', 'y_ord', 'y_nom']
df.to_csv('/home/user/Desktop/Saso/OPEN_MAT/_autoai/data/data_bn0.csv', sep=',', index=None)
###################################################################################################

dat = pd.read_csv('/home/user/Desktop/Saso/OPEN_MAT/_autoai/data/data_bn0.csv')
x = dat.iloc[:,:3].values
w = dat.iloc[:,3].values
y = dat.iloc[:,4:].values
ix = 0

# Prep data for binning
x = c_(x[:, ix])
y = c_(y[:, 1])
w = c_(w)
N = x.shape[0]

x = x + y*rng(x)
x[1,0] = np.nan

#if ix > 0: x=x.astype(str)
#if x.dtype.type is np.str_:
#    if 'xi_order' in par and par['xi_order'] is not None: x = enc_int(x, par['xi_order'])
#    else:                                                 x = enc_int(x)



# Set binning parameters
ytp = np.array(['bin']);
xtp = np.array(['num', 'ord', 'nom']); # list with data types of all x vars...
SV = [x[0,0]]

par = {}
par['xtp'] = xtp[ix]
par['ytp'] = ytp
# ub
par['md'] = 100
par['pd'] = 1
par['nmin'] = 50
par['met'] = 'enr' # 'erv' # 'epp' # 
par['sv'] = SV
if 'ord' in par['xtp']:
#    if x.dtype.type is np.str_: x[np.where(x.astype(str)==str(np.nan))] = 'mostcommonstring'
    ux = np.unique(x[~np.isnan(x)])
    for i in par['sv']: ux = list(filter(lambda a: a != i, ux))
    par['xi_order'] = ux[::-1]
else:
    par['xi_order'] = None
# sb
#par['md'] = 10 # set below
par['nmin_uy'] = [50, 50] # min number of obs in bin per each (ascending ordered) unique value of y
par['skip_mos'] = ['m', 'o', 'sv']
par['met_dist'] = 'manh' #'eucl'    # todo: single, complete, ward, average, ...
par['met_enc'] = 'my'
par['mar'] = np.inf
par['pt'] = 0.05
par['ba'] = 0
par['maxprm'] = 20000
par['dGBInd'] = 20
par['tolmindGBInd'] = 5
par['mt'] = 1
par['minB'] = 50
par['tolminB'] = 20

# UNSUPERVISED BINNING
tic()
ub = ubng(x, par['xtp'], w)
#ub = ubng(x, w, par)
ub_st, ub = stbng('ub', ub, xtp[ix], ytp, x, y, w)  # calc ub stats
print('ubng time: ', toc(0))

# SUPERVISED BINNING
par['met'] = 'co1y' # 'hclust' # 'pclust' # 
par['md'] = 6
tic()
[sb, D1] = sbng(ub, xtp[ix], ytp)
sb = stbnsy(sb, x, y, w, xtp[ix], ytp)
sb_st, sb = stbng('sb', sb, xtp[ix], ytp)  # calc sb stats
print('sbng: ', toc(0))

if sb is None: pass
else: 
    df = pd.DataFrame({'binning':['ub', 'sb'], 'm':[len(ub), len(sb)], 'Gini':[ub_st[0]['Gini'], sb_st[0]['Gini']], 'Chi2':[ub_st[0]['Chi2'], sb_st[0]['Chi2']]})
    print(df)

    par['met_enc'] = 'my'
    xe_my = enc_apl(sb, x, xtp[ix], 'my')
    #par['met_enc'] = 'woe'
    #xe_woe = enc_apl(sb, x, par)
