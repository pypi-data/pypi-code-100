import pandas as pd
import requests
import urllib3
from requests.adapters import HTTPAdapter


def get_cur_price(code):
    """获取股票实时行情，包括ETF、LOF等。

    Arguments:
        code {[type]} -- [description]
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

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.get(
        'https://hq.sinajs.cn/format=text&list=s_sh{}'.format(code), headers=headers)
    response.encoding = 'utf-8'
    text = response.text
    s.close()

    # 证券简称,最新价,涨跌额,涨跌幅,成交量,成交额
    arr = text.strip().split(',')

    if len(arr) < 2:
        return None
    return float(arr[1])


def get_cur_point(index_code):
    """

    Arguments:
        code {[type]} -- [description]
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

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    prefix = get_index_prefix(index_code)
    if prefix is None:
        return
    response = s.get(
        'https://hq.sinajs.cn/format=text&list={}{}'.format(prefix, index_code), headers=headers)
    response.encoding = 'utf-8'
    text = response.text
    s.close()

    arr = text.strip().split(',')

    if len(arr) < 4:
        return None
    return float(arr[3])


def get_index_prefix(index_code):
    if index_code.startswith("399"):
        return 'sz'
    if index_code.startswith('000'):
        return 'sh'
    if index_code.startswith('93'):
        return None
    if index_code.startswith('95'):
        return None
    if index_code.startswith('H'):
        return None

    raise UnknownPrefix


class UnknownPrefix(Exception):
    pass

# http://hq.sinajs.cn/list=sz399995

# 上交所上市的股票代码以6开头，以大中盘股居多。
# 深证成指主板股票以00开头，
# 中小板以002开头，
# 创业板以300开头。

# 查询深圳成指的URL为：sz
# s_sz399995=基建工程,3820.87,-29.143,-0.76, 15723640, 1198743
#           指数名称，当前点数，当前价格，涨跌率，成交量（手），成交额（万元）；
# var hq_str_sz399995="基建工程,
# 3838.224, 今开
# 3850.014, 昨收
# 3820.871, 当前
# 3849.132, 今日最高
# 3785.243,，今日最低
# 0.000,0.000,1572364021,11987431284.880,0,0.000,0,0.000,0,0.000,0,0.000,0,0.000,0,0.000,0,0.000,0,0.000,0,0.000,0,0.000,
# 2020-08-07,15:01:51,00"; 日期，时间

# 通过名字获取股票代码
# https://suggest3.sinajs.cn/suggest/key=%E5%85%89%E8%BF%85%E7%A7%91%E6%8A%80
# var suggestvalue="光迅科技,11,002281,sz002281,光迅科技,,光迅科技,99,1";

# 通过股票代码获取股票名称

def get_fund_asset(code):
    """获取基金规模

    :param code: [description]
    :type code: [type]
    :return: [description]
    :rtype: [type]
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-GPC': '1',
    }
    response = requests.get(
        'https://hq.sinajs.cn/format=text&list=f_{}'.format(code), headers=headers, verify=False)
    text = response.text
    if text.startswith('rt_hk'):
        return text.split(',')[1]

    return float(text.split(',')[-1].strip())

def get_stock_name(code: str) -> str:
    """获取股票、基金、指数的名称
    
    :param code: 代码
    :type code: str
    :return: [description]
    :rtype: str
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-GPC': '1',
    }
    # * 小写
    # * A股 SZ和SH开头
    # * 香港 hk_开头，加上指数名
    code = code.lower()
    if code.startswith('hk'):
        code = 'rt_' + code.upper().replace('HK', 'hk')
    elif code.startswith('hs'):
        code = 'rt_hk' + code.upper()
    elif code.startswith('f'):
        code = 'o' + code
    elif code.startswith('.'):
        code = 'gb_$' + code[1:]

    response = requests.get(
        'https://hq.sinajs.cn/format=text&list={}'.format(code), headers=headers)
    text = response.text
    if text.startswith('rt_hk'):
        return text.split(',')[1]

    return text.split(',')[0].split('=')[-1]


def build_scode(codes: list):
    scodes = []
    for code in codes:
        code = code.lower()
        if code.startswith('hk'):
            code = code.replace('hk', 'hk_')
        elif code.startswith('hs'):
            code = 'hk_' + code
        elif code.startswith('sz') or code.startswith('sh'):
            code = 'cn_' + code
        elif code.startswith('of'):
            code = 'fund_' + code.upper()
        elif code.startswith('f'):
            code = 'fund_o' + code.upper()
        elif code.startswith('.') or code.startswith('sh'):
            code = 'us_' + code
        scodes.append(code)

    return ",".join(scodes)


def corrcoef(codes: list, start_date: str, end_date: str) -> str:
    """计算股票、指数之间的相关性

    :param codes: 股票代码、指数代码，如SZ002773
    :type codes: list
    :param start_date: 开始日期, 如，'2021-05-19'
    :type start_date: str
    :param end_date: 结束日期，通常是3年
    :type end_date: str
    :return: 结果
    :rtype: str
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-GPC': '1',
        'TE': 'Trailers',
    }

    names = []
    stocks = {}
    for code in codes:
        name = get_stock_name(code)

        if code.startswith('HK'):
            code = code[2:]
        elif code.startswith('F'):
            code = 'O' + code

        stocks[code.upper()] = name
        names.append(name)


    scode = build_scode(codes)
    params = (
        ('scode', scode),
        ('start_date', start_date),
        ('end_date', end_date),
    )
    urllib3.disable_warnings()

    response = requests.get('https://global.finance.sina.com.cn/api/openapi.php/RiseService.corrcoef',
                            headers=headers, params=params, verify=False)
    result = response.json()

    return stocks, names, response.json()
