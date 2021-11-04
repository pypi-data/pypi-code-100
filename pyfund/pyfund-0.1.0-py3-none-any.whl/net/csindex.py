import requests
from requests.adapters import HTTPAdapter
from selectolax.parser import HTMLParser
# 主板市盈率
# 中证行业市盈率
# 中证行业市盈率简介
import json


def get_main_board_pe(date):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5,de;q=0.4,pt-BR;q=0.3,pt;q=0.2,ca;q=0.1,es;q=0.1',
    }

    params = (
        ('type', 'zy2'),
        ('date', date),
    )
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.get('http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio',
                     headers=headers, params=params, verify=False)

    p = HTMLParser(response.text)
    s.close()

    selector1 = 'tbody.tc > tr:nth-child({}) > td:nth-child(1)'
    selector2 = 'tbody.tc > tr:nth-child({}) > td:nth-child(2)'

    result = {}
    count = 1
    while True:
        node = p.css_first(selector1.format(count))
        if node is None:
            break
        key = node.text()

        node = p.css_first(selector2.format(count))
        value = node.text()
        result[key] = [float(value)]
        count += 1

    params = (
        ('type', 'zy4'),
        ('date', date),
    )

    response = requests.get('http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio',
                            headers=headers, params=params)

    p = HTMLParser(response.text)
    s.close()

    count = 1
    while True:
        node = p.css_first(selector1.format(count))
        if node is None:
            break
        key = node.text()

        node = p.css_first(selector2.format(count))
        value = node.text()
        result[key].append(float(value))
        count += 1

    return result


def get_csindex_pe(date):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('type', 'zz2'),
        ('date', date),
    )

    response = requests.get('http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio',
                            headers=headers, params=params)
    p = HTMLParser(response.text)
    response.close()

    select_c = '.table > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child({}) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)'
    select_b = '.table > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child({}) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > div:nth-child(1)'

    result = {}
    count = 2
    while True:
        selector = select_c.format(count)
        node = p.css_first(selector)
        if node is None:
            break
        key = node.text()
        node = p.css_first(select_b.format(count))
        result[key] = [float(node.text())]
        count += 2

    params = (
        ('type', 'zz4'),
        ('date', date),
    )

    response = requests.get('http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio',
                            headers=headers, params=params)
    p = HTMLParser(response.text)
    response.close()

    count = 2
    while True:
        selector = select_c.format(count)
        node = p.css_first(selector)
        if node is None:
            break
        key = node.text()
        node = p.css_first(select_b.format(count))
        result[key].append(float(node.text()))
        count += 2

    return result


def get_csrc_pe(date):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio?type=zjh1&date={}'.format(date),
        'Upgrade-Insecure-Requests': '1',
    }

    params = (
        ('type', 'zjh2'),
        ('date', date),
    )

    response = requests.get('http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio',
                            headers=headers, params=params)
    p = HTMLParser(response.text)
    response.close()

    select_c = '.table > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child({}) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)'
    select_b = '.table > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child({}) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > div:nth-child(1)'

    result = {}
    count = 2
    while True:
        selector = select_c.format(count)
        node = p.css_first(selector)
        if node is None:
            break
        key = node.text()
        node = p.css_first(select_b.format(count))
        value = node.text()
        count += 2

        if value.strip() == '--':
            continue
        result[key] = float(value)

    return result


def get_chinabond(date):
    # 获取十年国债，有点不稳定

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://yield.chinabond.com.cn',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'http://yield.chinabond.com.cn/cbweb-czb-web/czb/showHistory?locale=cn_ZH',
    }

    params = (
        ('startDate', date),
        ('endDate', date),
        ('gjqx', '10'),
        ('locale', 'cn_ZH'),
    )
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    response = s.post('http://yield.chinabond.com.cn/cbweb-czb-web/czb/historyQuery',
                      headers=headers, params=params)
    if len(response.text) == 0:
        import time
        time.sleep(10)
        return get_chinabond(date)
    result = json.loads(response.text)
    s.close()

    return float(result.get('heList')[0].get('tenYear'))/100


def get_chinabond_10year():
    #
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('locale', 'cn_ZH'),
    )

    response = requests.get('http://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo',
                            headers=headers, params=params)

    p = HTMLParser(response.text)
    response.close()

    node = p.css_first(
        'gjqxData > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(2)')
    if node is None:
        return 0.03
    return float(node.text())
# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('http://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo?locale=cn_ZH', headers=headers, cookies=cookies)


def get_rzrq():
    # 获取融资融券数据
    headers = {
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5,de;q=0.4,pt-BR;q=0.3,pt;q=0.2,ca;q=0.1,es;q=0.1',
    }

    params = (
        ('type', 'RPTA_RZRQ_LSHJ'),
        ('sty', 'ALL'),
        ('st', 'dim_date'),
        ('sr', '-1'),
        ('p', '1'),
        ('ps', '1'),
    )

    response = requests.get('http://datacenter.eastmoney.com/api/data/get',
                            headers=headers, params=params, verify=False)

    result = json.loads(response.text)
    response.close()

    date = result.get('result').get('data')[0]

    rzrqye = date.get('RZRQYE')
    rzye = date.get('RZYE')
    rqye = date.get('RQYE')

    params = (
        ('type', 'RPTA_RZRQ_LSHJ'),
        ('sty', 'ALL'),
        ('st', 'dim_date'),
        ('sr', '-1'),
        ('p', '1'),
        ('ps', '2500'),
    )

    response = requests.get('http://datacenter.eastmoney.com/api/data/get',
                            headers=headers, params=params, verify=False)
    result = json.loads(response.text)
    response.close()

    min_value = 2273035261015
    max_value = -1
    min_value_rz = 2273035261015
    max_value_rz = -1
    min_value_rq = 2273035261015
    max_value_rq = -1

    def init_min_max(item):
        nonlocal min_value
        nonlocal max_value
        nonlocal min_value_rz
        nonlocal max_value_rz
        nonlocal min_value_rq
        nonlocal max_value_rq
        value = item.get('RZRQYE')
        if value > max_value:
            max_value = value
        if value < min_value:
            min_value = value
        value = item.get('RZYE')
        if value > max_value_rz:
            max_value_rz = value
        if value < min_value_rz:
            min_value_rz = value
        value = item.get('RQYE')
        if value > max_value_rq:
            max_value_rq = value
        if value < min_value_rq:
            min_value_rq = value

    for item in result.get('result').get('data'):
        init_min_max(item)

    params = (
        ('type', 'RPTA_RZRQ_LSHJ'),
        ('sty', 'ALL'),
        ('st', 'dim_date'),
        ('sr', '-1'),
        ('p', '2'),
        ('ps', '2500'),
    )

    response = requests.get('http://datacenter.eastmoney.com/api/data/get',
                            headers=headers, params=params, verify=False)
    result = json.loads(response.text)
    response.close()

    for item in result.get('result').get('data'):
        init_min_max(item)

    params = (
        ('type', 'RPTA_RZRQ_LSHJ'),
        ('sty', 'ALL'),
        ('st', 'dim_date'),
        ('sr', '-1'),
        ('p', '3'),
        ('ps', '2500'),
    )

    response = requests.get('http://datacenter.eastmoney.com/api/data/get',
                            headers=headers, params=params, verify=False)
    result = json.loads(response.text)
    response.close()

    for item in result.get('result').get('data'):
        init_min_max(item)

    pos = (rzrqye-min_value)/(max_value-min_value)
    rzrqye = int(rzrqye/100000000)

    rz_pos = (rzye-min_value_rz)/(max_value_rz-min_value_rz)
    rzye = int(rzye/100000000)

    rq_pos = (rqye-min_value_rq)/(max_value_rq-min_value_rq)
    rqye = int(rqye/100000000)
    return rzrqye, pos, rzye, rz_pos, rqye, rq_pos
