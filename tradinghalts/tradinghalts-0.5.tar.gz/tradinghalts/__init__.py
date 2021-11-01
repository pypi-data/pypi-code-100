from datetime import datetime
from datetime import timedelta
from math import sqrt
import pandas as pd
import numpy as np
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pickle
from firebase import firebase

#python_jwt
#gcloud
#sseclient
#pycryptodome
#requests_toolbelt

fb = firebase.FirebaseApplication("https://tradinghalts-467f9-default-rtdb.firebaseio.com/", None)

def Insight(ticker):
    if type(ticker) != str:
        raise Exception("Please pass in a string")
    _ticker = ticker.upper()
    read = fb.get('/tradinghalts-467f9-default-rtdb/Halts/CurrentInsights', '')
    insight_dict=list(read.values())[0]
    dict_tickers = list(insight_dict.keys())
    if ticker not in dict_tickers:
        raise Exception("Please input a valid ticker")
        
    insight_ticker = insight_dict[_ticker]
    insight_ticker[0] = datetime.strptime(insight_ticker[0], '%Y-%M-%d')
    insight_ticker[1] = float(insight_ticker[1])
    insight_ticker[2] = int(insight_ticker[2])
    
    final_insight = pd.DataFrame()
    final_insight[ticker] = insight_ticker
    final_insight = final_insight.T
    final_insight.columns = ["Date", "Volatility", "Insight"]
    return final_insight

def History(ticker, offset):
    if offset > 350 or offset < 10:
        raise Exception("Please enter less than 350 days")
    
    _ticker = ticker.upper()
    read = fb.get('/tradinghalts-467f9-default-rtdb/Halts/MultiInsights', '')
    insight_dict=list(read.values())[0]
    dict_tickers = list(insight_dict.keys())
    if _ticker not in dict_tickers:
        raise Exception("Please input a valid ticker")

    insight_ticker = insight_dict[_ticker]
    
    string_vol = insight_ticker[1][1:-1].split(',')
    insight_ticker[1] = list(np.asarray(string_vol, dtype=np.float64, order='C'))

    string_pred = insight_ticker[2][1:-1].split(',')
    insight_ticker[2] = list(np.asarray(string_pred, dtype=np.int64, order='C'))

    curDate = insight_ticker[0]
    insight_ticker[0] = [datetime.strptime(curDate, '%Y-%m-%d')-timedelta(days=(len(insight_ticker[2])-x)) for x in range(0, len(insight_ticker[2]))]

    final_insight = pd.DataFrame()
    final_insight["Date"] = insight_ticker[0]
    final_insight["Volatility"] = insight_ticker[1]
    final_insight["Insight"] = insight_ticker[2]
    ticker_values = [_ticker for x in range(0,len(insight_ticker[0]))]

    final_insight = pd.DataFrame(zip(ticker_values, insight_ticker[0], insight_ticker[1], insight_ticker[2]), columns=['Ticker', 'Date', 'Volatility', 'Insight'])
    final_insight =  final_insight.set_index(['Ticker', 'Date'], inplace=False)
    return final_insight