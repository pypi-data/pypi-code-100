import random
from math import sqrt
import numpy as np

yesno = {True: 'yes', False: 'no'}			

def seed(n):
	random.seed(n)
	np.random.seed(n)
	np.set_printoptions(precision=3)

# https://stats.stackexchange.com/a/313138/112873
def correlated_normal(x, r, mean, sd):
    if abs(r)==1:
        return np.sign(r)*x
    else:
        # generate an initial normal random variable
        y = np.random.normal(size=x.size, loc=mean, scale=sd)
        # calculate the residuals for least square regression of y against x
        c = np.polyfit(x, y, deg=1)
        res = y - c[0]*x - c[1]
        # recover required correlation via a linear transformation:
        z = r*np.std(res)*x + res*np.std(x)*sqrt(1-r**2)
        # recover original distribution via a second linear transformation:
        a = sd/z.std()
        b = mean-a*z.mean()
        return a*z + b

def correlated_uniform(x, r, rng):
    if abs(r)==1:
        return np.sign(r)*x
    else:
        y = np.random.uniform(rng, size=x.shape[0])
        c = np.polyfit(x, y, deg=1)
        res = y - c[0]*x - c[1]
        z = r*np.std(res)*x + res*np.std(x)*sqrt(1-r**2)
        return rng*(z-min(z))/(max(z)-min(z))
            
def random_sign():
	return [-1, 1][random.randint(0, 1)]
	
def r(x, y):
	return np.corrcoef(x, y)[0,1]

def beta(X, Y, Z):   ## the first element is the index \(\beta_X\)
	a = r(Y, X) - r(Y, Z) * r(X, Z)
	b = 1 - r(X, Z) ** 2
	return a / b

def r2(X, Y, Z):
	a = r(Y, X) ** 2 + r(Y, Z) ** 2 - 2 * r(Y, X) * r(Y, Z) * r(X, Z)
	b = 1 - r(X, Z) ** 2
	return a / b
	
def r2b(y, yh):
	return 1-(np.square(y-yh).sum())/(np.square(y-y.mean()).sum())

def append_filename(name, postfix): # abc.png, x => abc.x.png
    parts = name.split('.')
    parts.insert(-1, postfix)
    return '.'.join(parts)