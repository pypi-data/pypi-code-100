"""策略"""
import abc
from enum import Enum

import pandas as pd
from rich import print

import pyfund
from pyfund import constants, core
from pyfund.net.xueqiu import Period


class Operate(Enum):
    BUY = 1  # 买入一份
    BUY_ALL = 2  # 满仓买入
    SELL = 3  # 卖出1份
    SELL_ALL = 4  # 卖出全部
    NONE = 5  # 无操作


class IStrategy(abc.ABC):

    keys = [
        constants.I_DATE,
        constants.I_CLOSE,
        constants.I_OPEN,
    ]

    def __init__(self):
        self.result = pd.DataFrame(columns=self.keys)
        self.name = self.__class__.__name__

        self.start_date = None
        self.end_date = None

        self.__is_full = False # 满仓标记

        self.cost = 0  # 成本价
        self.num = 0  # 持有份额
        self.market_value = 0  # 　市值，为了方便计算成本价
        self.irr = None  # 收益率
        self.sell_logs = []  # 卖出记录

        # 用于清仓策略，从最高处下跌20%。
        self.max_boll = False  # 买入后，BOLL线是否突破up
        self.max_close = 0  # 买入后最高估计
        self.fall_from_max = 0.2  # 从最高处下跌20%

        # 记录买入后的每日收盘价
        self.closes = []

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_period(self, period: Period):
        self.period = period
    
    @property
    def is_full(self):
        return self.__is_full

    @is_full.setter
    def is_full(self, value):
        self.__is_full = value

    def _reset(self):
        self.cost = 0
        self.num = 0
        self.market_value = 0
        self.irr = None
        self.sell_logs.clear()
        self.max_boll = False
        self.max_close = 0
        self.closes.clear()

    def execute(self, datas):
        b = 0.2
        buys = []
        for item in datas:
            date = item.get(constants.I_DATE)
            if self.start_date is not None:
                if self.start_date > date:
                    continue
            if self.end_date is not None:
                if self.end_date < date:
                    continue

            operate = self._trading(self._judge(item), item)
            l = item.to_list(self.keys[2:])
            l.insert(0, operate.name)
            l.insert(1, self.irr)
            self.result.loc[len(self.result)] = l

            if operate == Operate.SELL_ALL:
                self._reset()
        return self.result

    def _trading(self, operate, data):
        """执行交易操作，控制仓位

        :param operate: [description]
        :type operate: [type]
        :param data: [description]
        :type data: [type]
        :return: [description]
        :rtype: [type]
        """
        self.irr = 0  # 每次统计都重置
        close = data.get(constants.I_CLOSE)
        open = data.get(constants.I_OPEN)

        if operate == Operate.BUY:
            self.market_value += open
            self.num += 1
            self.cost = self.market_value/self.num
        elif operate == Operate.BUY_ALL:
            self.market_value += open*(10-self.num)
            self.num = 10
            self.cost = self.market_value/self.num   
            self.is_full = True
        elif operate == Operate.SELL:
            if self.num > 0:
                self.sell_logs.append([self.cost, open])
                self.irr = (open-self.cost)/self.cost
                self.market_value -= open
                self.num -= 1
        elif operate == Operate.SELL_ALL:
            if self.num > 0:
                self.sell_logs.append([self.cost*self.num, open*self.num])
                a = 0
                b = 0
                for item in self.sell_logs:
                    a += item[0]
                    b += item[1]
                if a > 0:
                    self.irr = (b-a)/a
                self.is_full = False
            else:
                operate = Operate.NONE

        if self.num > 0:
            self.closes.append(close)
            # if data.get(constants.I_BOLL) >= 1:  # 股价突破BOLL线UP
            #     self.max_boll = True

        return operate

    def _judge(self, data: core.Data):
        """操作判断"""
        op = self.sell_all(data)
        if op == Operate.SELL_ALL:
            return op

        op = self.sell(data)
        if op == Operate.SELL:
            return op

        op = self.buy_all(data)
        if op == Operate.BUY_ALL:
            return op

        op = self.buy(data)
        if op == Operate.BUY:
            return op

        return Operate.NONE

    @abc.abstractmethod
    def sell_all(self, date: core.Data) -> Operate:
        """清仓策略

        :param date: 股票数据
        :type date: core.Data
        :return: 操作
        :rtype: Operate
        """
        pass

    @abc.abstractmethod
    def sell(self, date: core.Data) -> Operate:
        """卖出策略

        :param date: 股票数据
        :type date: core.Data
        :return: 操作
        :rtype: Operate
        """
        pass


    @abc.abstractmethod
    def buy(self, date: core.Data) -> Operate:
        """买入策略

        :param date: 股票数据
        :type date: core.Data
        :return: 操作
        :rtype: Operate
        """
        pass


    def buy_all(self, date: core.Data) -> Operate:
        """满仓策略

        :param date: 股票数据
        :type date: core.Data
        :return: 操作
        :rtype: Operate
        """
        pass