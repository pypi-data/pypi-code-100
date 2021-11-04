from pyfund.net import eastmoney, sina, xueqiu



def get_cur_point(index_code):
    cp = sina.get_cur_point(index_code)
    if cp is None or cp == 0.0:
        cp = xueqiu.get_cur_point(index_code)

    print(index_code, cp)


def get_cur_price(code: str):
    """获取当前价格

    Args:
        code (str): 基金代码

    Returns:
        [float]: 基金价格
    """
    fund = eastmoney.Fund(code)
    price = fund.get_cur_price()
    if price:
        return price

    price = fund.get_price()
    if price:
        return price

    print(code, 'COULD NOT GET PRICE!')


def get_price(code: str, date=''):
    """获取某天单位净值，默认最近一天

    Args:
        code (str): 基金码
        date ([type], optional): 日期. Defaults to '':str.
    """
    pass
