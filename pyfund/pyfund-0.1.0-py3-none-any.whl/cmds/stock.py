from random import randint

import arrow
import click
import numpy as np
import pandas as pd
from petty import console

from pyfund import to_per
from pyfund.cmds import stocks
from pyfund.net import xueqiu


def judge(code, date, count):
    xq = xueqiu.XueQiu()
    begin = arrow.now().date()
    if date:
        begin = date

    lines = []
    data = xq.kline(code, begin, 'month', 'before', count,
                    'kline,pe,pb,pcf,market_capital,macd,boll,ma,kdj')
    last_kdjd = 0  # 上一个周期 kdj差
    last_boll = 0  # 上一个周期 boll百分比
    last_volume = 0  # 上一个周期 成交量
    last_close = 0  # 上一个周期 收盘价
    last_macd = 0  # 上一个周期 收盘价

    boll_break_100 = False  # Boll百分位突破100
    for _, item in data[['timestamp', 'close', 'volume', 'ma5', 'ub', 'lb', 'macd', 'kdjd', 'pe', 'pb']].iterrows():
        date = arrow.get(item['timestamp']).date()
        close = item['close']
        ma5 = item['ma5']
        volume = item['volume']
        pe = item['pe']  # 市值
        pb = item['pb']  # 市值
        roe = pb/pe

        macd = item['macd']
        kdjd = item['kdjd']

        ub = item['ub']
        per = np.nan
        if ub is not None and not np.isnan(ub):
            lb = item['lb']
            per = (close - lb)/(ub-lb)

        if per > 1:
            boll_break_100 = True

        line = [date, close, to_per(
            1/pe), to_per(roe), to_per(per)]

        MACD_BIT = 0b100000  # MACD上涨
        BOLL_BIT = 0b010000  # BOLL百分位上涨
        VOLUME_BIT = 0b001000  # 成交量上涨
        CLOSE_BIT = 0b000100  # 收盘价上涨
        KDJD_BIT = 0b000010  # KDJd上涨
        MA5_BIT = 0b000001  # 股价低于MA5，跌破MA5

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

        isPrint = False  # 打印标记
        if per > 0.7:  # ! 卖出逻辑
            if tag & CLOSE_BIT == CLOSE_BIT:  # 股价上涨
                count = 0
                msg = '股价↑ - '
                if tag & MACD_BIT != MACD_BIT:
                    count += 1
                    msg += 'macd↓ '
                if tag & BOLL_BIT != BOLL_BIT:
                    count += 1
                    msg += 'boll百分位↓ '
                if tag & VOLUME_BIT != VOLUME_BIT:
                    count += 1
                    msg += '成交量↓ '
                if tag & KDJD_BIT != KDJD_BIT:
                    count += 1
                    msg += 'KDJd↓ '
                if tag & MA5_BIT == MA5_BIT:
                    count += 1
                    msg += '跌破MA5 '
                if count > 0 and boll_break_100:
                    isPrint = True
                    opt = '清仓' if 'MA5' in msg else '卖出'
                    if boll_break_100 and per < 0.9:
                        msg += 'Boll百分比跌破0.9 '
                        opt = '清仓'
                    lines.append(line + ['{}< {}{}'.format(msg, opt, count)])

                    if opt == '清仓':
                        boll_break_100 = False  # 清仓，重置
            else:
                count = 0
                msg = '股价↓ - '
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
                if tag & MA5_BIT == MA5_BIT:
                    count += 1
                    msg += '跌破MA5 '
                if count > 0 and boll_break_100:
                    isPrint = True
                    opt = '清仓' if 'MA5' in msg else '卖出'
                    if boll_break_100 and per < 0.9:
                        msg += 'Boll百分比跌破0.9 '
                        opt = '清仓'
                    lines.append(line + ['{}< {}{}'.format(msg, opt, count)])
                    if opt == '清仓':
                        boll_break_100 = False  # 清仓，重置
        else:  # ! 买入逻辑
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
                if 'KDJd↑' in msg and '成交量↑' in msg:
                    opt = '买入'
                    lines.append(line + ['{}< {}{}'.format(msg, opt, count)])

        last_boll = per  # 上一个周期 boll百分比
        last_volume = volume  # 上一个周期 成交量
        last_close = close  # 上一个周期 成交量
        last_macd = macd  # 上一个周期 macd
        last_kdjd = kdjd


    return lines


@click.command()
@click.argument('code')
@click.option('-d', '--date', help='指定日期')
@click.option('-c', '--count', default=1, help='数据数量')
def stock(code, date, count):
    """查看股票信息
    """
    lines = judge(code, date, count)
    # 股票不行，股票与指数基金不同，股票买的人多了，会造成抢筹；卖的人多了，会造成踩踏。
    df = pd.DataFrame(columns=['日期', 'close', 'eps', 'roe', 'boll', '操作'])
    for item in lines:
        df.loc[len(df)] = [item[i] for i in range(len(item))]

    df.to_csv("./tmp/" + code + '.csv', sep=',')
    console.prettify(df, row_limit=200, col_limit=50)

    xq = xueqiu.XueQiu()
    jjcg = xq.jjcg(code)
    fund_items = jjcg.get('fund_items', [])

    funds = []
    for i in fund_items:
        name = i['org_name_or_fund_name']
        if stocks.skip_fund(name):
            funds.append(name)

    print()
    print(len(funds))
    # for fund in sorted(funds):
    #     print(fund)
