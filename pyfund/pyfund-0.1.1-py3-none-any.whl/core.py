import abc
import os.path

import arrow
import numpy as np
import pandas as pd
from rich import print

from pyfund import constants, to_per, log
from pyfund.net import xueqiu


class Data:

    def generate_method(self, d):
        _keys = set(['Unnamed: 0', 'ma20.1', 'hold_volume_cn', 'hold_ratio_cn',
                     'net_volume_cn', 'hold_volume_hk', 'hold_ratio_hk', 'net_volume_hk',
                     'balance', 'volume_post', 'amount_post'])
        for k, v in d.items():
            if k in _keys:
                continue
            if k == 'timestamp':
                self.__dict__['date'] = str(arrow.get(d[k]).date())
                continue
            self.__dict__[k] = v

    def get(self, key):
        if hasattr(self, key):
            return getattr(self, key)

    def to_list(self, keys):
        if keys is None:
            keys = self.__dict__.keys()
        l = []
        for key in keys:
            l.append(getattr(self, key))
        return l


class DataProcessor:
    # 大批量过滤器，这些东西，本质上只是一堆数据，可以考虑存放成cvs文件，后续直接读取。
    # 无需使用网络
    def __init__(self, code, period: xueqiu.Period):
        self.code = code
        self.path = os.path.join(constants.DATA_PATH, code + '_' + period.value + '.csv')
        self.xq = xueqiu.XueQiu()
        self.period = period

        data = self.xq.quote(self.code).get('data', {})
        quoto = data.get('quote', {})
        self.name = quoto.get('name')

        self._init()

        self.xq.close()

    @log
    def _init(self):
        if not os.path.exists(self.path):
            self._init_from_net()
        self.df = pd.read_csv(self.path)

    @log
    def _init_from_net(self):
        begin = arrow.now().date()
        df = self.xq.kline(self.code, begin, self.period)
        df.to_csv(self.path)

    @log
    def clean_cache(self):
        os.remove(self.path)

    @log
    def get_last_day(self) -> Data:
        """获取最后一天的数据

        Returns:
            Data: [description]
        """
        return self.get_all()[-1]

    @log
    def get(self, date: str) -> Data:
        for item in self.get_all():
            if item.get(constants.I_DATE) == date:
                return item

    @log
    def get_all(self) -> list:
        datas = []

        cr_volume = 0
        cr_close = 0
        cr_kdjd = 0
        cr_ma5 = 0
        cr_ma10 = 0
        cr_ma20 = 0
        cr_macd = 0
        cr_dea = 0
        cr_dif = 0

        last_volume = 0
        last_close = 0
        last_kdjd = 0
        last_ma5 = 0
        last_ma10 = 0
        last_ma20 = 0
        last_macd = 0
        last_dea = 0
        last_dif = 0
        macdx = 0 # 金叉指示器 高位金叉1，低位金叉-1，无金叉0

        is_first = True

        for _, item in self.df.iterrows():
            ma5 = item[constants.I_MA5]
            ma10 = item[constants.I_MA10]
            ma20 = item[constants.I_MA20]
            volume = item[constants.I_VOLUME]
            close = item[constants.I_CLOSE]
            kdjd = item[constants.I_KDJD]
            macd = item[constants.I_MACD]
            dea = item[constants.I_DEA]
            dif = item[constants.I_DIF]

            per = np.nan
            ub = item[constants.I_UB]
            if ub is not None and not np.isnan(ub):
                lb = item[constants.I_LB]
                per = (close - lb)/(ub-lb)

            d = Data()
            d.generate_method(item)
            datas.append(d)

            if is_first:
                is_first = False
            else:
                if not pd.isnull(volume):
                    if last_volume < volume:
                        cr_volume = 1 if cr_volume < 0 else cr_volume + 1
                    else:
                        cr_volume = -1 if cr_volume > 0 else cr_volume - 1
                if not pd.isnull(close):
                    if last_close < close:
                        cr_close = 1 if cr_close < 0 else cr_close + 1
                    else:
                        cr_close = -1 if cr_close > 0 else cr_close - 1
                if not pd.isnull(kdjd):
                    if last_kdjd < kdjd:
                        cr_kdjd = 1 if cr_kdjd < 0 else cr_kdjd + 1
                    else:
                        cr_kdjd = -1 if cr_kdjd > 0 else cr_kdjd - 1
                if not pd.isnull(ma5):
                    if last_ma5 < ma5:
                        cr_ma5 = 1 if cr_ma5 < 0 else cr_ma5 + 1
                    else:
                        cr_ma5 = -1 if cr_ma5 > 0 else cr_ma5 - 1

                if not pd.isnull(ma10):
                    if last_ma10 < ma10:
                        cr_ma10 = 1 if cr_ma10 < 0 else cr_ma10 + 1
                    else:
                        cr_ma10 = -1 if cr_ma10 > 0 else cr_ma10 - 1

                if not pd.isnull(ma20):
                    if last_ma20 < ma20:
                        cr_ma20 = 1 if cr_ma20 < 0 else cr_ma20 + 1
                    else:
                        cr_ma20 = -1 if cr_ma20 > 0 else cr_ma20 - 1

                if not pd.isnull(macd):
                    if last_macd < macd:
                        cr_macd = 1 if cr_macd < 0 else cr_macd + 1
                    else:
                        cr_macd = -1 if cr_macd > 0 else cr_macd - 1
                    
                    # ! 差距很小，很贴近。
                    if last_macd > 0.01 and macd <=0.01:
                        macdx = -1
                    elif last_macd <= 0.01 and macd > 0.01:
                        macdx = 1
                    else:
                        macdx += 1

                if not pd.isnull(dea):
                    if last_dea < dea:
                        cr_dea = 1 if cr_dea < 0 else cr_dea + 1
                    else:
                        cr_dea = -1 if cr_dea > 0 else cr_dea - 1
                if not pd.isnull(dif):
                    if last_dif < dif:
                        cr_dif = 1 if cr_dif < 0 else cr_dif + 1
                    else:
                        cr_dif = -1 if cr_dif > 0 else cr_dif - 1

            new_indicators = {
                'cr_volume': cr_volume,
                'cr_close': cr_close,
                'cr_kdjd': cr_kdjd,
                'cr_ma5': cr_ma5,
                'cr_ma10': cr_ma10,
                'cr_ma20': cr_ma20,
                'cr_macd': cr_macd,
                'cr_dea': cr_dea,
                'cr_dif': cr_dif,
                'macdx': macdx,
                'last_volume': last_volume,
                'roe': item.get(constants.I_PB)/item.get(constants.I_PE),
                'boll': per
            }
            d.generate_method(new_indicators)

            last_volume = volume
            last_close = close
            last_kdjd = kdjd
            last_ma5 = ma5
            last_ma10 = ma10
            last_ma20 = ma20
            last_macd = macd
            last_dea = dea
            last_dif = dif

        return datas


class Filters:
    pass
