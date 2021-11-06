import abc
from random import randint

import arrow
import click
import numpy as np
import pandas as pd

from pyfund.net import xueqiu
from pyfund.backtesting import BackTesting
from pyfund.strategies import bull, day, week


@click.command()
@click.argument('code')
def backtest(code):
    bt = BackTesting()
    bt.load_datas(code, xueqiu.Period.WEEK)
    bt.load_strategy(week.Strategy())
    bt.set_start_date('2020-01-01')
    bt.run()
