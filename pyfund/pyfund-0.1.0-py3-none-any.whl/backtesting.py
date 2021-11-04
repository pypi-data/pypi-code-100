from rich import print

from pyfund import constants, log, strategy, to_per
from pyfund.core import DataProcessor
from pyfund.net.xueqiu import Period
from pyfund.strategy import IStrategy


class BackTesting:

    @log
    def __init__(self):
        self.logs = []
        self.buys = []
        self.sells = []
        self.trading_records = []
        self.boll_break_100 = False  # 布林线破100，则设置为True，开始执行卖出操作；清仓后，重置

    @log
    def load_datas(self, code, period: Period):
        self.code = code
        self.dp = DataProcessor(code, period)
        self.datas = self.dp.get_all()

    @log
    def load_strategy(self, strategy: IStrategy):
        self.strategy = strategy

    @log
    def set_start_date(self, start_date):
        self.strategy.set_start_date(start_date)

    @log
    def set_end_date(self, end_date):
        self.strategy.set_end_date(end_date)

    @log
    def run(self):
        result = self.strategy.execute(self.datas)
        self._handle(result)

    def _handle(self, result):
        result.to_csv(self.code + '_' + self.strategy.name + ".csv")

        line = result.values[-1]

        wins = 0
        loss = 0
        earn = 0
        irrs = []
        for _, item in result.iterrows():
            if item['operate'] == strategy.Operate.SELL_ALL.name:
                earn += item['irr']
                if earn > 0:
                    wins += 1
                    if constants.IS_DEBUG:
                        print(item['date'], 'win', to_per(earn))
                elif earn < 0:
                    if constants.IS_DEBUG:
                        print(item['date'], 'loss', to_per(earn))
                    loss += 1

                irrs.append(earn)  # 用于计算平均收益率
                earn = 0

        wr = 0
        irr = 0
        if (wins+loss) > 0:
            wr = to_per(wins/(wins+loss))
        # 日期 代码 名称 策略 胜率 收益率 操作
            irr = to_per(sum(irrs))
        # if 'NONE' in line[0]:
        #     return
        # if 'SELL' in line[0]:
        #     return
        print('{} {} {} {} WR{} {} {}'.format(
            line[2], self.code, self.dp.name, self.strategy.name, wr, irr, line[0]))
