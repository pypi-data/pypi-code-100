import numpy as np
from sf import *

a=c_(10*np.array(range(1,10)))
b=c_(10*np.array(range(1,10)))
x=c_(1*np.array(range(1,10)))/10.1
bi = np.zeros(x.shape)
ii = (x > 0) & (x < (a + 1)/(a + b + 2))


res = betacf(a, b, x)

pval = betai(a, b, x)
print(pval)