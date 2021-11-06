import arrow
import click
import numpy as np
import pandas as pd
from pyfund import constants, core, to_per
from pyfund.net import xueqiu
from rich import print
from tabulate import tabulate


@click.command()
@click.argument('code')
def test(code):
    """获取数据
    """
    dp = core.DataProcessor('SZ000656')
    d = dp.get_last_day()
    print(d)
    print(d.__dict__)
    print(len(d.__dict__))
    print(d.get(constants.I_PB))
    print(d.get(constants.I_MACD))
    dp.clean_cache()
