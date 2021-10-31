import sys
#sys.path.append('D:\\Lorien\\OPEN_MAT\\_autoai\\python\\sf')
import numpy as np
import pandas as pd
from aislab.gnrl.measr import *
# from dp import *
# from ml import *

g = np.array([1, 2, 3, 4, 5])
b = np.array([5, 4, 3, 2, 1])
print('Chi2:', chi2(g, b))
v = 10
C2 = chi2(g, b)
print('pvalC2:', pvalC(v, C2))
#print('WoE:', woe(g, b))
#print('GBI:', gbi(g, b))
#print('Gini:', gini(g, b))
#print('Vinf:', vinf(g, b))
#print('KS:', ks(g, b))
print('Dind:', dind(g, b))

g = np.array([[1, 2, 3, 4, 5]]).T
b = np.array([[5, 4, 3, 2, 1]]).T
print('Chi2:', chi2(g, b))
v = 10
C2 = chi2(g, b)
print('pvalC2:', pvalC(v, C2))
#print('WoE:', woe(g, b))
#print('GBI:', gbi(g, b))
#print('Gini:', gini(g, b))
#print('Vinf:', vinf(g, b))
#print('KS:', ks(g, b))
print('Dind:', dind(g, b))

g = np.array([[1, 2, 3, 4, 5], [3, 2, 1, 5, 4]]).T
b = np.array([[5, 4, 3, 2, 1], [5, 4, 3, 2, 1]]).T
print('Chi2:', chi2(g, b))
v = 10
C2 = chi2(g, b)
print('pvalC2:', pvalC(v, C2))
#print('WoE:', woe(g, b))
#print('GBI:', gbi(g, b))
#print('Gini:', gini(g, b))
#print('Vinf:', vinf(g, b))
#print('KS:', ks(g, b))
print('Dind:', dind(g, b))


#print('GBI:', gbi(g, b))
dat = pd.read_csv('D:\\Lorien\\OPEN_MAT\\_autoai\\data\\data_sf.csv', header=None)
y = dat.iloc[:, 0].values
y2 = dat.iloc[:, 1].values
nw = dat.iloc[:, 2].values
print('Frat:', frat(y, y2, nw))
F = frat(y, y2, nw)
v1 = 10
v2 = 202
print('pvalF:', pvalF(F, v1, v2))

y = np.vstack((dat.iloc[:, 0].values, dat.iloc[:, 0].values)).T
y2 = np.vstack((dat.iloc[:, 1].values, dat.iloc[:, 1].values)).T
nw = np.vstack((dat.iloc[:, 2].values, dat.iloc[:, 2].values)).T
print('Frat:', frat(y, y2, nw))
F = frat(y, y2, nw)
v1 = 10
v2 = 202
#F = np.array([10, 100])
print('pvalF:', pvalF(F, v1, v2))
