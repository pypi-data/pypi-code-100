import datetime
import json
import time
from enum import Enum

import arrow
import pandas
import requests
import urllib3
from requests.adapters import HTTPAdapter

# 参考
# https://fintie.readthedocs.io/zh_CN/latest/stock/hist_quotes.html
# 可以获得kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy，这些数据，可以看看有没有趋势分析到

Minute_Period = (
    '1d',  # 分时
    '5d',  # 5日
)


class Period(Enum):
    """K线周期
    """
    ONE_M = '1m'
    FIVE_M = '5m'
    FIFTEEN_M = '15m'
    THIRTY_M = '30m'
    ONE_HOUR_M = '60m'
    TWO_HOUR_M = '120m'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    QUARTER = 'quarter'
    YEAR = 'year'

# 技术指标
INDICATORS = 'kline,pe,pb,ps,pcf,market_capital,balance,agt,ggt,ma,macd,kdj,boll,rsi,wr,bias,cci,psy'


def code2symbol(code):
    """将代码转为XQ符号

    Args:
        code (str): 代码

    Returns:
        [str]: 雪球支持的符号
    """
    code = code.upper()
    if code.startswith('399'):
        return 'SZ' + code
    if code.startswith('980'):
        return 'SZ' + code

    if code == '000859':
        return 'CSI' + code

    if code.startswith('00084'):
        return 'SH' + code
    if code.startswith('00085'):
        return 'SH' + code

    if code.startswith('0008'):
        return 'CSI' + code
    if code.startswith('000'):
        return 'SH' + code
    if code.startswith('5138'):
        return 'SH' + code
    if code in ['02828', '.INX', 'GLD', '.NDX', '.SPAHLVCP', 'DAX', 'IAU', 'RSP']:
        return code
    if code.startswith('HS'):
        return 'HK' + code
    if code.startswith('H50'):
        return 'CSI' + code
    if code.startswith('H30'):
        return 'CSI' + code
    if code.startswith('H11'):
        return 'CSI' + code

    if code.isdigit():
        return 'CSI' + code  # 中证指数

    return code


# K线频率
KLINE_FREQ = (
    "1m",  # 1分
    "5m",  # 5分
    "15m",  # 15分
    "30m",  # 30分
    "60m",  # 60分
    "120m",  # 120分
    "day",  # 日K
    "week",  # 周K
    "month",  # 月K
    "quarter",  # 季K
    "year",  # 年K
)


class XueQiu(object):

    def __init__(self):
        urllib3.disable_warnings()

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

        self.session = None
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=5))
        self.session.mount('https://', HTTPAdapter(max_retries=5))
        self.session.get("https://xueqiu.com", headers=self.headers)

    def minute(self, symbol, period):
        """获取分时、五日数据

   # https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH000300&period=1d 分时
        # https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH000300&period=5d 5日


        current': 4807.71, 最新价格
        'volume': 654532900, 成交量
        'avg_price': 4807.71, 均价
        'chg': -7.516, 涨跌额
        'percent': -0.16, 涨跌幅
        timestamp': 1597714200000, 时间
        'amount': 9621772229.0, 交易额
        'high': 4816.57,  最高
        'low': 4807.47 最低

        :param symbol: 代码
        :type symbol: [type]
        :param period: 周期
        :type period: [type]
        :return: [description]
        :rtype: [type]
        """

        assert period in Minute_Period

        params = (
            ('symbol', symbol),
            ('period', period),
        )

        response = self.session.get('https://stock.xueqiu.com/v5/stock/chart/minute.json',
                                    headers=self.headers, params=params, verify=False)
        response.encoding = 'utf-8'
        text = response.text
        data = response.json()
        if data.get("error_code", -1) != 0:
            print(data.get('error_description'))
            return None
        quotes = data.get("data", {})
        df = pandas.DataFrame(data=quotes["items"])
        return df

    def realtime(self, symbol: str):
        """获取实时股票信息

        :param symbol: 指数代码
        :type symbol: str
        :return: 股票信息
        :rtype: int
        """
        params = (
            ('symbol', symbol),
        )

        response = self.session.get('https://stock.xueqiu.com/v5/stock/realtime/quotec.json',
                                    headers=self.headers, params=params, verify=False)

        return response.json()['data'][0]

    def jjcg(self, symbol: str):
        """基金持股数据

        :param symbol: [description]
        :type symbol: str
        :return: [description]
        :rtype: [type]
        """
        params = (
            ('symbol', symbol),
            ('extend', 'true'),
        )

        response = self.session.get('https://stock.xueqiu.com/v5/stock/f10/cn/org_holding/detail.json',
                                    headers=self.headers, params=params, verify=False)

        return response.json()['data']

    def quote(self, symbol):
        """获取股票当前信息，如股票名、价格、pe、pb市值等。
        # https://stock.xueqiu.com/v5/stock/quote.json?symbol=SH000300&extend=detail
        """

        params = (
            ('symbol', symbol),
            ('extend', 'detail'),
        )

        response = self.session.get('https://stock.xueqiu.com/v5/stock/quote.json',
                                    headers=self.headers, params=params, verify=False)

        return response.json()

    def get_boll(self, code: str, period: str = "month"):
        """获取获取最近的macd数据

        :param code: 指数代码
        :type code: str
        :param period: 周期, defaults to "week"
        :type period: str, optional
        :return: [description]
        :rtype: [type]
        """
        begin = int(round(time.time()*1000))
        return self.get_boll_from_date(code, begin, period)

    def get_boll_from_date(self, code: str, begin: int, period: str = "month"):
        """获取指定日期的数据

        :param code: 指数代码
        :type code: str
        :param period: 周期, defaults to "week"
        :type period: str, optional
        :return: [description]
        :rtype: [type]
        """
        dtype = "before"
        count = 1
        indicator = "boll"

        df = self.kline(code, begin, period, dtype, count, indicator)
        if df is None:
            print(code, "no data")
            return None

        for tup in zip(df['ub'], df['lb'], df['ma20']):
            return tup

    def get_info(self, symbol, date, period, count, indicator):
        """获取指定日期的K线、ma、macd等信息。
        Args:
            symbol (str): 代码
            begin (int): 表示从这一天开始，往前count天的数据。
            period (str): 1m/5m/15m/30m/60m/120m/day/week/month/quarter/year
            type (str): before/after/normal 前复权、后复权、不复权
            count (int): 要取最近的行情数据的条数,-2，表示取最近2条数据。
            indicator (str): kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy
        """
        begin = int(round(arrow.get(date).timestamp()*1000))
        params = (
            ('symbol', symbol),
            ('begin', begin),
            ('period', period),
            ('type', 'before'),  # 默认前复权
            ('count', -count),
            ('indicator', indicator),
        )

        response = self.session.get('https://stock.xueqiu.com/v5/stock/chart/kline.json',
                                    headers=self.headers, params=params, verify=False)

        response.encoding = 'utf-8'
        data = response.json()
        if data.get("error_code", -1) != 0:
            print(data.get('error_description'))
            return None
        quotes = data.get("data", {})
        if quotes == {}:
            return
        df = pandas.DataFrame(data=quotes["item"], columns=quotes['column'])
        return df

    def kline(self, symbol, begin, period: Period, dtype='before', count=0xFFFF,
              indicator=INDICATORS):
        """查看k线数据
        Args:
            symbol (str): 代码
            begin (str): 日期。查询从这一天开始，往前count天的数据。
            period (str): 1m/5m/15m/30m/60m/120m/day/week/month/quarter/year
            type (str): before/after/normal 前复权、后复权、不复权
            count (int): 要取最近的行情数据的条数,-2，表示取最近2条数据。
            indicator (str): kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy
            # pe,pb,ps,pcf,market_capital,agt,ggt,balance

            # https: // stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH000300 & 
            # begin = 1566227621083 & end = 1597763600066&period=day 
            # & type = before & indicator = kline
        """



        params = (
            ('symbol', symbol),
            ('begin', int(arrow.get(begin).timestamp()*1000)),
            ('period', period.value),
            ('type', dtype),
            ('count', -count),
            ('indicator', indicator),
        )

        response = self.session.get('https://stock.xueqiu.com/v5/stock/chart/kline.json',
                                    headers=self.headers, params=params, verify=False)

        response.encoding = 'utf-8'
        data = response.json()
        if data.get("error_code", -1) != 0:
            print(data.get('error_description'))
            return None
        quotes = data.get("data", {})
        if quotes == {}:
            return
        df = pandas.DataFrame(data=quotes["item"], columns=quotes['column'])
        return df

    def close(self):
        self.session.close()
