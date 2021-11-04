"""读入股票持有信息，输出权重、比例、收益率"""
import os

import arrow
import click
import pandas as pd
from petty import console

from pyfund.cmds import stocks
from pyfund.net import xueqiu
from pyfund.utils import to_per

STOCKS = {}

def process(symbols):

    days = []
    weeks = []
    months = []

    xq = xueqiu.XueQiu()

    today = arrow.now().date()
    
    jjcgs = [] # 基金数量

    # 计算基金数量、上涨空间
    for symbol in symbols:
        if symbol == 'CASH':
            months.append(0)
            jjcgs.append(0)
            continue
        jjcg = xq.jjcg(symbol)
        fund_items = jjcg.get('fund_items', [])
        num = 0
        for i in fund_items:
            name = i['org_name_or_fund_name']
            if cli_stocks.skip_fund(name):
                num += 1
        jjcgs.append(num)

        name = STOCKS.get(symbol, "None")
        if 'ETF' in name or 'QDII' in name:
            num = 9999

        d = xq.get_info(symbol, today, 'month', 1, 'kline,boll,ma')
        for _, item in d[['close', 'ub', 'lb', 'ma10']].iterrows():
            close = item['close']
            ub = item['ub']
            lb = item['lb']

            per = (close - lb)/(ub-lb)
            months.append(to_per(per))

    xq.close()
    return months, jjcgs


@click.command()
@click.argument('filename')
def status(filename):
    '''统计当前持仓的状态'''
    data = pd.read_csv(filename, converters={'代码': str})
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180)

    global STOCKS
    for _, row in data[['完整代码', '名称']].iterrows():
        STOCKS[row[0]] = row[1]
    
    hoding_cost = []
    for _, row in data[['成本', '持仓数']].iterrows():
        hoding_cost.append(int(row[0] * row[1]))
    data["持有市值"] = hoding_cost

    all_cost = sum(hoding_cost)
    def ff(x): return x/all_cost
    data['持有权重'] = ["{:.2%}".format(ff(x)) for x in hoding_cost]

    current_cost = []
    xq = xueqiu.XueQiu()
    # 获取列代码，获取当前价格
    percents = []  # 今日涨跌幅
    CASH = 0 # 现金
    for _, row in data[['完整代码', '持仓数']].iterrows():
        if row[0] == 'CASH':
            percents.append("0")
            CASH = row[1]
            current_cost.append(CASH)
            continue

        sb = xueqiu.code2symbol(row[0])
        rt = xq.realtime(sb)
        price = rt.get('current')

        percent = ''
        p = rt.get('percent')
        if p == 0:
            if rt.get('open'):
                percent = '{}%'.format(p)
            else:  # 停牌
                percent = '停牌'
        else:
            percent = '{}%'.format(p)
        percents.append(percent)

        current_cost.append(row[1] * price)

    # data["当前市值"] = current_cost
    current_all_cost = sum(current_cost)
    data['当前权重'] = ["{:.2%}".format(ff(x)) for x in current_cost]
    data['收益'] = [int(current_cost[i] - hoding_cost[i])
                  for i in range(0, len(hoding_cost))]
    data['收益率'] = [round(data['收益'][i]*100 / data['持有市值'][i],3)
                   for i in range(0, len(hoding_cost))]
    data["涨跌幅"] = percents

    symbols = []
    for _, row in data[['完整代码']].iterrows():
        symbols.append(row[0])

    months, jjcgs = process(symbols)
    data['基金数'] = jjcgs
    data['月'] = months

    # TODO 既然不要为什么要计算？
    data = data.drop(columns=['交易所', '代码', '持仓数', '成本', '持有市值', '持有权重'])
    data = data.sort_values(by=['收益率'], ascending=False)
    console.prettify(data, row_limit=30, col_limit=15)

    # TODO 买卖点计算
    print("持有成本：{}".format(all_cost))
    print("当前市值：{}".format(int(current_all_cost)))
    print("总收益：{:.2f}".format(current_all_cost - all_cost))
    print("总收益率：{:.2%}".format((current_all_cost - all_cost)/all_cost))
    print("5%份额：{:.2f}".format((current_all_cost)*0.05))
    print("现金{}，占比{:.2%}".format(CASH, CASH/current_all_cost))
