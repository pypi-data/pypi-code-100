"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
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
from aislab.gnrl.bf import *

np.set_printoptions(precision=5, linewidth=100000, threshold=100000000)
pd.options.display.precision = 5
pd.options.display.max_rows = int(1e20)

# Load Data
# data = pd.read_csv(dpath)
# data = data[['Client07BG_GB_Score', 'Client07BG_GBR_Score', 'Good', 'Bad', 'Reject']]
# data.columns = ['Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']

########################################################################################################################
########################################################################################################################
data = pd.read_csv('/home/user/Desktop/Saso/AutoSCDev/data/sc_Stik_06/Scored_Data.csv')
data = data[['APP_LoanContractID', 'DER_APP_NewClient', 'GB_Score_New', 'GBR_Score_New', 'Good', 'Bad', 'Reject']]
data.columns = ['APP_AccountID', 'NewClient', 'Score_GB', 'Score_GBR', 'Good', 'Bad', 'Reject']
########################################################################################################################
########################################################################################################################

#Strat = 'NewClients'
Strat = 'OldClients'


par = {'Nind': 40,
       'mut_rate': 50,      # percentage of mutated invds /current beat indv is not mutating/
       'mut_strength': 2,   # number of mutated gens
       'mut_met':  'Gauss', #'Reset', # 
       'mut_stdev': 70,
       'stop_itrConstF': 10, 
       'pairing_met': 'Fbest', # 'wrnd', #   'rnd', #          # wrnd - weighted random pairing
       'select_met':  'Fhalf' # 'roulette' # 'rnd' # 
      }

args = {'nc1': 4,
        'nc2': 4,
        'lb1': np.min(data['Score_GB']),
        'ub1': np.max(data['Score_GB']),
        'lb2': np.min(data['Score_GBR']),
        'ub2': np.max(data['Score_GBR']),
       'minx': np.min(np.min(data[['Score_GB', 'Score_GBR']])),
       'maxx': np.max(np.max(data[['Score_GB', 'Score_GBR']])),
          # 'w': w,
        'BRA': 10,       # max Bad rate for less risky population
         'TA': 500,      # min Total number of applicants for less risky population
        'BRR': 70,     # min Bad rate for most risky population
         'TR': 500,      # min Total number of applicants for most risky population
      'minNb': 10,   # min Nb
     'minNgb': 30,   # min Ng+Nb
     'mindBR': 0,    # min delta BR
       # 'data': data
        }

# X = np.array([[-1471, -1469, -34, 922, -1860, -1403, -95, 1053], [-1469, -1177, 230, 1066, -1384, -1097, 86, 954], [-1150, -1110, 237, 1047, -1253, -643, 131, 997], [-900, -600, 237, 1047, -1000, -643, 131, 997], [-700, -400, 237, 1047, -900, -643, 131, 997]])
# F = func(X, args)
# print(F)

if Strat == 'NewClients':
    data = data[data['NewClient'] == True]
    ##############################################################################
    #             AA   RR    mt   Nb Ngb  NaN min_maxCell
    w = np.array([500, 10000000, 100, 0, 100, 1e3, 1])  # Weights: [discriminatory, monotonicity, minNb, minNr, No_NaN-s
    args['w'] = w
    args['data'] = data
    s = np.array([[1, 1, 1, 3, 4],  # A
                  [2, 2, 3, 4, 5],  # L
                  [2, 3, 4, 5, 6],  # M
                  [2, 4, 5, 7, 7],  # H
                  [6, 7, 8, 9, 9]])  # R
    if s.shape[0] != args['nc1'] + 1 and s.shape[1] != args['nc2'] + 1: s = ones((args['nc1'] + 1, args['nc1'] + 1))
    tic()
    F_opt, x_opt = genopt(par, args)
    toc()
    cs = x_opt
    ##############################################################################
    # #             AA   RR    mt   Nb Ngb  NaN min_maxCell
    # w = np.array([0, 0, 0, 0, 0, 0, 0])  # Weights: [discriminatory, monotonicity, minNb, minNr, No_NaN-s
    # F_opt = None
    # args['w'] = w
    # args['data'] = data
    # s = np.array([[1, 1, 1, 2, 5],  # A
    #               [2, 2, 2, 4, 5],  # L
    #               [3, 4, 4, 4, 5],  # M
    #               [5, 5, 5, 5, 6],  # H
    #               [5, 5, 6, 6, 6]])  # R
    # #     GB                  GBR
    # CutoffsGB = [500, 550, 820, 837]
    # CutoffsGBR = [-325, 150, 320, 360]
    # cs = CutoffsGB + CutoffsGBR

elif Strat == 'OldClients':
    data = data[data['NewClient'] == False]
    data['Bad'][data['Reject'] == 1] = 0
    #             AA   RR        mt   Nb   Ngb  NaN  min_maxCell
    w = np.array([500, 10000000, 100, 100, 100, 1e3, 1])  # Weights: [discriminatory, monotonicity, minNb, minNr, No_NaN-s
    args['w'] = w
    args['data'] = data
    s = np.array([[1, 2, 3, 4, 6],  # A
                  [4, 4, 5, 6, 7],  # L
                  [6, 7, 7, 8, 8],  # M
                  [8, 8, 9, 9, 9],  # H
                  [10, 10, 10, 10, 10]])  # R
    if s.shape[0] != args['nc1'] + 1 and s.shape[1] != args['nc2'] + 1: s = ones((args['nc1'] + 1, args['nc1'] + 1))
    ##############################################################################
    tic()
    F_opt, x_opt = genopt(par, args)
    toc()
    cs = x_opt
    ##############################################################################
    # #             AA   RR    mt   Nb Ngb  NaN min_maxCell
    # w = np.array([0, 0, 0, 0, 0, 0, 0])  # Weights: [discriminatory, monotonicity, minNb, minNr, No_NaN-s
    # F_opt = None
    # args['w'] = w
    # args['data'] = data
    # s = np.array([[1, 2, 3, 4, 6],  # A
    #               [4, 4, 5, 6, 7],  # L
    #               [6, 7, 7, 8, 8],  # M
    #               [8, 8, 9, 9, 9],  # H
    #               [10, 10, 10, 10, 10]])  # R
    # #     GB                  GBR
    # CutoffsGB = [300, 570, 650, 860]
    # CutoffsGBR = [280, 480, 622, 681]
    # cs = CutoffsGB + CutoffsGBR




G, B, R, TGB, TGBR, BR = tables(cs, args)
T1, T2 = tables2(G, B, R, TGB, TGBR, BR, args)  # if ~np.isinf(G):...

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

lus = int(np.max(np.max(s)))
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

nn = range(int(np.min(s)), int(np.max(s) + 1))
print('\n')
#print(np.hstack((np.array([nn]).T, BRi, CumBR1, CumBR2, TT, CumTT)))
Stats = pd.DataFrame(np.hstack((np.round(BRi, 2), np.round(TT, 2), np.round(CumBR1*100, 2), np.round(CumTT1, 2), np.round(CumBR2*100, 2), np.round(CumTT2, 2))))/100
Stats = Stats.dropna()
Stats.columns = ['BadRate', 'TotalPrc', 'CumBR', 'CumTotPrc', 'RevCumBR', 'RevCumTotPrc']
print(Stats.to_string(index=False))
print('\nCut-offsGB: ', cs[:args['nc1']])
print('Cut-offsGBR: ', cs[args['nc1']:])


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
