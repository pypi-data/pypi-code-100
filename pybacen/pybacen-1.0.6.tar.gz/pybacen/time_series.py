# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 14:38:45 2021

@author: Rafael Pereira de Castro
"""

import pandas as pd

def read_time_series(bacen_code: int, start: str = None, end: str = None) -> pd.core.frame.DataFrame:
  url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{bacen_code}/dados?formato=json'
  ts = pd.read_json(url)
  ts['date'] = pd.to_datetime(ts['data'], dayfirst=True)
  
  if start is not None or end is not None:
    ts = ts[(ts['date']>=start) & (ts['date']<=end)].copy()
  else:
      pass

  ts.set_index('date', inplace=True)
  ts.drop('data', inplace=True, axis=1)
  return ts
  
def read_bacen_code(search_text: str) -> pd.core.frame.DataFrame:
    try:
        result = pd.read_csv('https://raw.githubusercontent.com/RPCastro07/Bacen_Time_Series_Codes/main/series_bacen_codes.csv', encoding='cp1252')
        result = result[result['NM_SERIE'].str.upper().str.contains(search_text.upper())].copy()
        return result
    
    except:
        print('Conecte-se à internet ou verifique se você tem acesso ao GitHub!')
    

