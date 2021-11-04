import concurrent.futures as cf
import json
import os
import sys

import arrow
import click
import numpy
import pandas as pd
from petty import console

from pyfund import log, to_per
from pyfund.net import xueqiu


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
    df = pd.DataFrame(
        columns=['代码', '名称', '日期', '收盘价', '月BOLL', 'MACD', 'KDJ', 'KDJ-J'])

    def get(df):
        part = df[['close', 'ub', 'lb']]
        close = part.iloc[0, 0]
        ub = part.iloc[0, 1]
        lb = part.iloc[0, 2]
        return close, ub, lb

    def process(code):
        symbol = xueqiu.code2symbol(code)

        try:
            data = xq.quote(symbol).get('data', {})
        except:
            print('\n', symbol, "ERROR XQ")
            return
        if data is None:
            print(code, 'data error')
            return
        quoto = data.get('quote', {})
        if quoto is None:
            print(code, 'quoto error')
            return
        name = quoto.get('name')

        today = arrow.now().date()

        line = []  # '代码', '名称', '收盘价', '月BOLL', 'MACD', 'KDJ1', 'KDJ2'
        dm = xq.get_info(symbol, today, 'month', 1, 'kline,boll,macd,kdj')
        try:
            for _, item in dm[['timestamp', 'close', 'ub', 'lb', 'dea', 'dif', 'macd', 'kdjk', 'kdjd', 'kdjj']].iterrows():
                date = arrow.get(item['timestamp']).date()
                close = item['close']

                ub = item['ub']
                per = numpy.nan
                if ub is not None and not numpy.isnan(ub):
                    lb = item['lb']
                    per = (close - lb)/(ub-lb)
                    # if per > 0.5:
                    #     return

                dea = item['dea']
                dif = item['dif']

                # 找下降趋势
                if dif > dea:  # 排除上升趋势
                    return

                # 排除下降趋势
                kdjd = item['kdjd']
                kdjk = item['kdjk']
                kdjj = item['kdjj']
                # if kdjj > 33:
                #     return
                # if kdjd > kdjk and kdjk > kdjj:
                #     return
                x = abs((kdjj-kdjd)/100)
                if x > 0.1:
                    return
                
                line = [symbol, name, date, close, to_per(per), item['macd'], round(x, 3), kdjj]
        except KeyError:
            print(symbol)
        stocks.append(line)

    with cf.ThreadPoolExecutor(3) as executor:
        tasks = []
        for code in codes:
            task = executor.submit(process, code)
            task.add_done_callback(log)
            tasks.append(task)

        size = len(tasks)
        i = 0
        for _ in cf.as_completed(tasks):
            i += 1
            print('\r', end='')
            print("{} -> {:.2%}".format(size, i/size), end='')
            sys.stdout.flush()
    print()

    for item in stocks:
        df.loc[len(df)] = [item[i] for i in range(len(item))]

    df.to_csv("./tmp/" + output, sep=',')
    console.prettify(df, row_limit=30)


@click.command()
@click.option('-i', '--input', required=True, help="存放指数等文件")
def etf(input):
    """筛选etf
    """
    codes = set()

    if os.path.isfile(input):
        with open(input, encoding='utf-8') as f:
            for line in f:
                code = line.split(',')[0]
                if code in codes:
                    print(code)
                codes.add(code)
    else:
        return

    lists = sorted(codes)
    __filter(lists, 'filter_etf_{}.csv'.format(arrow.now().date()))
