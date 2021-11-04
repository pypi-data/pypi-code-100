"""读入股票持有信息，输出权重、比例、收益率"""
import arrow
import click
import pandas as pd

from pyfund.net import sina
import math


@click.command()
@click.argument('filename')
@click.option('-p', '--period', default=3, type=int, help="时间间隔，单位年，1表示一年")
def corrcoef(filename, period):
    """对股票的相关性进行计算
    """
    codes = []
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            if '#' in line:
                continue
            codes.append(line.split(',')[0].strip())
    
    now = arrow.now()
    end = now.date()
    start = now.shift(years=-period).date()
    print(start, end)
    sina.corrcoef(codes, start, end)
    stocks, names, result = sina.corrcoef(codes, start, end)

    df = pd.DataFrame(columns=stocks.keys(), index=names)

    from rich_dataframe import prettify

    dicts = {}  # 存放相关度高的组合。
    keys = set()  # 存放名称
    for k, v in result.get('result', {}).get('data', {}).items():
        a, b = k.split('_')  # 2个代码由_连接而成，v是它们的相关度
        if a == b:
            continue
        key1 = stocks[a]  # 获得名称
        keys.add(key1)  # 存放所有的名称
        df.loc[key1, b] = v  # 写入df

        if v == '':
            continue

        key2 = stocks[b]  # 获得b的名称
        if float(v) >= 0.8:
            if key1 in dicts:
                dicts[key1].add(key2)
            else:
                dicts[key1] = {key2}

    prettify(df, col_limit=20)

    sizes = []  # 代码 - 有多少个相关度高的代码
    for k, v in dicts.items():
        sizes.append((k, len(v)))

    skip_keys = set()  # 表示已经处理过的keys，不再做任何处理
    # 相关度指数，关联的指数数量越多的，优先处理
    for item in sorted(sizes, key=lambda x: x[1], reverse=True):
        key = item[0]
        if key in skip_keys:
            continue
        values = dicts[key]
        for v in values:
            if v in skip_keys:
                continue
            keys.remove(v)  # 删除相关度高的指数
            skip_keys.add(v)  # 后面不再处理该指数，因为高相关度的指数已经被处理
        skip_keys.add(key)


    for item in keys:  # 存放相关度低的指数
        for k, v in stocks.items():
            if item != v:
                continue
            if v in dicts:
                print(k, v, dicts[v])
            else:
                print(k, v)

    if len(codes) > 20:
        return
    # ! 生成所有的组合
    print("-" * 80)

    ss = set()  # 存放名称
    datas = result.get('result', {}).get('data', {})

    all_codes = set() # 存放所有的指数代码
    for k, v in datas.items():
        a, _ = k.split('_')  # 2个代码由_连接而成，v是它们的相关度
        all_codes.add(a)
    
    n = len(all_codes)
    items = list(all_codes)
    print("开始生成所有的子集")
    sub_codes = get_sub_set(items)
    print("生成成功", len(sub_codes))
    
    zuhe = []
    for item in sorted(sub_codes, key=lambda x: len(x), reverse=True):
        
        flag = False
        for one in zuhe:
            if set(item).issubset(one):
                flag = True
                break
        if flag:
            continue

        if len(item) == 0:
            continue
        if len(item) == 1:
            print(item)
            continue
        if has_big(datas, item):
            continue

        zuhe.append(set(item))
        print(item, sorted([stocks[i] for i in item]))

def get_sub_set(a_set, size=-1):
    res = [[]]
    for item in a_set:
        res += [ i + [item] for i in res]
    
    if size != -1:
        result = []
        for item in res:
            if len(item) == size:
                result.append(item)
        return result
    return res


def is_big(datas, x, y):
    k = x+ '_' + y
    v = datas.get(k)
    if v == '':
        return True
    v = float(v)
    return v >= 0.8

def has_big(datas, _codes):
    subs = get_sub_set(_codes, 2)
    for item in subs:
        if is_big(datas, item[0], item[1]):
            return True
    return False