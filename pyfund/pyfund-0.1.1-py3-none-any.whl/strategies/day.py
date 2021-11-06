""" 日线策略 """

from pyfund import constants, core
from pyfund.strategy import IStrategy, Operate
from rich import print


class Strategy(IStrategy):

    keys = [
        'operate',
        'irr',
        constants.I_DATE,
        constants.I_OPEN,
        constants.I_CLOSE,
        constants.I_CR_CLOSE,
        constants.I_MACD,
        constants.I_CR_MACD,
        constants.I_DEA,
        constants.I_CR_DEA,
        constants.I_DIF,
        constants.I_CR_DIF,
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

    flag1 = True  # ma5上穿ma10
    flag2 = True  # ma5上穿ma20

    def __init__(self):
        super().__init__()
        self.name = 'day'

    def sell_all(self, data: core.Data):
        if self.num == 0:
            return Operate.NONE

        operate = Operate.NONE
        close = data.get(constants.I_CLOSE)
        ma5 = data.get(constants.I_MA5)
        ma10 = data.get(constants.I_MA10)
        ma20 = data.get(constants.I_MA20)

        # 买入后，亏损4%，直接清仓
        if (close - self.cost)/self.cost <= -0.4:
            print(data.get(constants.I_DATE), '买入后，亏损4%，直接清仓')
            operate = Operate.SELL_ALL

        dif = data.get(constants.I_DIF)
        dea = data.get(constants.I_DEA)
        cr_dea = data.get(constants.I_CR_DEA)
        cr_dif = data.get(constants.I_CR_DIF)
        macd = data.get(constants.I_MACD)
        cr_macd = data.get(constants.I_CR_MACD)
        boll = data.get(constants.I_BOLL)

        if cr_dea < 0 and cr_dif < 0:
            if dea > dif:
                operate = Operate.SELL_ALL
        # dif = data.get(constants.I_CR_DIF)
        # if dif < 0:
        #     if close < ma5:
        #         print(data.get(constants.I_DATE), '清仓')
        #         operate = Operate.SELL_ALL

        return operate

    def sell(self, data: core.Data):
        return Operate.NONE

    def buy_all(self, data):
        if super().buy_all(data) == Operate.NONE:
            return Operate.NONE

        ma5 = data.get(constants.I_MA5)
        ma10 = data.get(constants.I_MA10)
        ma20 = data.get(constants.I_MA20)
        dif = data.get(constants.I_DIF)
        dea = data.get(constants.I_DEA)
        cr_dea = data.get(constants.I_CR_DEA)
        cr_dif = data.get(constants.I_CR_DIF)
        macd = data.get(constants.I_MACD)
        cr_macd = data.get(constants.I_CR_MACD)
        boll = data.get(constants.I_BOLL)

        if macd < 0:
            return Operate.NONE

        if boll >= 0.95:
            return Operate.NONE

        if cr_macd < 0:
            return Operate.NONE

        if dif < 0 or dea < 0:
            return Operate.NONE

        if dif >= dea:
            if cr_dif > 1 and cr_dea > 1:
                return Operate.BUY_ALL
        # if data.get(constants.I_KDJD) >50:
        #     return Operate.NONE

        # if data.get(constants.I_CR_DIF) == 1:
        #     if data.get(constants.I_CLOSE) > ma5:
        #         return Operate.BUY_ALL

        # TODO 增加PE百分位
        # TODO 增加PB百分位

    def buy(self, data):
        pass
