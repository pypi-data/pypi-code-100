import os
import sys
import numpy as np
import pandas as pd

met_enc = 'dv' # 'my' # 'woe'

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/lending_club/'
cpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/lending_club/cnf_LC.csv'

np.set_printoptions(precision = 15, linewidth = 1e5, threshold = 1e10)
pd.options.display.precision = 15
pd.options.display.max_rows = int(1e20)

sys.path.append(wpath)
os.chdir(wpath)

from dp_feng.binenc import *
from gnrl import *
from md_fsel.swlinr import *
from md_fsel.swlogr import *
from md_reg import *

x = pd.read_csv(dpath + 'x_samples_250000.csv')
y = pd.read_csv(dpath + 'y_samples_250000.csv')
cnf = pd.read_csv(cpath)

N = 1000 # x.shape[0] #

x = x.iloc[:N, :]
y = y.iloc[:N, :].values

tic2() # Overall time

cname = cnf['cnames'].tolist()
xtp = cnf['xtp'].values
vtp = cnf['xtp'].values
order = cnf['order']
x = x[cname]
w = ones((N, 1))
ytp = ['bin']
y[find(np.isnan(y) == 1)] = 0
w[find(np.isnan(w) == 1)] = 0

dsp = 1
order = order.values
dlm = '$'
# 1. All categorical vars to int
tic()
xe = enc_int(x, cname, xtp, vtp, order, dsp, dlm)
toc('INT-ENCODING')
xe.to_csv('data_enc_int.csv')

# 2. BINNING
tic()
ub = ubng(xe, xtp, w, y=y, ytp=ytp, cnames=cname, dsp=True)     # unsupervised binning
toc('UBNG')
tic()
sb = sbng(ub, dsp=True)            # supervised binning
toc('SBNG')

# 3. ONE HOT ENCODING
tic()

x_mdl, cnames_mdl = enc_apl(sb, xe, met_enc)
toc('ENCODING')

dat = pd.DataFrame(np.hstack((x_mdl, y, w)))
cnames_mdl = cnames_mdl
varnames = cnames_mdl
varnames.append('y')
varnames.append('w')
dat.columns = varnames
if met_enc == 'dv':     dat.to_csv('data_enc_dv.csv')
elif met_enc == 'woe':  dat.to_csv('data_enc_woe.csv')
elif met_enc == 'my':   dat.to_csv('data_enc_my.csv')

# dat = pd.read_csv('/home/user/Desktop/Saso/Edu/TU/~DiplomniRaboti/2019_TsvetomirNedyalkov/python/aislab/' + 'data_enc_dv.csv')
# x_dv = dat.iloc[:, :-2]
# y = c_(dat.iloc[:, -2].values)
# w = c_(dat.iloc[:, -1].values)
# cnames_dv = x_dv.columns.tolist()
# x_dv = x_dv.values

# 4. SW LINEAR REGRESSION
met = 'SWR' # 'BR' # 'FR' #
mtp = 'empty' # 'full' # 'init' #
ivi = np.array([]).astype(int) # c_(np.arange(1, int(np.floor(x_dv.shape[1]/3))))
afcnv = 1e-6

tic()
mdl_lin = swlinr(x_mdl, y, w, cnames=cnames_mdl, met=met, mtp=mtp, ivi=ivi)
toc('SWLINR')

# 5. SW LOGISTIC REGRESSION
# mtp = 'init' # 'empty' # 'full' #
# ivi = mdl_lin[-1]['ivi']
tic()

mdl_log = swlogr(x_mdl, y, w, cnames=cnames_mdl, SLE=1, SLS=1, met=met, mtp=mtp, ivi=ivi, dsp_op=2)
toc('SWLOGR')

toc2('OVERALL') # Overall time

N = y.shape[0]
xx_lin = np.hstack((ones((N,1)), x_mdl[:, mdl_lin[-1]['ivi'][1:]-1]))
ym_lin = xx_lin@mdl_lin[-1]['pm']
vaf_lin = vaf(y, ym_lin, w, p=mdl_lin[-1]['n'])

xx_log = np.hstack((ones((N,1)), x_mdl[:, mdl_log[-1]['ivi'][1:]-1]))
ym_log = lgr_apl(xx_log, mdl_log[-1]['pm'])
vaf_log = vaf(y, ym_log, p=mdl_log[-1]['n'])

print('VAF_LIN: ', vaf_lin)
print('VAF_LOG: ', vaf_log)

print('VAF_LIN ALL:')
for i in range(len(mdl_lin)):   print(mdl_lin[i]['st']['ovr']['VAF'])

print('VAF_LOG ALL:')
for i in range(len(mdl_log)):
    # print(mdl_log[i]['st']['ovr']['VAF'])
    print(mdl_log[i]['st']['ovr']['VAF'])


import matplotlib.pyplot as plt
# plt.plot(y)
# plt.plot(ym_lin)
# plt.show
plt.plot(ym_log)
plt.show


