from collections import defaultdict
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/rreg/data_rreg.csv'

sys.path.append(wpath)
os.chdir(wpath)

from aislab.gnrl.sf import *
from aislab.md_reg.linest import *
from aislab.md_reg.rreg import *
from aislab.dp_feng.decomp import *
from aislab.dp_feng.filt import *

###############################################################################
def forecast(fi, pm, fit, pmt, ys, T):
    if not isinstance(ys, np.ndarray): ys = np.array([ys])

    ym2 = fi@pm
    ymt = np.mean(fit@pmt)
    # % add back trend in forecast
    ym1 = ym2 + ymt
    # % add back period in forecast
    if len(ys) > T: ym = ym1*max(1, ys[len(ys) - T])
    else:           ym = ym1*np.mean(ys)
    return ym, ymt, ym1, ym2
###############################################################################

# INITIALIZING
data = pd.read_csv(dpath)
y = data['sales'].values
y = np.reshape(y, (760, 1))
u = data[['base_price', 'discount']].values
day = np.arange(1, len(y))
prod_start_time = datetime.datetime.now()
r = 1
N = 1000

# periodic component - find optimal T, Ns - linspace?
# T - periods, Ns - seasonality samples, Nt - full period for modeling,
# w - weights, wmin -
T = 7
# if T = 0, error
mode = 'single'  # 'multiple' outputs
Ns = T*12
wmin = 0.4
dk = 1

mode = 'multiple'
# Ns =
Nt = T*np.array([1, 2, 4, 8])
wmin = np.array([1, 1, 1, 1])  #/np.sqrt([1, 2, 4, 8])

# trend
if mode == 'single':
    w = np.tile((np.arange(1, 1 + Nt/T) - 1)/(Nt/T - 1)*(1 - wmin) + wmin, (T, 1)).T.ravel()
elif mode == 'multiple':
    keys = list(range(len(Nt)))
    # w = dict(keys=key, values=key)
    w = defaultdict(list)
    for h in keys:
        if Nt[h] == T:
            w[h] = np.ones((T))
        else:
            Nt1 = Nt[h]
            wmin1 = wmin[h]
            # w[h] = vec(repmat(([1:Nt1/T] - 1)/(Nt1/T - 1)*(1 - wmin1) + wmin1, T, 1))
            w[h] = np.tile((np.arange(1, 1 + Nt1/T) - 1)/(Nt1/T - 1)*(1 - wmin1) + wmin1, (T, 1)).T.ravel()

# % rls - ym
# hf model parameters

N, pld = y.shape
m = u.shape[1]  # promo

na = np.ones((r, r))
nb = np.ones((r, m))
pm0 = np.ones((r, r))
mod = 'vff'
Ne = 70
se = 0.5
rvmin = 0.4
rv = 1
me1 = np.empty((0, 0))
ee = np.empty((0, 0))
a = 0.1
rc = 0.9
s = 5
trPmin = 0.1
pn = int(np.sum([np.sum(pm0),
                 np.sum(na),
                 np.sum(nb)
                 ]))
pm = np.zeros((pn, N))
nn = int(np.max([np.max(na), np.max(nb)]) + 1)
par = {'na':na,
        'nb':nb,
        'pm0':pm0,
        'rv':rv,
        'me1':me1,
        'ee':ee
        }
fi = dmpv(np.zeros((nn, m)), np.zeros((nn, r)), na=na, nb=nb, pm0=pm0)
# P = covariance matrix
if mod == 'cmm':
    P = np.eye(len(pm))
else:
    P = np.eye(len(pm))*10

# % rls - yt
# trend model parameters
rr = len(Nt)
mm = m

tna = np.ones((rr, rr))
tnb = np.ones((rr, mm))
tpm0 = np.zeros((rr, 1))
tNe = Ne
tse = np.tile(0.05, (rr, 1))  ############# <<<<<<<
trvmin = np.tile(rvmin, (rr, 1))
trv = np.ones((rr, 1))
tme1 = np.empty((0, 0))
tee = np.empty((0, 0))
at = 0.1
rct = 0.9
st = 5
trPmint = 0.1
tpm0 = np.zeros((rr, 1))
trvmin = np.tile(0.4, (rr, 1))
tpn = int(np.sum([np.sum(tpm0),
                  np.sum(tna),
                  np.sum(tnb)
                  ]))
pmt = np.zeros((tpn, N))
tnn = int(np.max([np.max(tna), np.max(tnb)]) + 1)
part = {'na':tna,
        'nb':tnb,
        'pm0':tpm0,
        'rv':trv,
        'me1':tme1,
        'ee':tee
        }
fit = dmpv(np.zeros((tnn, mm)), np.zeros((tnn, rr)), na=tna, nb=tnb, pm0=tpm0)

if mod == 'cmm':    Pt = np.eye(len(pm))*0.1
else:               Pt = np.eye(len(pmt))*1e0
y1 = np.zeros((N, 1))
ym = yti = yt = np.zeros((N, 1))  # np.empty((N,0))
ymt = ym1 = ym2 = np.zeros((N, 1))
yt0 = np.zeros((N, rr))
y20 = np.zeros((N, 1))
y1 = []
ys = []
r2 = []
for k in range(N - 1):  # k-th day
    k0 = max(0, k - max(Ns, max(Nt)))
    k1 = max(0, k - 1)
    # mdls2
    # % RECURSIVE DATA PREP & MODELLING
    # % Deperiodicity
    # % periodic component TODO: make it recursive
    yy = y[k0:k + 1]
    NN = len(yy)
    spm0 = permdl(yy[max(0, NN - Ns + 1):], T=T, Ne=Ns)  ##
    spm0 = spm0.ravel()
    if spm0.size == 1:
        ys1 = spm0
    else:
        ys1 = spm0[len(spm0) - 1]

    # % remove periodic component
    y1 = np.append(y1, yy[max(0, len(yy) - 1)]/max(1, ys1))
    ys = np.append(ys, ys1)
    # % Detrending
    Nt = np.array(Nt)
    if len(Nt) == 1:
        yti = mavg(y1[max(0, len(y1) - Nt):], w[max(0, len(w) - Nt):], Ne=Nt)
        # print ('\n uid:', q, '\n iternation k: ', k )
    else:
        yti = np.ones((len(Nt)))
        for h in range(len(Nt)):
            yti[h] = fltma(y1[max(0, len(y1) - Nt[h]):],
                              Nt[h],
                              w[h][max(0, len(w[h]) - Nt[h]):]
                              )
    yti = yti.reshape(-1, 1)
    y1k = y1[len(y1) - 1]

    yt0[k, :] = yti.T
    # REGRESSION

    # trend model
    um = u[k + dk].reshape(1, -1)

#    pmt[:, k:k + 1], fit1, Pt, trv, tme1, tee = rls(yti, um[len(um) - 1], pm=pmt[:, k1:k1 + 1], fi=fit, P=Pt,
#                na=tna, nb=tnb, pm0=tpm0, mod='non', Ne=tNe, se=tse,
#                rvmin=trvmin, rv=trv, me1=tme1, ee=tee, a=at, rc=rct, trPmin=trPmint, s=st)
    if k < nn:
        pmt[:, k:k + 1] = np.zeros((tpn, 1))
        yt = 0
        # remove trend
        y2 = y1k - yt
        y20[k, 0] = y2
        # % HF model
        pm[:, k:k + 1] = np.zeros((pn, 1))
    else:
        pmt[:, k:k + 1], Pt, part = rls(u[k-nn+1+dk:k+1+dk, :], yt0[k-nn+1:k+1, :], pm=pmt[:, k1:k1 + 1], P=Pt, na=tna, nb=tnb, pm0=tpm0, mod='non', Ne=tNe, se=tse, rvmin=trvmin, rv=trv, me1=tme1, ee=tee, a=at, rc=rct, trPmin=trPmint, s=st, par=part)  # U and Y are upto k-th time instant!!!
        trv = part['rv']
        tme1 = part['me1']
        tee = part['ee']
        fit = dmpv(u[k-nn+1:k+1, :], yt0[k-nn+1:k+1, :], par=part)
        yt = np.mean(fit@pmt[:, k:k + 1])
        # remove trend
        y2 = y1k - yt
        y20[k, 0] = y2
        # % HF model
        pm[:, k:k + 1], P, par = rls(u[k-nn+1+dk:k+1+dk, :], y20[k-nn+1:k+1, :], pm=pm[:, k1:k1 + 1], P=P, na=na, nb=nb, pm0=pm0, mod='non', Ne=Ne, se=se, rvmin=rvmin, rv=rv, me1=me1, ee=ee, a=a, rc=rc, trPmin=trPmin, s=s, par=par)  # U and Y are upto k-th time instant!!!
        rv = part['rv']
        me1 = part['me1']
        ee = part['ee']
        fi = dmpv(u[k-nn+1:k+1, :], y20[k-nn+1:k+1, :], par=par)
    # FORECAST
    ym[k + 1, 0:1], ymt[k + 1, 0:1], ym1[k + 1, 0:1], ym2[k + 1, 0:1] = forecast(fi, pm[:, k:k + 1], fit, pmt[:, k:k + 1], ys, T)
    ym = np.maximum(0, ym)

# #% replace periods without sales with 0
## TEST ##
# noproduct = pk.retail.rem_no_prod(y)
# yy1 = ym
# yy1[noproduct==1] = 0
# yy2 = pk.retail.rem_no_prodd(y, ym)
# yyy = np.hstack((y, ym, yy1, yy2 ))

## TEST ##
# ym = retail.rem_no_prodd(y, ym)

#####################
# rsq = pk.sf.vaf(y,ym)/100
# results = np.vstack((results, np.array([q, upc1, rsq[0]])))

forecasts = np.hstack((y, ym))

VAF = vaf(y, ym)

prod_end_time = datetime.datetime.now()

print('Time elapsed between product processing {0} - {1}'.format(prod_start_time, prod_end_time))

forecasts = pd.DataFrame(forecasts)
forecasts.to_csv("results.csv")

plt.plot(forecasts)
plt.show()

del prod_start_time
del prod_end_time
