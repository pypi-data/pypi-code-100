# เอกสารจาก
#1.https://medium.com/swlh/black-scholes-algorithmic-delta-hedging-c2cdd42ce175 
#2.https://aaronschlegel.me/measure-sensitivity-derivatives-greeks-python.html


try:
    #ลำดับมีผลพยายามโหลดที่ ใน folder ที่กำลัง Implement ก่อน
    #import config as con 
    from starfishX import config as con 
except:
    import starfishX.config as con

prefix = "starfishX."

if(con.__mode__=="debug"):
    prefix = ""


#ฟังก์ชันสำหรับหา rho และ theta
import numpy as np
import scipy.stats as si
import sympy as sy

import math
from scipy.stats import norm

import pandas as pd
import numpy as np


from datetime import datetime

from datetime import datetime
import pandas as pd

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def EuropeanCallRolling(df_UnderRight,df_CallOption,ExerciseDate,strike_price,risk_free_rate):
    '''
    
    '''
    df = df_UnderRight
    dfw5 = df_CallOption 

    histUnderRight = []         #เก็บประวัติราคาแม่
    histPriceEuropeanCall = []  #เก็บประวัติราคาจาก EuropeanCall
    histRealPrice = []          #warrnt ที่เปลี่ยนบนกระดาน

    histDelta = [] 
    histgamma = []
    histVega = []

    #add Greek
    histRho = []
    histTheta = []

    histDate = []

    #หาราคาที่เปลี่ยนแปลงตามช่วงเวลา
    for i in dfw5.sort_index().index:
        date_of_warrant = str(i)[:10]
        #std นับถึงปัจจุบัน
        std = df[df.index<date_of_warrant][['Close']].std()[0]


        date_now = df[df.index<date_of_warrant][['Close']].index[-1]
        date_now = str(date_now)[:10]
        time = days_between(date_now,ExerciseDate)
        time_to_expiration = time/365
        #print(time) ใช้เวลาจาก dataframe จะมีวันเสาร์อาทิตย์หรือวันหยุดด้วยได้

        price_now = df[df.index<date_of_warrant][['Close']].iloc[-1][0]


        #log value change time step 
        #print(price_now,std,time,time_to_expiration,strike_price)
        callOption = EuropeanCall(asset_price=price_now, 
                                  asset_volatility=std,
                                  strike_price=strike_price,
                                  time_to_expiration=time_to_expiration, 
                                  risk_free_rate=risk_free_rate)

        priceW5Real = dfw5[dfw5.index==date_of_warrant]['close'][0]

        #print(callOption.price)  
        histDate.append(date_of_warrant)

        histUnderRight.append(price_now)  #ราคาแม่

        histRealPrice.append(priceW5Real) #ราคา w5 บนกระดาษจริงๆ    
        histPriceEuropeanCall.append(callOption.price) #ราคา w5 จาก EuropeanCall

        histDelta.append(callOption.delta)

        histgamma.append(callOption.gamma)

        histVega.append(callOption.vega)

        #update
        histTheta.append(callOption.theta)
        histRho.append(callOption.rho)



    histDate = pd.to_datetime(histDate)
    
    #########
    
    rp = pd.DataFrame({'UnderRight':histUnderRight,
                   'Actual':histRealPrice,
                   'EuropeanCall':histPriceEuropeanCall,
                   'delta':histDelta,
                   'gamma':histgamma,
                   'vega':histVega,
                   'theta':histTheta,
                   'rho':histRho},index=histDate)
    
    return rp




#เอกสารจาก https://medium.com/swlh/black-scholes-algorithmic-delta-hedging-c2cdd42ce175
class EuropeanCall:
    '''
    ``float asset_price : ราคาสินค้าอ้างอิง ``  
    ``float asset_volatility : ความผันผวนของราคาสินค้าอ้างอิง `` 
    ``float strike_price : ราคาใช้สิทธิ `` 
    ``float time_to_expiration : วันหมดอายุ (จำนวนวัน/365) ``
    ``float risk_free_rate : อัตราผลตอบแทนที่ไม่มีความเสี่ยง ``
    return : คืนค่าเป็น Option Price,Delta,Gamma,Vega,Theta และ Rho
    ตัวอย่าง :
    callOption = EuropeanCall(asset_price=4.94, asset_volatility=0.8093888412229526,strike_price=2,
                          time_to_expiration=2.9013698630136986, risk_free_rate=0.015)
    '''
    def call_delta(
        self, asset_price, asset_volatility, strike_price,
        time_to_expiration, risk_free_rate
            ):
        b = math.exp(-risk_free_rate*time_to_expiration)
        x1 = math.log(asset_price/(b*strike_price)) + .5*(asset_volatility*asset_volatility)*time_to_expiration
        x1 = x1/(asset_volatility*(time_to_expiration**.5))
        z1 = norm.cdf(x1)
        return z1

    def call_gamma(
        self, asset_price, asset_volatility, strike_price,
        time_to_expiration, risk_free_rate
            ):
        b = math.exp(-risk_free_rate*time_to_expiration)
        x1 = math.log(asset_price/(b*strike_price)) + .5*(asset_volatility*asset_volatility)*time_to_expiration
        x1 = x1/(asset_volatility*(time_to_expiration**.5))
        z1 = norm.cdf(x1)
        z2 = z1/(asset_price*asset_volatility*math.sqrt(time_to_expiration))
        return z2

    def call_vega(
        self, asset_price, asset_volatility, strike_price,
        time_to_expiration, risk_free_rate
            ):
        b = math.exp(-risk_free_rate*time_to_expiration)
        x1 = math.log(asset_price/(b*strike_price)) + .5*(asset_volatility*asset_volatility)*time_to_expiration
        x1 = x1/(asset_volatility*(time_to_expiration**.5))
        z1 = norm.cdf(x1)
        z2 = asset_price*z1*math.sqrt(time_to_expiration)
        return z2/100
    
    
    #เอกสารจาก https://aaronschlegel.me/measure-sensitivity-derivatives-greeks-python.html
    def rho_call(self, asset_price, asset_volatility, strike_price,time_to_expiration, risk_free_rate):
    
        d2 = (np.log(asset_price / strike_price) 
               + (risk_free_rate - 0.5 * asset_volatility ** 2) * time_to_expiration) / (asset_volatility * np.sqrt(time_to_expiration))
        rho = time_to_expiration * strike_price * np.exp(-risk_free_rate * time_to_expiration) * si.norm.cdf(d2, 0.0, 1.0)
        return rho
    
    #เอกสารจาก https://aaronschlegel.me/measure-sensitivity-derivatives-greeks-python.html
    def theta_call(self, asset_price, asset_volatility, strike_price,time_to_expiration, risk_free_rate):
        d1 = (np.log(asset_price / strike_price) + (risk_free_rate + 0.5 * asset_volatility ** 2) * time_to_expiration) / (asset_volatility * np.sqrt(time_to_expiration))
        d2 = (np.log(asset_price / strike_price) + (risk_free_rate - 0.5 * asset_volatility ** 2) * time_to_expiration) / (asset_volatility * np.sqrt(time_to_expiration))
        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-d1 ** 2 * 0.5)
        theta = (-asset_volatility * asset_price * prob_density) / (2 * np.sqrt(time_to_expiration)) - risk_free_rate * strike_price * np.exp(-risk_free_rate * time_to_expiration) * si.norm.cdf(d2, 0.0, 1.0)
        return theta
    

    def call_price(
        self, asset_price, asset_volatility, strike_price,
        time_to_expiration, risk_free_rate
            ):
        b = math.exp(-risk_free_rate*time_to_expiration)
        x1 = math.log(asset_price/(b*strike_price)) + .5*(asset_volatility*asset_volatility)*time_to_expiration
        x1 = x1/(asset_volatility*(time_to_expiration**.5))
        z1 = norm.cdf(x1)
        z1 = z1*asset_price
        x2 = math.log(asset_price/(b*strike_price)) - .5*(asset_volatility*asset_volatility)*time_to_expiration
        x2 = x2/(asset_volatility*(time_to_expiration**.5))
        z2 = norm.cdf(x2)
        z2 = b*strike_price*z2
        return z1 - z2

    def __init__(
        self, asset_price, asset_volatility, strike_price,
        time_to_expiration, risk_free_rate
            ):
        self.asset_price = asset_price
        self.asset_volatility = asset_volatility
        self.strike_price = strike_price
        self.time_to_expiration = time_to_expiration
        self.risk_free_rate = risk_free_rate
        self.price = self.call_price(asset_price, asset_volatility, strike_price, time_to_expiration, risk_free_rate)
        self.delta = self.call_delta(asset_price, asset_volatility, strike_price, time_to_expiration, risk_free_rate)
        self.gamma = self.call_gamma(asset_price, asset_volatility, strike_price, time_to_expiration, risk_free_rate)
        self.vega = self.call_vega(asset_price, asset_volatility, strike_price, time_to_expiration, risk_free_rate)
        
        #update 
        #https://aaronschlegel.me/measure-sensitivity-derivatives-greeks-python.html
        self.rho = self.rho_call(asset_price, asset_volatility, strike_price, time_to_expiration, risk_free_rate)
        self.theta = self.theta_call(asset_price, asset_volatility, strike_price, time_to_expiration, risk_free_rate)

