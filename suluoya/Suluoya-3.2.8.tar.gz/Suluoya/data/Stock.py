import concurrent.futures
import datetime
import os
import re
import sys
import time

import baostock as bs
import pandas as pd
import pretty_errors
import requests
from tqdm import tqdm, trange

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.log import hide, show, slog, sprint
except:
    from log.log import hide, show, slog, sprint


def get_data(rs):
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    return pd.DataFrame(data_list, columns=rs.fields)


def login():
    hide()
    bs.login()
    show()


class StockData(object):
    '''
    股票数据\n
    names=['贵州茅台', '隆基股份', '五粮液']\n
    start_date='2019-01-01'\n
    end_date='2020-01-01'\n
    adjustflag='3' -->默认不复权
    '''

    def __init__(self, names=['贵州茅台', '隆基股份'],
                 start_date='2019-12-01', end_date='2020-12-31',
                 adjustflag='3'):
        self.names = names
        self.start_date = start_date
        self.end_date = end_date
        self.adjustflag = adjustflag  # 默认不复权
        login()

    def logout(self):
        '''
        退出
        '''
        hide()
        bs.logout()
        show()

    def stocks_info(self):
        '''
        Return a dict containing stock names, codes and ipoDate\n
        {
            '贵州茅台': {'code': 'sh.600519', 'ipoDate': '2001-08-27'},
            '隆基股份': {'code': 'sh.601012', 'ipoDate': '2012-04-11'},
            ...
        }
        '''
        info = {}
        sprint('Loading stocks information...')
        for name in tqdm(self.names):
            rs = bs.query_stock_basic(code_name=name)
            stock_info = get_data(rs)
            info[name] = {'code': stock_info['code'][0],
                          'ipoDate': stock_info['ipoDate'][0]}
        return info

    def stocks_data(self, info='date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST'):
        '''
        Return a DataFrame containing all the stocks data\n
        戳下面这个链接\n
        http://baostock.com/baostock/index.php/A股K线数据
        '''
        stocks_info = self.stocks_info()
        df_list = []
        sprint('Loading stocks data...')
        for name in tqdm(self.names):
            code = stocks_info[name]['code']
            if stocks_info[name]['ipoDate'] > self.start_date:
                sprint(
                    f"{name}'s ipo date is {stocks_info[name]['ipoDate']}, which is after {self.start_date}.")
            rs = bs.query_history_k_data_plus(code,
                                              info,
                                              start_date=self.start_date, end_date=self.end_date,
                                              frequency='d', adjustflag=self.adjustflag)
            df = get_data(rs)
            df['name'] = name
            df_list.append(df)
        df = pd.concat(df_list).apply(pd.to_numeric, errors='ignore')
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df

    def stocks_valuation(self):
        '''
        Return a DataFrame containing all the stocks valuation data \n
        (date, code, close, peTTM, pbMRQ, psTTM, pcfNcfTTM)\n
        戳下面这个链接\n
        http://baostock.com/baostock/index.php/估值指标(日频)
        '''
        stocks_info = self.stocks_info()
        df_list = []
        sprint('Loading stocks valuation data...')
        for name in tqdm(self.names):
            code = stocks_info[name]['code']
            rs = bs.query_history_k_data_plus(code,
                                              "date,code,close,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                                              start_date=self.start_date, end_date=self.end_date,
                                              frequency='d', adjustflag=self.adjustflag)
            df = get_data(rs)
            df['name'] = name
            df_list.append(df)
        df = pd.concat(df_list).apply(pd.to_numeric, errors='ignore')
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df


class ConstituentStocks(StockData):
    def __init__(self):
        hide()
        bs.login()
        show()

    def stock_industry(self):
        '''
        Return a DataFrame containing all stock industry data\n
        戳下面这个链接\n
        http://baostock.com/baostock/index.php/行业分类
        '''
        return get_data(bs.query_stock_industry())

    def sz50(self):
        '''上证50'''
        return get_data(bs.query_sz50_stocks())

    def hs300(self):
        '''沪深300'''
        return get_data(bs.query_hs300_stocks())

    def zz500(self):
        '''中证500'''
        return get_data(bs.query_zz500_stocks())


def GetGoodStock(page=5):
    sprint('getting data from http://fund.eastmoney.com/data/rankhandler.aspx')
    url = "http://fund.eastmoney.com/data/rankhandler.aspx"
    headers = {
        "Host": "fund.eastmoney.com",
        "Referer": "http://fund.eastmoney.com/data/fundranking.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63"
    }
    urls = []

    def get_urls(page):
        params = {
            "op": "ph",
            "sc": "6yzf",
            "sd": '2021-03-11',
            "ed": '2021-03-11',
            "pi": str(page),
            "dx": "1",
        }
        response = requests.get(url, headers=headers, params=params)
        response.encoding = response.apparent_encoding
        data = re.findall('var rankData = {datas:(.*),allRe', response.text)[0]
        data = eval(data)
        list = ['http://fund.eastmoney.com/' +
                re.findall(r'(\d*),', i)[0]+'.html' for i in data]
        for i in list:
            urls.append(i)
    for i in range(1, page+1):
        get_urls(i)

    def get_stock(url):
        df = pd.read_html(url)
        return df[5][['股票名称', '持仓占比']]

    stocks = []

    def main(url):
        stocks.append(get_stock(url))

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for url in urls:
            sprint(url)
            executor.submit(main, url)

    stock = pd.concat(stocks)
    stock['持仓占比'] = stock['持仓占比'].map(lambda x: x.replace('%', ''))
    stock = stock.replace('暂无数据', 0)
    stock['持仓占比'] = stock['持仓占比'].astype('float')
    group = stock.groupby('股票名称')
    df1 = group.mean()
    df2 = group.count()
    df1 = df1.rename(columns={'持仓占比': '平均持仓占比'})
    df2 = df2.rename(columns={'持仓占比': '出现次数'})
    df = pd.merge(df1, df2, how='outer', on='股票名称')
    df = df.sort_values(by='出现次数', ascending=False)
    return df


if __name__ == '__main__':
    GetGoodStock(3)
    cs = StockData(names=['贵州茅台'], start_date='2021-01-28',
                   end_date='2021-09-28')
    test = cs.stocks_data()
    print(test)
