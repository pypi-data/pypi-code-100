from pyfund import constants, core
from pyfund.strategy import IStrategy, Operate
from rich import print


class Strategy(IStrategy):

    keys = [
        'operate',
        'irr',
        constants.I_DATE,
        constants.I_CLOSE,
        constants.I_CR_CLOSE,
        # constants.I_VOLUME,
        constants.I_CR_VOLUME,
        constants.I_CR_MACD,
        constants.I_CR_DEA,
        constants.I_KDJD,
        constants.I_CR_KDJD,
        constants.I_KDJJ,
        constants.I_MA5,
        constants.I_CR_MA5,
        constants.I_MA10,
        constants.I_CR_MA10,
        constants.I_MA20,
        constants.I_CR_MA20,
        constants.I_PE,
        constants.I_PB,
        constants.I_ROE,
        constants.I_BOLL
    ]

    flag1 = True # ma5上穿ma10
    flag2 = True # ma5上穿ma20

    def sell_all(self, data: core.Data):
        if self.num == 0:
            return Operate.NONE
        
        operate = Operate.NONE
        close = data.get(constants.I_CLOSE)
        ma5 = data.get(constants.I_MA5)
        ma10 = data.get(constants.I_MA10)
        ma20 = data.get(constants.I_MA20)

        # 买入后，亏损4%，直接清仓
        if (close - self.cost )/self.cost <= -0.4:
            print(data.get(constants.I_DATE), '买入后，亏损4%，直接清仓')
            operate = Operate.SELL_ALL

        # 已买入MA5上穿MA10，MA5上穿MA20；但没满仓
        # if self.flag1 is False and self.flag2 is False and self.num == 2:
        #     # MA20，连续跌2天，股价下跌，上涨动力不足。
        #     if data.get(constants.I_CR_MA20) <= -2 and data.get(constants.I_CR_CLOSE) < 0:
        #         print(data.get(constants.I_DATE), '买入2份，上涨动力不足，清仓')
        #         operate = Operate.SELL_ALL

        # 趋势确认，趋势不再，则清仓

        # 股价跌破10，清仓
        if ma10 > ma20 and close <= ma20:
            print(data.get(constants.I_DATE), '跌破MA20，清仓')
            operate = Operate.SELL_ALL

        # KDJD趋势变化，清仓
        if data.get(constants.I_CR_KDJD) < 0:
            print(data.get(constants.I_DATE), 'KDJD趋势反转，清仓')
            operate = Operate.SELL_ALL


        # 最大收益，跌破20%
        # max_close = max(self.closes)
        # 跌破最大收益20%
        # if close <= (max_close - self.fall_from_max*(max_close - self.cost)):
        #     print(data.get(constants.I_DATE), '跌破最大收益20%，清仓')
        #     operate = Operate.SELL_ALL

        if operate == Operate.SELL_ALL:
            self.flag1 = self.flag2 = True
        return operate

    def sell(self, data: core.Data):
        # 如果KDJD的趋势发生变化
        if data.get(constants.I_CR_KDJD) > 0:
            return Operate.NONE

        close = data.get(constants.I_CLOSE)

        # 跌破MA5，卖出1份
        if data.get(constants.I_MA5) < close:
            return Operate.SELL

        if data.get(constants.I_MA10) < close:
            return Operate.SELL

        # 跌破MA20，则清仓

    def buy_all(self, data):
        if super().buy_all(data) == Operate.NONE:
            return Operate.NONE
        
        ma5 = data.get(constants.I_MA5)
        ma10 = data.get(constants.I_MA10)
        ma20 = data.get(constants.I_MA20)

        # MA5,MA10朝上
        if data.get(constants.I_CR_MA5) < 0:
            return Operate.NONE
        # if data.get(constants.I_CR_MA10) < 0:
        #     return Operate.NONE
        
        if data.get(constants.I_CR_DEA) < 0:
            return Operate.NONE
        
        if data.get(constants.I_CR_KDJD) < 0:
            return Operate.NONE

        # if data.get(constants.I_CR_MA20) < 0:
        #     return Operate.NONE
        
        # MA5上穿MA10
        if ma5 > ma10:
            return Operate.NONE
        
        # MA10上穿MA20
        if ma10 >= ma20:
            return Operate.BUY_ALL

        print(data.get(constants.I_DATE), "MA5,MA10,MA20朝上, MA10上穿MA20，满仓")
        return Operate.BUY_ALL



        # def a(): # MA10上穿MA20
        #     # MA5穿10，20，已经买入
        #     if self.flag1:
        #         return Operate.NONE
        #     if self.flag2:
        #         return Operate.NONE

        #     # MA5,MA10,MA20朝上
        #     if data.get(constants.I_CR_MA5) < 0:
        #         return Operate.NONE
        #     if data.get(constants.I_CR_MA10) < 0:
        #         return Operate.NONE
        #     if data.get(constants.I_CR_MA20) < 0:
        #         return Operate.NONE
            
        #     # MA5大于MA10
        #     if ma5 < ma10:
        #         return Operate.NONE
            
        #     # MA10上穿MA20
        #     if ma10 >= ma20:
        #         return Operate.BUY_ALL

        # if a() == Operate.BUY_ALL:
        #     print(data.get(constants.I_DATE), "MA5,MA10,MA20朝上, MA10上穿MA20，满仓")
        #     return Operate.BUY_ALL

        # return Operate.NONE

        # 牛市判断，直接满仓执行
        # 5、10、20，3条MA线都向上。
        # if data.get(constants.I_CR_MA5) <= 0:
        #     return Operate.NONE
        # if data.get(constants.I_CR_MA10) <= 0:
        #     return Operate.NONE
        # if data.get(constants.I_CR_MA20) <= 0:
        #     return Operate.NONE

        # if data.get(constants.I_CR_KDJD) < 0:
        #     return Operate.NONE
        
        # if data.get(constants.I_CR_DEA) < 0:
        #     return Operate.NONE

        # if data.get(constants.I_MA10) > data.get(constants.I_MA20):
        #     return Operate.NONE

        # # 选择满仓买入后，不能再买
        # print(data.get(constants.I_DATE), "满仓买入")
        # return Operate.BUY_ALL


    def buy(self, data):
        return Operate.NONE
        # 操作、份额
        ma5 = data.get(constants.I_MA5)
        ma10 = data.get(constants.I_MA10)
        ma20 = data.get(constants.I_MA20)

        # 第一步
        # MA5趋势向上 MA5上穿MA10(只能买一次，第二次不能再买)
        if self.flag1 and data.get(constants.I_CR_MA5) > 0 and ma5 > ma10 and ma5 < ma20:
            print(data.get(constants.I_DATE), "MA5趋势向上 MA5上穿MA10，买入")
            self.flag1 = False
            return Operate.BUY

        # 第二步
        # if self.num == 0: # 第一步，已经买入了一份。
        #     return Operate.NONE

        # MA5、MA10的趋势向上，MA5上穿MA20(只能买一次，第二次不能再买)
        # if self.flag2 and data.get(constants.I_CR_MA5) > 0 and data.get(constants.I_CR_MA10) > 0:
        #     if ma5 > ma20 and ma20 > ma10:
        #         print(data.get(constants.I_DATE), "MA5、MA10的趋势向上，MA5上穿MA20，买入")
        #         self.flag2 = False
        #         return Operate.BUY
        
        return Operate.NONE

        # MA10上穿MA20 - 满仓

# 的策略
#　能否同时执行多个策略？
# 通常买入策略，对应了卖出策略
# 以MA20为基础的买卖策略。
# 5>10>20，并都向上。

# 这种情况，牛市模式开启。
# 果断满仓，不跌破MA20，绝对不卖出。
# 牛市KDJ会失真。
# 均线+MACD+BOLL
