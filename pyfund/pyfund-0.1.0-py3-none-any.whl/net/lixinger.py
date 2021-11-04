import calendar
import csv
import datetime
import json

import requests

from enum import Enum


class API_TYPE(Enum):
    A = 'a'  # A股
    H = 'h'  # 港股
    US = 'us'  # 美股


class API(Enum):
    A = 'a'  # A股
    H = 'h'  # 港股
    US = 'us'  # 美股


class LixingerAPI:

    def __init__(self, token):
        """初始化

        Args:
            token (str): 指定token
        """
        self.token = token

    def buildPostDataByDate(self, codes: list, date):
        """通过日期获取数据

        Args:
            codes (list): [description]
            date ([type]): [description]

        Returns:
            [type]: [description]
        """
        data = {}
        data['token'] = self.token
        data["date"] = date
        data['stockCodes'] = codes

        data['metricsList'] = [
            "pe_ttm.y10.ewpvo",
            "pb.y10.ewpvo",
            "ps_ttm.y10.ewpvo",
            "pe_ttm.y5.ewpvo",
            "pb.y5.ewpvo",
            "ps_ttm.y5.ewpvo",
            'dyr.ewpvo',  # 股息率
            "cp",  # 收盘点位
            "cpc",  # 涨跌幅
            "mc",  # 市值
            "fb",  # 融资余额
            "sb",  # 融券余额
        ]

        return data

    def buildPostDataByDateRange(self, code, start, end):
        """通过时间范围获取

        Args:
            code (str): 指数代码
            start (str): 开始日期
            end (str): 结束日期
        """
        data = {
            "token": self.token,
            "startDate": start,
            "endDate": end,
            "stockCodes": [
                code
            ],
            "metricsList": [
                "pe_ttm.y10.ewpvo",
                "pb.y10.ewpvo",
                "ps_ttm.y10.ewpvo",
                "pe_ttm.y5.ewpvo",
                "pb.y5.ewpvo",
                "ps_ttm.y5.ewpvo",
                'dyr.ewpvo',  # 股息率
                "cp",  # 收盘点位
                "cpc",  # 涨跌幅
                "mc",  # 市值
                "fb",  # 融资余额
                "sb",  # 融券余额
            ]
        }

        print(data)

        return data

    def Post(self, api, data):
        """数据到特定到API服务器，获取数据

        Args:
            api ([type]): [description]
            data ([type]): [description]

        Returns:
            [type]: [description]
        """
        url = 'https://open.lixinger.com/api/{}/index/fundamental'.format(
            api.value)

        headers = {"Content-Type": "application/json"}
        result = requests.post(
            url=url, data=json.dumps(data), headers=headers)
        if result.status_code != 200:
            print('lixingger，获取{}数据失败!'.format(api))
            print(url)
            print(data)
            print(result.text)
            return
        return json.loads(result.text)

    def ddd(self):
        print("???")

    def PostByDateRange(self, api_type, code, start, end):
        data = self.buildPostDataByDateRange(code, start, end)
        return self.Post(api_type, data)

        # def GetDataByRate(api_type, index_code, start, end):
        #     pass


def getIndex(api, codes: list):
    """获取指数的名称

    Args:
        codes (list): [description]

    Returns:
        [type]: [description]
    """
    data = {}
    data['token'] = '1488a264-221a-4fdd-ab1f-48b908f19380'
    data['stockCodes'] = codes

    url = 'https://open.lixinger.com/api/{}/index'.format(api.value)
    headers = {"Content-Type": "application/json"}
    result = requests.post(url=url, data=json.dumps(data), headers=headers)
    if result.status_code != 200:
        print('lixingger，获取{}数据失败!'.format(api))
        print(url)
        print(data)
        print(result.text)
        return
    return json.loads(result.text)


def getConstituents(api, codes: list):
    """获取指数的样本信息

    Args:
        codes (list): [description]

    Returns:
        [type]: [description]
    """
    data = {}
    data['token'] = '1488a264-221a-4fdd-ab1f-48b908f19380'
    data["date"] = 'latest'
    data['stockCodes'] = codes

    url = 'https://open.lixinger.com/api/{}/index/constituents'.format(
        api.value)
    headers = {"Content-Type": "application/json"}
    result = requests.post(url=url, data=json.dumps(data), headers=headers)
    if result.status_code != 200:
        print('lixingger，获取{}数据失败!'.format(api))
        print(url)
        print(data)
        print(result.text)
        return
    return json.loads(result.text)


def Post(api, data):
    """Post数据到特定到API服务器，获取数据

    Args:
        api ([type]): [description]
        data ([type]): [description]

    Returns:
        [type]: [description]
    """
    url = 'https://open.lixinger.com/api/{}/index/fundamental'.format(
        api.value)

    headers = {"Content-Type": "application/json"}
    result = requests.post(url=url, data=json.dumps(data), headers=headers)
    if result.status_code != 200:
        print('lixingger，获取{}数据失败!'.format(api))
        print(url)
        print(data)
        print(result.text)
        return
    return json.loads(result.text)


class YEAR(Enum):
    Three = 'y3'
    Five = 'y5'
    Ten = 'y10'
    Twenty = 'y20'
    ALL = 'fs'


def build_post_data(codes: list, date):
    data = {}
    data['token'] = '1488a264-221a-4fdd-ab1f-48b908f19380'
    data["date"] = date
    data['stockCodes'] = codes

    data['metricsList'] = [
        "pe_ttm.y10.ewpvo",
        "pb.y10.ewpvo",
        "ps_ttm.y10.ewpvo",
        "pe_ttm.y5.ewpvo",
        "pb.y5.ewpvo",
        "ps_ttm.y5.ewpvo",
        'dyr.ewpvo',  # 股息率
        "cp",  # 收盘点位
        "cpc",  # 涨跌幅
        "mc",  # 市值
        "fb",  # 融资余额
        "sb",  # 融券余额
    ]

    return data


def GetIndexByDate(api_type, codes: list, date: str):
    """获取单个指数

    Arguments:
        api_type {[type]} -- [description]
        codes {[type]} -- [description]
        date {str} -- [description]
        year {int} -- [description]
    """

    data = build_post_data(codes, date)
    result = Post(api_type, data)
    return result


def GetRiskLevels(api_type, codes: list, date):
    """获取指数，某天的5年综合估值（风险水平），百分位越低越安全，越高越危险。
    最多只能获取100个。

    Args:
        api_type ([type]): [description]
        codes ([type]): [description]
        date ([type]): [description]
        year ([type]): [description]
    """
    idata = GetIndexByDate(api_type, codes, date)
    if idata['data'] == []:
        print(index_code, '无法获得数据')
        raise

    result = {}
    for item in idata['data']:
        key = item['stockCode']

        pe_cvpos = item['pe_ttm']['y5']['ewpvo']['cvpos']
        pb_cvpos = item['pb']['y5']['ewpvo']['cvpos']
        ps_cvpos = item['ps_ttm']['y5']['ewpvo']['cvpos']

        lvl_y5 = (pe_cvpos+pb_cvpos+ps_cvpos)/3
        pe_cvpos = item['pe_ttm']['y10']['ewpvo']['cvpos']
        pb_cvpos = item['pb']['y10']['ewpvo']['cvpos']
        ps_cvpos = item['ps_ttm']['y10']['ewpvo']['cvpos']
        lvl_y10 = (pe_cvpos+pb_cvpos+ps_cvpos)/3

        pe = item['pe_ttm']['y5']['ewpvo']['cv']
        pb = item['pb']['y5']['ewpvo']['cv']
        dyr = item['dyr']['ewpvo']
        roe = pb/pe + dyr

        result[key] = [lvl_y5, lvl_y10, pe, pb, roe]

    return result


def GetRiskLevel(api_type, index_code, date):
    """获取指数，某天的5年综合估值（风险水平），百分位越低越安全，越高越危险。

    Args:
        api_type ([type]): [description]
        index_code ([type]): [description]
        date ([type]): [description]
        year ([type]): [description]
    """
    idata = GetIndexByDate(api_type, [index_code], date)
    if idata['data'] == []:
        print(index_code, '无法获得数据')
        raise
    pe_cvpos = idata['data'][0]['pe_ttm']['y5']['ewpvo']['cvpos']
    pb_cvpos = idata['data'][0]['pb']['y5']['ewpvo']['cvpos']
    ps_cvpos = idata['data'][0]['ps_ttm']['y5']['ewpvo']['cvpos']

    return (pe_cvpos+pb_cvpos+ps_cvpos)/3


def GetIndexPoints(api_type, index_code, start, end):
    """获得指数一段时间内的点数。

    Args:
        api_type ([type]): API类型
        index_code ([type]): 指数代码
        start ([type]): 开始时间
        end ([type]): 结束时间

    Returns:
        [type]: [description]
    """
    data = {
        "token": "1488a264-221a-4fdd-ab1f-48b908f19380",
        "startDate": start,
        "endDate": end,
        "stockCodes": [
            index_code
        ],
        "metricsList": [
            "cp"
        ]
    }
    result = Post(api_type, data)
    return result


def GetIndexMinMaxPoints(api_type, index_code, start, end):
    """获得指数一段时间内的最高/最低点。

    Args:
        api_type ([type]): API类型
        index_code ([type]): 指数代码
        start ([type]): 开始时间
        end ([type]): 结束时间

    Returns:
        [type]: [description]
    """
    result = GetIndexPoints(api_type, index_code, start, end)
    min_point = 0xFFFFFFFF
    max_point = -1
    for item in result['data']:
        p = item['cp']
        if p < min_point:
            min_point = p
        if p > max_point:
            max_point = p
    return min_point, max_point


def GetIndexMinMaxPointsByDate(api_type, index_code, date):
    """获得指数一段时间内的最高/最低点。

    Args:
        api_type ([type]): API类型
        index_code ([type]): 指数代码
        start ([type]): 开始时间
        end ([type]): 结束时间

    Returns:
        [type]: [description]
    """
    day = datetime.datetime.strptime(date, '%Y-%m-%d')
    day = day + datetime.timedelta(days=-365)
    start = day.strftime('%Y-%m-%d')

    result = GetIndexPoints(api_type, index_code, start, date)
    min_point = 0xFFFFFFFF
    max_point = -1
    for item in result['data']:
        p = item.get('cp', None)
        if p is None:
            continue
        if p < min_point:
            min_point = p
        if p > max_point:
            max_point = p
    return min_point, max_point
