import math
import os
import random
import sys
import time
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pretty_errors
import scipy.optimize as sco
from tqdm import tqdm, trange

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
try:
    from ..log.log import slog, sprint, hide, show, progress_bar
    from ..data.Stock import StockData
except:
    from log.log import slog, sprint, hide, show, progress_bar
    from data.Stock import StockData


class Markovitz(object):
    '''
    组合投资权重\n
    names=['贵州茅台', '隆基股份', '五粮液']\n
    start_date='2019-01-01'\n
    end_date='2020-01-01'\n
    no_risk_rate=0.0185\n
    funds=10000000
    '''

    def __init__(self, names=['贵州茅台', '隆基股份', '五粮液'],
                 start_date='2019-01-01',
                 end_date='2020-01-01',
                 no_risk_rate=0.0185,
                 funds=10000000):
        self.names = names
        self.lens = len(names)
        self.start_date = start_date
        self.end_date = end_date
        self.no_risk_rate = no_risk_rate
        self.funds = funds
        sprint('Please make sure that all of the stocks are in the market!')
        sprint('Initializing...')
        global StockData
        StockData = StockData(names=self.names, start_date=self.start_date,
                              end_date=self.end_date)
        self.data = StockData.stocks_data()
        self.date = list(map(lambda x: str(x)[:10], self.data.date.unique()))
        self.first_date = self.date[0]
        self.last_date = self.date[-1]
        self.first_price = self.data[self.data.date == self.data.date.unique(
        )[0]][['open', 'name']].set_index('name').to_dict()['open']
        self.last_price = self.data[self.data.date == self.data.date.unique(
        )[-1]][['close', 'name']].set_index('name').to_dict()['close']
        self.flag = True

    def weights(self, number=5000):
        # 股票随机权重
        return np.random.dirichlet(np.ones(self.lens), size=number)

    def calculate(self):
        data = self.data[['date', 'name', 'pctChg']]
        # 收益率均值
        data_mean = data.groupby('name').mean().T
        # 收益率协方差矩阵
        data_cov = pd.DataFrame()
        for name in self.names:
            data_cov[name] = data[data['name'] == name]['pctChg']
        data_cov = data_cov.cov()
        return data_mean, data_cov

    def scatter_data(self, number=5000):
        '''散点数据，默认生成5000个
        '''
        data_mean, data_cov = self.calculate()
        # 随机权重
        weights = self.weights(number=number)
        # 收益率
        rate = data_mean.dot(weights.T).T
        # 方差
        risk = np.sqrt(np.diagonal(weights.dot(data_cov).dot(weights.T)))
        # 散点
        df_scatter = pd.DataFrame()
        df_scatter['weights'] = pd.Series(map(lambda x: str(x), weights))
        df_scatter['risk'] = risk
        df_scatter['rate'] = rate['pctChg']
        # 夏普比率
        df_scatter['sharpe'] = (
            df_scatter.rate-self.no_risk_rate)/df_scatter.risk
        return df_scatter

    def max_sharpe(self, weights):
        '''
        计算夏普比率
        '''
        data_mean, data_cov = self.calculate()
        weights = np.array(weights)
        rate = data_mean.dot(weights.T)['pctChg']
        risk = np.sqrt(weights.dot(data_cov).dot(weights.T))
        return (self.no_risk_rate-rate)/risk  # 相反数

    def shares_numbers(self):
        '''
        股票手数（不取整）
        '''
        df = pd.DataFrame(columns=['price', 'weight'])
        df['weight'] = pd.Series(self.optimization()[1])
        df['price'] = pd.Series(self.last_price)
        df['shares'] = (self.funds*df['weight'])/(df['price']*100)
        self.shares_number = df
        return df

    def optimization(self):
        '''
        非线性规划找出最大夏普比率
        '''
        opts = sco.minimize(fun=self.max_sharpe,
                            x0=np.ones(self.lens)/self.lens,
                            bounds=tuple((0, 1)for x in range(self.lens)),
                            constraints={'type': 'eq',
                                         'fun': lambda x: np.sum(x) - 1}
                            )
        return -opts.fun, dict(zip(self.names, list(opts.x)))

    def adjacent_combination(self, shares):
        ceils = [math.ceil(i) for i in shares.values()]
        floors = [math.floor(i) for i in shares.values()]
        result = np.array(list(zip(ceils, floors)))
        df_shares = pd.DataFrame(list(product(*result)), columns=self.names)
        return df_shares

    def search(self):
        df = self.shares_numbers()[['price', 'shares']]
        weights = df['shares']*(100*df['price'])/self.funds
        max_sharpe = -self.max_sharpe(weights=weights)
        df_shares = self.adjacent_combination(shares=df['shares'].to_dict()).T
        df_search = df_shares.T
        sharpe_list = []
        for i in range(0, 2**self.lens):
            weights = df_shares[i]*(100*df['price'])/self.funds
            sharpe_list.append(-self.max_sharpe(weights=weights))
        df_search['sharpe'] = sharpe_list
        df_search['<max_sharpe'] = df_search['sharpe'] <= max_sharpe
        df_search = df_search.sort_values(by='sharpe', ascending=False)
        self.original_max_sharpe = max_sharpe
        return df_search

    def exam_search(self, exam_shares):
        df = self.shares_number[['price', 'shares']]
        weights = exam_shares*(100*df['price'])/self.funds
        exam_max_sharpe = -self.max_sharpe(weights=weights)
        exam_shares_list = list(exam_shares)
        exam_lists = []
        for i in range(0, self.lens):
            lists = exam_shares_list.copy()
            lists[i] += 1
            exam_lists.append(lists)
        df_exam = pd.DataFrame(exam_lists, columns=self.names)
        sharpe_list = []
        for exam in exam_lists:
            weights = exam*(100*df['price'])/self.funds
            sharpe_list.append(-self.max_sharpe(weights=weights))
        df_exam['sharpe'] = sharpe_list
        df_exam['cost'] = 0
        for i in df[['price']].itertuples():
            name = i.Index
            price = i.price
            df_exam[f'{name}_cost'] = (df_exam[name]*price*100).astype(int)
            df_exam['cost'] += df_exam[f'{name}_cost']
        df_exam['>=exam_max_sharpe'] = df_exam['sharpe'] >= exam_max_sharpe
        df_exam['<=max_sharpe'] = df_exam['sharpe'] <= self.original_max_sharpe
        df_exam['cost<funds'] = df_exam['cost'] <= self.funds
        df_exam['all'] = df_exam['>=exam_max_sharpe'] & \
            df_exam['<=max_sharpe'] & df_exam['cost<funds']
        df_exam = df_exam.sort_values(by='sharpe', ascending=False)
        return df_exam

    def exam_shares_cycle(self):
        df_search = self.search()
        exam_shares = df_search[df_search['<max_sharpe']
                                == True][self.names]
        lists = []
        for i, j in exam_shares.iterrows():
            exam_share = self.exam_search(exam_shares=j)
            exam_share = exam_share[exam_share['all']
                                    == True][self.names]
            lists.append(exam_share)
        return pd.concat(lists)

    def circle(self, exam_shares):
        exam_list = []
        for i, exam_share in exam_shares.iterrows():
            result = self.exam_search(exam_shares=exam_share)
            exam_list.append(result)
        if not exam_list:
            self.flag = False
            return pd.DataFrame(columns=self.names)
        df = pd.concat(exam_list)
        df = df.drop_duplicates()
        df = df[df['all'] == True]
        if df.empty:
            self.flag = False
        return df

    def tree(self):
        '''分支检验
        '''
        results = []
        sprint('Calculate the optimal number of stocks...')
        for exam_shares in progress_bar(self.exam_shares_cycle()):
            df_exam = self.exam_search(exam_shares=exam_shares)
            exam_shares = df_exam[df_exam['all'] == True][self.names]
            while True:
                exam_shares_last = exam_shares
                print(exam_shares_last)
                exam_shares = self.circle(exam_shares=exam_shares[self.names])
                if not self.flag:
                    results.append(exam_shares_last)
                    break
            self.flag = True
        return pd.concat(results).sort_values(by='sharpe', ascending=False).iloc[0]

    def optimal_weight(self):
        '''
        计算最优权重
        '''
        sharpe_value, weights_dict = self.optimization()
        weights_dict['sharpe'] = sharpe_value
        return pd.Series(weights_dict)

    def buy(self):
        '''股票购买数量（整数）
        '''
        items = self.names+['sharpe', 'cost'] + \
            list(map(lambda x: x+'_cost', self.names))
        return self.tree()[items]

    def font_scatter_data(self, number=500):
        '''边界散点数据，默认生成500个
        '''
        scatter_data = self.scatter_data()
        data_mean, data_cov = self.calculate()
        scatter_list = []
        sprint('Searching for boundary scatter...')
        for i in trange(number):
            i
            random_rate = random.uniform(
                scatter_data.rate.min(), scatter_data.rate.max())
            constraints = ({'type': 'eq', 'fun': lambda weights: weights.sum()-1},
                           {'type': 'eq', 'fun': lambda weights: data_mean.dot(weights.T)['pctChg']-random_rate})
            opts = sco.minimize(fun=lambda weights: weights.dot(data_cov).dot(weights.T),
                                x0=np.ones(self.lens)/self.lens,
                                bounds=tuple((0, 1)for x in range(self.lens)),
                                constraints=constraints
                                )
            scatter_list.append([opts.x,  np.sqrt(opts.fun), random_rate])
        scatter_df = pd.DataFrame(scatter_list, columns=[
                                  'weights', 'risk', 'rate'])
        scatter_df['sharpe'] = (
            scatter_df.rate-self.no_risk_rate)/scatter_df.risk
        return scatter_df

    def drawing(self):
        '''散点图
        '''
        max_sharpe = self.optimization()[0]
        scatter_data = self.scatter_data()
        font_scatter_data = self.font_scatter_data(number=500)
        sprint(f'max sharpe: {max_sharpe}')
        plt.scatter(scatter_data.risk, scatter_data.rate, s=10)
        plt.scatter(font_scatter_data.risk, font_scatter_data.rate, s=10)
        plt.axline(xy1=(0, self.no_risk_rate), slope=max_sharpe)
        plt.xlabel('Risk')
        plt.ylabel('Yield')
        plt.show()


if __name__ == '__main__':
    mk = Markovitz(names=[
        '药明康德',
        '比亚迪',
        '山西汾酒',
        '科沃斯',
        '紫金矿业',
    ],  # 股票组合
        start_date='2020-10-17',  # 开始日期
        end_date='2021-10-17',  # 结束日期
        no_risk_rate=0.023467,  # 无风险利率
        funds=10000000  # 最大资金限制
    )
    # buy = mk.buy()
    # print(buy)
    ow = mk.optimal_weight().map(lambda x: round(x, 4))
    print(ow)
