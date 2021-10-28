import pandas as pd
import numpy as np
from pandas.io.parsers import read_csv
import yfinance as yf
import datetime

from os.path import exists
import os


class Project():
    def __init__(self) -> None:
        start_stream = datetime.datetime(2018,1,1)
        end_stream = datetime.datetime(2020,10,1)
        # downloading Apple adj closes
        s = 'AAPL'
        print("[] downloading\t -> ", end = "")

        # not downloading everytime to avoid request ban from yfinance APIs
        if exists('./data/AAPL_data.csv'):
            self.data = read_csv('./data/AAPL_data.csv')
        else:
            if not exists('./data/'):
                os.mkdir('./data/')
            self.data = yf.download(s, start = start_stream, end = end_stream)
            self.data.to_csv('./data/AAPL_data.csv')
        print("Done")

    def get_data_adj(self):
        df = pd.read_csv('./data/AAPL_data.csv', index_col=0)
        return df['Adj Close']
    
    def get_data_volume(self):
        df = pd.read_csv('./data/AAPL_data.csv', index_col=0)
        return df['Volume']


def compute_CC():
    downloader = Project()
    df_adj = downloader.get_data_adj()

    df_adj.index = pd.to_datetime(df_adj.index)
    df_adj_op = df_adj.groupby(pd.Grouper(freq = 'D')) # using monthly aggregation
    df_adj = df_adj_op.mean()   # aggregate by average
    df_returns = np.log(df_adj/df_adj.shift(1)) # calculating CC returns
    df_returns.name = 'Apple CC Returns'

    # returning while dropping na values
    return df_returns.dropna()



if __name__ == "__main__":
    # excecuted to check if everything in the software works correctly
    # print('Creating Project')
    main = Project()
    print('Created')
    
    # adj = main.get_data_adj()
    # print(adj)
    # vol = main.get_data_volume()
    # print(vol)
