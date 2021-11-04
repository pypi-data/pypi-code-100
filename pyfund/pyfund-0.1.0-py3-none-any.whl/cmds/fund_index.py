import concurrent.futures as cf
import json
import os
import sys

import akshare as ak
import arrow
import click
import pandas as pd
import pyfund
from pyfund import __data_path__
from pyfund.cmds import init_fund
from pyfund.net import sina
from rich import print
from rich.progress import track


@click.command()
def fund_index():
    """指数基金"""
    print("初始化数据库...", end="")
    fdb = init_fund.FundDB()
    print("OK")

    df = pd.DataFrame(
        columns=["代码", "名称", "类型", "周", "1月", "3月", "6月", "1年", "2年", "3年", "规模", "手续费"]
    )

    for _, item in track(
        fdb.fund_rank_all_df.iterrows(), total=len(fdb.fund_rank_all_df)
    ):
        name = item["基金简称"]
        if (
            name.endswith("C")
            or name.endswith("B")
            or name.endswith("D")
            or name.endswith("E")
        ):
            continue

        code = item["基金代码"]
        ftype = fdb.get_type(code)
        if "指数" not in ftype:
            continue

        week = item["近1周"]
        month = item["近1月"]
        month3 = item["近3月"]
        month6 = item["近6月"]
        year = item["近1年"]
        year2 = item["近2年"]
        year3 = item["近3年"]

        if pd.isnull(year3):  # 成立至少3年
            continue

        if year > 0 and year2 > 0 and year3 > 0:
            continue

        scale = fdb.get_scale(code)
        if scale < 1:
            continue

        fee = item["手续费"]
        line = [
            code,
            name,
            ftype,
            week,
            month,
            month3,
            month6,
            year,
            year2,
            year3,
            round(scale),
            fee,
        ]
        df.loc[len(df)] = line

    df.to_csv(os.path.join(__data_path__, "funds-index.csv"))
