
# coding: utf-8

# In[1]:


# Import pandas  
import os
from typing import Type 
cmd = "pip install sklearn statsmodels numpy"
os.system(cmd)

import numpy as np
import warnings 
warnings.filterwarnings("ignore")
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
import itertools
import math 
import random


# In[2]:


class simple_forcust_T1():
    def __init__(self,x,a,b,c,p,y):
        trans_x=np.log10(x)
        self.x= trans_x
        self.a=int(a)
        self.b=int(b)
        self.c=int(c)
        self.y=y
        self.p=p
        self.counter = 0
    def Model_manual(self):
        X_train, X_test = train_test_split(self.x,test_size=self.p, random_state=42)
        a1 = [self.a,self.b,self.c]
        n = 3
        perm_iterator = itertools.permutations(a1, n)
        rmsel_model=[]
        for item in perm_iterator:
            mod = ARIMA(X_train,order=item)
            res1 = mod.fit()
            predictions = res1.predict(start=len(X_train), end=len(X_train)+len(X_test)-1, dynamic=False)
            rmse1 = sqrt(mean_squared_error(X_test, predictions))
            n_1=[rmse1,item]
            rmsel_model.append(n_1)
        for i in rmsel_model:
            for j in range(len(i)):
                if i[j]<= self.y and j==0:
                    return rmsel_model[j]
                else:
                    return min(rmsel_model)  
    def Model_random(self,t):
        a1 = min([self.a,self.b,self.c])
        a2 = max([self.a,self.b,self.c])
        ran_a=int(random.randint(a1,a2))
        ran_b=int(random.randint(a1,a2))
        ran_c=int(random.randint(a1,a2))
        self.counter += 1
        X_train, X_test = train_test_split(self.x,test_size=self.p, random_state=42)
        a1 = [ran_a,ran_b,ran_c]
        n = 3
        perm_iterator = itertools.permutations(a1, n)
        rmsel_model=[]
        for item in perm_iterator:
            mod = ARIMA(X_train,order=item)
            res1 = mod.fit()
            predictions = res1.predict(start=len(X_train), end=len(X_train)+len(X_test)-1, dynamic=False)
            rmse1 = sqrt(mean_squared_error(X_test, predictions))
            if rmse1 <= self.y:
                return [item,rmse1]
            else:
                if self.counter > t: 
                    return "time_out"
                else:
                      
                    self.Model_random(t)

class Window(simple_forcust_T1):
    def __init__(self,x,a,b,c,p,y,N):
        super().__init__(x,a,b,c,p,y)
        self.N=N
        #X_1=simple_forcust_1.Model(self)[1]
    def prediction(self,s,t):
        if s =="manual" and t ==0:
            x_1=simple_forcust_T1.Model_manual(self)[1]
            mod=ARIMA(self.x,order=x_1).fit()
            predictions = mod.predict(start=len(self.x), end=len(self.x)+self.N, dynamic=False)
            x_2=np.array(predictions)
            return 10**x_2
        elif s =="random":
            x_1=list(simple_forcust_T1.Model_random(self,t)[0])
            mod=ARIMA(self.x,order=x_1).fit()
            predictions = mod.predict(start=len(self.x), end=len(self.x)+self.N, dynamic=False)
            x_2=np.array(predictions)
            return 10**x_2 
                     


# In[ ]:




