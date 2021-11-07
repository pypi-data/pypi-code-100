"""
author: OPEN-MAT
"""
import os
import sys
import numpy as np
import pandas as pd

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
dpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/data/ga/data_scoring5.csv'

sys.path.append(wpath)
os.chdir(wpath)

from aislab.op_nlopt.ga import *
from aislab.gnrl.sf import *

np.set_printoptions(precision=5, linewidth=100000, threshold=100000000)
pd.options.display.precision = 5
pd.options.display.max_rows = int(1e20)

# Load Data
data = pd.read_csv(dpath)
data = data[['Client07BG_GB_Score', 'Client07BG_GBR_Score', 'Good', 'Bad', 'Reject']]
# data.to_csv('/home/user/Desktop/Saso/OPEN_MAT/_autoai/data/Credissimo_05_01/data_scoring5.csv')
data.columns = ['Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']

par = {'Nind': 20,
       'mut_rate': 50,    # percentage of mutated invds /current beat indv is not mutating/
       'mut_strength': 1, # number of mutated gens 
       'mut_met':  'Gauss', #'Reset', # 
       'mut_stdev': 70,
       'stop_itrConstF': 10, 
       'pairing_met': 'Fbest', # 'wrnd', #   'rnd', #          # wrnd - weighted random pairing
       'select_met':  'Fhalf' # 'roulette' # 'rnd' # 
      }

#             Acc  Rej  mt    Nb   Ngb  NaN  min_maxCell
w = np.array([50,  50,  200,  0,   50,  1,   0])  # Weights: [discriminatory, monotonicity, minNb, minNr, No_NaN-s
args = {'nc1': 4,
        'nc2': 4,
        'lb1': np.min(data['Score_GB']),
        'ub1': np.max(data['Score_GB']),
        'lb2': np.min(data['Score_GBR']),
        'ub2': np.max(data['Score_GBR']),
        'w': w,
        'BRA': 5,       # max Bad rate for less risky population
        'TA': 30000,    # min Total number of applicants for less risky population
        'BRR': 95,      # min Bad rate for most risky population
        'TR': 10000,    # min Total number of applicants for most risky population
        'minNb': 10,    # min Nb 
        'minNgb': 500,  # min Ng+Nb
        'mindBR': 5,    # min delta BR
        'data': data
        }

s = np.array([[ 1,	1,	2,	3,	4],  # 3
              [ 1,	1,	2,	4,	5],
              [ 2,	2,	3,	4,	5],
              [ 3,	4,	4,	5,	6],
              [ 4,	5,	6,	6,	7]]) # R
s = np.array([[ 1,	1,	2,	3,	4],  # 4
              [ 1,	1,	2,	4,	5],
              [ 2,	2,	3,	4,	5],
              [ 3,	4,	4,	5,	6],
              [ 4,	5,	6,	6,	7]]) # R

##############################################################################
tic()
F_opt, x_opt = genopt(par, args)
toc()
##############################################################################

cs = x_opt

# [c11 , c12, c13, c14, c21 , c22, c23, c24]

G, B, R, TGB, TGBR, BR = tables(cs, data)
T1, T2 = tables2(G, B, R, TGB, TGBR, BR)  # if ~np.isinf(G):...

print('============================================')
T = {'': ['constraint', 'weight'],
     'BRA': [args['BRA'], w[0]],
     'BRR': [args['BRR'], w[1]],
     'TA': [args['TA'], w[2]],
     'TR': [args['TR'], w[3]],
     'minNb': [args['minNb'], w[4]],
     'minNr': [args['minNgb'], w[5]],
     'mindBR': [args['mindBR'], w[6]],
     'mutatRate': [par['mut_rate'], None],
     'mutMethod': [par['mut_met'], None],
     'mutStdev': [par['mut_stdev'], None],
     'stop_itrConstF': [par['stop_itrConstF'], None]
    }
print(pd.DataFrame(T).set_index(''))
print('objF: ', F_opt)

lus = np.max(np.max(s))
GG = np.full((lus, 1), np.nan)
BB = np.full((lus, 1), np.nan)
RR = np.full((lus, 1), np.nan)
TT = np.full((lus, 1), np.nan)
BRi = np.full((lus, 1), np.nan)

for i in range(1, lus + 1):
    ind = s == i
    GG[i-1] = sum(G.values[ind])
    BB[i-1] = sum(B.values[ind])
    RR[i-1] = sum(R.values[ind])
    TT[i-1] = sum(TGBR.values[ind])
    
BRi = BB/(GG + BB)*100
TT = TT/sum(TT)*100
CumGG1 = np.cumsum(GG)
CumBB1 = np.cumsum(BB)
CumGG2 = np.cumsum(GG[::-1])[::-1]
CumBB2 = np.cumsum(BB[::-1])[::-1]

CumTT1 = c_(np.cumsum(TT))
CumTT2 = c_(np.cumsum(TT[::-1])[::-1])
CumBR1 = c_(CumBB1/(CumGG1 + CumBB1))
CumBR2 = c_(CumBB2/(CumGG2 + CumBB2))

nn = range(np.min(s), np.max(s)+1)
print('\n')
#print(np.hstack((np.array([nn]).T, BRi, CumBR1, CumBR2, TT, CumTT)))
Stats = pd.DataFrame(np.hstack((np.round(BRi, 2), np.round(TT, 2), np.round(CumBR1*100, 2), np.round(CumTT1, 2), np.round(CumBR2*100, 2), np.round(CumTT2, 2))))/100
Stats = Stats.dropna()
Stats.columns = ['BadRate', 'TotalPrc', 'CumBR', 'CumTotPrc', 'RevCumBR', 'RevCumTotPrc']
print(Stats.to_string(index=False))
print('\nCut-offsGB: ', cs[0:4])
print('Cut-offsGBR: ', cs[4:])


print('\nBadRate: ')
np.set_printoptions(suppress=True)
print(np.round(BR, 2))

print('\nTotal: ')
print(TGBR)
print('\nGood: ')
print(G)
print('\nBad: ')
print(B)
print('\nGood&Bad: ')
print(TGB)
print('\nReject: ')
print(R)
