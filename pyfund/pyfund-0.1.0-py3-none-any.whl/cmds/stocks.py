"""股票筛选"""
import concurrent.futures as cf
import os
import sys

import arrow
import click
import numpy as np
import pandas as pd
from petty import console
from pyfund import __version__, log
from pyfund.backtesting import BackTesting
from pyfund.net import xueqiu
from pyfund.strategies import bull, day, week


def weeks(code):
    bt = BackTesting()
    bt.load_datas(code, xueqiu.Period.WEEK)
    bt.load_strategy(week.Strategy())
    bt.set_start_date('2020-01-01')
    bt.run()

def to_per(i):
    return '{:.2%}'.format(i)


def skip_fund(name):
    if '股票型' in name:
        return True
    if '混合型' in name:
        return True
    if '债券型' in name:
        return True
    return False


def __filter(codes: list, output: str):
    """PE尽量低，接近BOLL下轨。之后，再根据资产负债率相对较好的。

    :param codes: [description]
    :type codes: list
    :param name: [description]
    :type name: str
    :param percent: Boll百分位
    :type percent: float
    """
    xq = xueqiu.XueQiu()
    stocks = []
    df = pd.DataFrame(columns=['代码', '名称', '日期', '收盘价',
                               'pe/pb', 'roe', '月BOLL', '基数', '说明'])

    def judge(code):
        # xq = xueqiu.XueQiu()
        data = xq.quote(code).get('data', {})
        quoto = data.get('quote', {})
        name = quoto.get('name')
        if 'ST' in name:
            return
        pe_ttm = quoto.get('pe_ttm')
        pb = quoto.get('pb')  # 市净率=每股市价/每股净资产 比值越低意味着风险越低。

        eps = quoto.get('eps')  # 每股收益，越高越好
        navps = quoto.get('navps')  # 每股净资产值越大，表明公司每股股票代表的财富越雄厚

        roe = eps/navps

        jjcg = xq.jjcg(code)
        num = 0
        for item in jjcg.get('fund_items', []):
            org_name_or_fund_name = item['org_name_or_fund_name']
            if org_name_or_fund_name == '全部合计':
                to_float_shares_ratio = item['to_float_shares_ratio']
                continue
            if skip_fund(org_name_or_fund_name):
                num += 1
        if num == 0:
            return
        if num < 50:
            return

        begin = arrow.now().date()

        data = xq.kline(code, begin, 'month', 'before', 3,
                        'kline,market_capital,macd,boll,ma,kdj')
        last_kdjd = 0  # 上一个周期 kdj差
        last_boll = 0  # 上一个周期 boll百分比
        last_volume = 0  # 上一个周期 成交量
        last_close = 0  # 上一个周期 收盘价
        last_macd = 0  # 上一个周期 收盘价
        counter = 0
        for _, item in data[['timestamp', 'close', 'volume', 'ma5', 'ub', 'lb', 'macd', 'kdjd']].iterrows():
            counter += 1
            date = arrow.get(item['timestamp']).date()
            close = item['close']
            volume = item['volume']
            macd = item['macd']
            kdjd = item['kdjd']

            ub = item['ub']
            per = np.nan
            if ub is not None and not np.isnan(ub):
                lb = item['lb']
                per = (close - lb)/(ub-lb)

            if counter == 1:
                last_boll = per  # 上一个周期 boll百分比
                last_volume = volume  # 上一个周期 成交量
                last_close = close  # 上一个周期 成交量
                last_macd = macd  # 上一个周期 macd
                last_kdjd = kdjd
                continue

            ma5 = item['ma5']

            tag = 0b000000
            if macd > last_macd:
                tag |= MACD_BIT

            if per > last_boll:
                tag |= BOLL_BIT

            if volume > last_volume:
                tag |= VOLUME_BIT

            if close > last_close:
                tag |= CLOSE_BIT

            if kdjd > last_kdjd:
                tag |= KDJD_BIT

            if ma5 > close:
                tag |= MA5_BIT

            if per > 0.7:
                continue
            
            # ! 买入逻辑
            if tag & CLOSE_BIT == CLOSE_BIT:  # 股价上涨
                count = 0
                msg = '股价↑ - '
                if tag & MACD_BIT == MACD_BIT:
                    count += 1
                    msg += 'macd↑ '
                if tag & BOLL_BIT == BOLL_BIT:
                    count += 1
                    msg += 'boll百分位↑ '
                if tag & VOLUME_BIT == VOLUME_BIT:
                    count += 1
                    msg += '成交量↑ '
                if tag & KDJD_BIT == KDJD_BIT:
                    count += 1
                    msg += 'KDJd↑ '
                if tag & MA5_BIT != MA5_BIT:
                    count += 1
                    msg += '突破MA5 '
                if 'KDJd↑' not in msg:
                    continue
                stocks.append([code, name, date, close, to_per(
                    pb/pe_ttm), round(roe*100, 3), to_per(per), num, msg])

            last_boll = per  # 上一个周期 boll百分比
            last_volume = volume  # 上一个周期 成交量
            last_close = close  # 上一个周期 成交量
            last_macd = macd  # 上一个周期 macd
            last_kdjd = kdjd
            
    with cf.ThreadPoolExecutor(3) as executor:
        tasks = []
        for code in codes:
            task = executor.submit(judge, code)
            task.add_done_callback(log)
            tasks.append(task)

        size = len(tasks)
        i = 0
        for _ in cf.as_completed(tasks):
            i += 1
            print('\r', end='')
            print("{} -> {:.2%}".format(size, i/size), end='')
            sys.stdout.flush()
    
    xq.close()
    print()
    for item in stocks:
        df.loc[len(df)] = [item[i] for i in range(len(item))]
    df.to_csv("./tmp/" + output, sep=',')
    console.prettify(df, row_limit=100, col_limit=20)


@click.command()
@click.option('-i', '--input', help="存放股票代码的文件，或者存放指数表格的目录")
def stocks(input):
    """从股票列表，或指数excel中，筛选股票
    """
    codes = set()
    if input is None:
        return
    if not os.path.exists(input):
        return

    if os.path.isdir(input):
        return

    elif input.endswith(".txt"):
        with open(input, encoding='utf-8') as f:
            for line in f:
                codes.add(line.strip())
    else:
        ef = pd.ExcelFile(input)
        name = ef.sheet_names[0]

        data = pd.DataFrame()
        d = pd.read_excel(input, sheet_name=name, dtype=str)
        data = pd.concat([data, d])\

        for _, item in data[['成分券代码Constituent Code', '交易所Exchange']].iterrows():
            cc = str(item[0])
            if cc.startswith('300') or cc.startswith('688'):
                continue
            code = 'S' + item[1][-1] + cc
            codes.add(code)

    name = os.path.basename(input)
    lists = sorted(codes)
    # __filter(lists, 'filter_stocks_{}_{}.csv'.format(name, arrow.now().date()))

    with cf.ThreadPoolExecutor(3) as executor:
        tasks = []
        for code in lists:
            task = executor.submit(weeks, code)
            task.add_done_callback(log)
            tasks.append(task)

        size = len(tasks)
        i = 0
        for _ in cf.as_completed(tasks):
            i += 1
            # print('\r', end='')
            # print("{} -> {:.2%}".format(size, i/size), end='')
            # sys.stdout.flush()