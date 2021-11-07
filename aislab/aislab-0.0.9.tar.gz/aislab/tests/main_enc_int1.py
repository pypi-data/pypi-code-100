import re
import os
import sys
import numpy as np
import pandas as pd

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/data_enc_int.csv'
cpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/bngenc/cnf_enc_int.csv'
sys.path.append(wpath)
os.chdir(wpath)

from aislab.dp_feng.binenc import *
from aislab.gnrl import *

np.set_printoptions(precision=15)
np.set_printoptions(threshold=10000)
np.set_printoptions(linewidth=10000)
pd.options.display.max_rows = int(1e20)

x = pd.read_csv(dpath)
# x = x.iloc[:15, :]
cnf = pd.read_csv(cpath)

cname = cnf['cname'].tolist()
x = x[cname]

xtp = cnf['xtp']
vtp = cnf['vtp']
order = cnf['order']
dsp = 1

i2 =  10 # len(cname) #
cname = cname[:i2]
x = x[cname]
xtp = xtp[:i2].values
vtp = vtp[:i2].values
order = order[:i2].values


tic()
xe = enc_int(x, cname, xtp, vtp, order, dsp)
toc()

xe.to_csv('res.csv')



