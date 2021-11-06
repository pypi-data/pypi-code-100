import datetime
import json
import time

import requests
from requests.adapters import HTTPAdapter
from selectolax.parser import HTMLParser

from py_mini_racer import MiniRacer


def calc_fund(fund_code, stime, etime, sgfl, shfl, sg):
    """开放式基金收益计算器
    http://data.eastmoney.com/money/calc/CalcFundKF.html
    Arguments:
        fund_code {[type]} -- 基金代码
        stime {[type]} -- 开始持有时间
        etime {[type]} -- 结束持有时间
        sgfl {[type]} -- 申购费率
        shfl {[type]} -- 赎回费率
        sg {[type]} -- 申购金额
    Returns:
        [type] -- 结果
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    timestamp = int(round(time.time() * 1000))
    params = (
        ('fc', fund_code),  # 基金代码
        ('stime', stime),  # 开始持有日期
        ('etime', etime),  # 结束持有日期
        ('stype', '2'),     # 分红方式，1是红利再投，2是现金分红
        ('sgfl', sgfl),  # 申购费率
        ('shfl', shfl),  # 赎回费率
        ('sg', sg),  # 收费金额
        ('lx', '1'),  # 默认值
        ('_', str(timestamp)),  # 时间戳
    )

    url = 'http://fundex.eastmoney.com/FundWebServices/FundSylCalculator.aspx?'
    path = 'fc={}&stime={}&etime={}&stype=2&sgfl={}&shfl={}&sg={}&lx=1&_={}'.format(
        fund_code, stime, etime, sgfl, shfl, sg, timestamp)
    url = url + path

    res = requests.get(
        'http://fundex.eastmoney.com/FundWebServices/FundSylCalculator.aspx', headers=headers, params=params)

    # res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return

    ctx = MiniRacer()
    ctx.eval(res.text)
    result = ctx.eval('Result')

    # jsContent = execjs.compile(res.text)
    # result = jsContent.eval('Result')

    if result.get('error') == '2':
        r = {}
        r['基金代码'] = fund_code
        r['持有天数'] = '0'
        r['赎回总金额'] = '0'
        r['期间总收益金额'] = '0.01'
        r['期间收益率'] = '0'
        r['年化收益率'] = '0'
        return r

    if result.get('error'):
        stime = result.get('sum')
        today = datetime.datetime.strptime(stime, "%Y-%m-%d").date()
        tommorow = today + datetime.timedelta(days=1)
        if tommorow > datetime.datetime.strptime(etime, "%Y-%m-%d").date():
            r = {}
            r['基金代码'] = fund_code
            r['持有天数'] = '0'
            r['赎回总金额'] = '0'
            r['期间总收益金额'] = '0.01'
            r['期间收益率'] = '0'
            r['年化收益率'] = '0'
            return r

        return calc_fund(fund_code, tommorow, etime, sgfl, shfl, sg)

    r = {}
    r['基金代码'] = fund_code
    r['持有天数'] = result.get('days')
    r['赎回总金额'] = result.get('SHZJE')
    r['期间总收益金额'] = result.get('ZSYJE')
    r['期间收益率'] = result.get('QJSYL')
    r['年化收益率'] = result.get('Y')
    return r



def get_funds():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    response = requests.get(
        'http://fund.eastmoney.com/js/fundcode_search.js', headers=headers)

    # jsContent = execjs.compile(response.text)
    # return jsContent.eval('r')
    ctx =    MiniRacer()
    ctx.eval(response.text)
    return ctx.eval('r')


def get_cur_price(code):
    """获取估算净值（实时更新）

    Arguments:
        fund_code {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('rt', int(round(time.time() * 1000))),
    )

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.get('http://fundgz.1234567.com.cn/js/{}.js'.format(code),
                     headers=headers, params=params)
    response.encoding = 'utf-8'
    text = response.text
    s.close()

    if len(text) < 11:
        return None

    return float(json.loads(text[8:-2]).get('gsz'))


def get_stocks(code):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('type', 'jjcc'),
        ('code', code),
        ('topline', '10'),
    )

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.get('http://fundf10.eastmoney.com/FundArchivesDatas.aspx',
                     headers=headers, params=params)
    response.encoding = 'utf-8'

    stocks = set()
    p = HTMLParser(response.text)
    s.close()

    if p is None:
        return stocks

    idx = 1
    while True:
        selector = '.w782 > tbody:nth-child(2) > tr:nth-child({}) > td:nth-child(3) > a:nth-child(1)'.format(
            idx)
        node = p.css_first(selector)
        if node is None:
            break
        stocks.add(node.text())
        idx += 1

    return stocks


class Fund:

    def __init__(self, code):
        self.__code = code

        self.__home_page = None
        self.__init_home_page()
        self.__parser = HTMLParser(self.__home_page)

        self.__name = None

        self.__js = None
        self.__ac_worth_trend = {}
        self.__net_worth_trend = {}

    def get_code(self):
        return self.__code

    def __init_home_page(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        try:
            response = requests.get(
                'http://fund.eastmoney.com/{}.html'.format(self.__code), headers=headers)
            response.encoding = 'utf-8'
            self.__home_page = response.text
        except Exception as e:
            print("__init_home_page", e)
            print("重试初始化{}".format(self.__code))
            s.close()
            time.sleep(15)
            self.__init_home_page()
        finally:
            s.close()

    def get_name(self):
        if self.__name:
            return self.__name

        if self.__parser is None:
            return

        node = self.__parser.css_first('.fundDetail-tit > div:nth-child(1)')
        if node:
            name = node.text()
            self.__name = name[:name.rindex('(')]

        return self.__name

    def get_type(self):
        if self.__parser is None:
            return

        node = self.__parser.css_first(
            '.infoOfFund > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)')
        if node:
            return node.text().strip()

    def get_return(self):
        """获取成立以来的收益
        """
        if self.__parser is None:
            return
        selector = '.dataItem03 > dd:nth-child(4) > span:nth-child(2)'
        node = self.__parser.css_first(selector)
        if node:
            if '%' not in node.text():
                return
            return float(node.text().strip('%'))

    def get_cur_price(self):
        """获取估算净值（实时价格）

        Returns:
            [float] -- 估算净值
        """
        if self.__parser is None:
            return
        node = self.__parser.css_first('#gz_gsz')
        if node:
            if node.text() == '--':
                return
            return float(node.text())

    def get_price(self):
        """获取单位净值

        Returns:
            [float] -- 单位净值
        """
        if self.__parser is None:
            return

        node = self.__parser.css_first(
            '.dataItem02 > dd:nth-child(2) > span:nth-child(1)')
        if node:
            if '--' == node.text():
                return
            return float(node.text())

    def get_ac_price(self):
        """获取累计净值
        """
        if self.__parser is None:
            return
        selector = '.dataItem03 > dd:nth-child(2) > span:nth-child(1)'
        node = self.__parser.css_first(selector)
        if node:
            if '--' == node.text():
                return
            return float(node.text())

    def get_trading_status(self):
        """获取交易状态

        Returns:
            [str] -- 交易状态
        """
        if self.__parser is None:
            return

        node = self.__parser.css_first('div.staticItem:nth-child(1)')
        if node:
            return node.text()

    def get_date(self):
        """基金成立日期

        Returns:
            [type]: [description]
        """
        if self.__parser is None:
            return
        node = self.__parser.css_first(
            '.infoOfFund > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)')
        if node:
            return node.text().split('：')[1]

    def get_asset(self):
        if self.__parser is None:
            return

        node = self.__parser.css_first(
            '.infoOfFund > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)')
        if node:
            asset = node.text().split('：')[1].split('亿元')[0]
            if '--' in asset:
                return
            else:
                return float(asset)

    def load_trend_js(self):
        """初始化JavaScript脚本，用于初始化历史净值等数据（容易被ban，建议少量使用）

        Returns:
            [type] -- [description]
        """
        url = 'http://fund.eastmoney.com/pingzhongdata/{}.js?v={}'.format(
            self.__code, time.strftime("%Y%m%d%H%M%S", time.localtime()))

        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'fund.eastmoney.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        }

        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        content = s.get(url, headers=header)
        content.encoding = 'utf-8'

        self.__js = MiniRacer()
        self.__js.eval(content.text)
        # self.__js = execjs.compile(content.text)
    
        s.close()

    def get_ac_worth_trend(self):
        """获取累计净值趋势
        """
        if self.__ac_worth_trend:
            return self.__ac_worth_trend

        try:
            trend = self.__js.eval('Data_ACWorthTrend')
            for item in trend:
                time_local = time.localtime(item[0]/1000)
                day = time.strftime("%Y-%m-%d", time_local)
                self.__ac_worth_trend[day] = item[1]
        except Exception:
            pass

        return self.__ac_worth_trend

    def get_net_worth_trend(self):
        """获取单位净值趋势
        """
        if self.__net_worth_trend:
            return self.__net_worth_trend
        try:
            trend = self.__js.eval('Data_netWorthTrend')
            for item in trend[::-1]:
                time_local = time.localtime(item['x']/1000)
                day = time.strftime("%Y-%m-%d", time_local)
                self.__net_worth_trend[day] = item['y']
        except Exception as e:
            pass
        return self.__net_worth_trend
