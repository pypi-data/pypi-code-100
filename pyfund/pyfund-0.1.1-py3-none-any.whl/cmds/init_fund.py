import os

import akshare as ak
import click
import pandas as pd
import pyfund
from pyfund import __data_path__

path_fund_manager = os.path.join(__data_path__, "fund", "fund_manager.csv")  # 基金经理
path_fund_name = os.path.join(__data_path__, "fund", "fund_name.csv")  # 基金名称
path_fund_rank_all = os.path.join(__data_path__, "fund", "fund_rank_all.csv")  # 基金排行
path_fund_daily = os.path.join(
    __data_path__, "fund", "fund_daily.csv"
)  # 基金实时净值，申赎状态，规模
path_fund_scale = os.path.join(__data_path__, "fund", "fund_scale.csv")  # 基金规模


class FundManagerDB:
    def __init__(self):
        self.df = pd.read_csv(path_fund_manager)

    def get_managers(self, name):
        """根据基金名称，查询基金经理(可能有多个)

        :param name: [description]
        :type name: [type]
        :raises Exception: [description]
        :return: [description]
        :rtype: [type]
        """
        name = name.replace("(", ".").replace(")", ".")
        return self.df[self.df["现任基金"].str.contains(name, na=False)].reset_index(
            drop=True
        )


class FundNameDB:
    def __init__(self):
        self.df = pd.read_csv(path_fund_name, dtype={"基金代码": str})

    def get_code(self, name):
        x = self.df[self.df["基金简称"].str.contains(name, na=False)].reset_index(drop=True)
        try:
            return x["基金代码"][0]
        except:
            raise Exception

    def get_type(self, code):
        x = self.df[self.df["基金代码"] == code].reset_index(drop=True)
        try:
            return x["基金类型"][0]
        except:
            print(code)
            raise Exception


class FundDB(object):
    def __init__(self):
        """初始化所有的数据"""
        self.fund_manager_df = pd.read_csv(path_fund_manager, dtype={"基金代码": str})
        self.fund_name_df = pd.read_csv(path_fund_name, dtype={"基金代码": str})
        self.fund_rank_all_df = pd.read_csv(path_fund_rank_all, dtype={"基金代码": str})
        self.fund_rank_daily_df = pd.read_csv(path_fund_daily, dtype={"基金代码": str})
        self.fund_rank_scale_df = pd.read_csv(path_fund_scale, dtype={"基金代码": str})

    def get_code(self, name):
        """根据名字，获取代码

        :param name: [description]
        :type name: [type]
        :raises Exception: [description]
        :return: [description]
        :rtype: [type]
        """
        x = self.fund_name_df[
            self.fund_name_df["基金简称"].str.contains(name, na=False)
        ].reset_index(drop=True)
        try:
            return x["基金代码"][0]
        except:
            raise Exception

    def get_type(self, code):
        """根据代码，获取类型

        :param code: [description]
        :type code: [type]
        :raises Exception: [description]
        :return: [description]
        :rtype: [type]
        """
        x = self.fund_name_df[self.fund_name_df["基金代码"] == code].reset_index(drop=True)
        try:
            return x["基金类型"][0]
        except:
            print(code)
            raise Exception

    def get_managers(self, name):
        """根据基金名称，查询基金经理(可能有多个)

        :param name: [description]
        :type name: [type]
        :raises Exception: [description]
        :return: [description]
        :rtype: [type]
        """
        name = name.replace("(", ".").replace(")", ".")
        return self.fund_manager_df[
            self.fund_manager_df["现任基金"].str.contains(name, na=False)
        ].reset_index(drop=True)

    def get_scale(self, code):
        # 单位净值,总募集规模,最近总份额
        x = self.fund_rank_scale_df[
            self.fund_rank_scale_df["基金代码"] == code
        ].reset_index(drop=True)
        try:
            v = x["单位净值"][0]
            n = x["最近总份额"][0]
            return v * n / 1_0000_0000
        except:
            # 165519
            print(code)
            raise Exception

    def get_established_time(self, code):
        """成立时间

        :param code: [description]
        :type code: [type]
        :raises Exception: [description]
        :return: [description]
        :rtype: [type]
        """
        x = self.fund_rank_scale_df[
            self.fund_rank_scale_df["基金代码"] == code
        ].reset_index(drop=True)
        try:
            return x["成立日期"][0]
        except:
            print(code)
            raise Exception


@click.command()
def init_fund():
    """初始化基金数据"""
    if not os.path.exists(os.path.join(pyfund.__data_path__, "fund")):
        os.makedirs(os.path.join(pyfund.__data_path__, "fund"))

    print("开始初始化基金基本信息数据……")
    fund_name_df = ak.fund_em_fund_name()
    fund_name_df.to_csv(path_fund_name)

    print("开始初始化基金经理数据……")
    fund_manager_df = ak.fund_manager(explode=False)
    fund_manager_df.to_csv(path_fund_manager)

    print("开始初始化全部类型的基金排行数据……")
    df = ak.fund_em_open_fund_rank(symbol="全部")
    df.to_csv(path_fund_rank_all)

    print("开始初始化基金净值-实时数据……")
    # 申购状态、赎回状态、手续费
    df = ak.fund_em_open_fund_daily()
    df.to_csv(path_fund_daily)

    print("开始初始化基金规模数据……")
    dfs = []
    dfs.append(ak.fund_scale_open_sina(symbol="股票型基金"))

    for key in ["混合型基金", "债券型基金", "QDII基金"]:
        dfs.append(ak.fund_scale_open_sina(symbol=key))

    dfs.append(ak.fund_scale_close_sina())
    dfs.append(ak.fund_scale_structured_sina())

    df = pd.concat(dfs).reset_index(drop=True)

    df.to_csv(path_fund_scale)
