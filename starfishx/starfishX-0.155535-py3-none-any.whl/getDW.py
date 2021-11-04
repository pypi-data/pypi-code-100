
import requests
import json 
import pandas as pd
from datetime import datetime

try:
    #ลำดับมีผลพยายามโหลดที่ ใน folder ที่กำลัง Implement ก่อน
    #import config as con 
    from starfishX import config as con 
except:
    import starfishX.config as con

prefix = "starfishX."

if(con.__mode__=="debug"):
    prefix = ""

def getDW(symbol):
    '''
      str : symbol 
      เช่น symbol  'INTU01C2201A'   
    '''
    urlStarter = 'https://api.set.or.th/api/stock/'+symbol+'/historical-trading' 

    resp = requests.get(urlStarter)
    txt = resp.json()

    df = pd.DataFrame(txt)
    df['date'] = pd.to_datetime(df['date']) #convert str2date
    df = df.set_index('date')

    return df