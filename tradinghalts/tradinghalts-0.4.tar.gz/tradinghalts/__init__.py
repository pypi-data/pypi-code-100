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

def Insight(ticker):
    if type(ticker) != str:
        raise Exception("Please pass in a string")
    _ticker = ticker.upper()
    fb = firebase.FirebaseApplication("https://tradinghalts-467f9-default-rtdb.firebaseio.com/", None)
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

