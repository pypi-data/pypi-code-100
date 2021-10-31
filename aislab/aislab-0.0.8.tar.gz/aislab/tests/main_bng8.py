import os
import sys
import numpy as np
import pandas as pd

# wpath = '/home/user/.../aislab'
# dpathx = '/home/user/....x_samples_250000.csv'
# dpathy = '/home/user/.../y_samples_250000.csv'
# cpath = '/home/user/.../cnf_LC.csv'

wpath = '/home/user/Desktop/Saso/Edu/TU/~DiplomniRaboti/2019_TsvetomirNedyalkov/python/aislab'
dpathx = '/home/user/Desktop/Saso/Edu/TU/~DiplomniRaboti/2019_TsvetomirNedyalkov/python/aislab/data/data_scoring/x_samples_250000.csv'
dpathy = '/home/user/Desktop/Saso/Edu/TU/~DiplomniRaboti/2019_TsvetomirNedyalkov/python/aislab/data/data_scoring/y_samples_250000.csv'
cpath = '/home/user/Desktop/Saso/Edu/TU/~DiplomniRaboti/2019_TsvetomirNedyalkov/python/aislab/data/data_scoring/cnf_LC.csv'

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


x = pd.read_csv(dpathx)
y = pd.read_csv(dpathy)
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
dsp = 1
order = order.values
dlm = '$'
# 1. All categorical vars to int
tic()
xe = enc_int(x, cname, xtp, vtp, order, dsp, dlm)
toc('INT-ENCODING')

# 2. BINNING
tic()
ub = ubng(xe, xtp, w, y=y, ytp=ytp, cnames=cname)     # unsupervised binning
toc('UBNG')
tic()
sb = sbng(ub)            # supervised binning
toc('SBNG')

# 3. ONE HOT ENCODING
tic()
x_dv, cnames_dv = enc_apl(sb, xe, 'dv')
toc('DUMMIES-ENCODING')
y[find(np.isnan(y) == 1)] = 0
w[find(np.isnan(w) == 1)] = 0

toc2('OVERALL') # Overall time