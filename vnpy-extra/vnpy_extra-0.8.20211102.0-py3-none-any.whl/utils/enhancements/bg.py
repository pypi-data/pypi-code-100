#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/9/17 10:56
@File    : bg.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""

import logging
from datetime import time
from typing import Callable, Optional

from ibats_utils.mess import get_first
from vnpy.app.cta_strategy import (
    BarData,
    BarGenerator as BarGeneratorBase,
)
from vnpy.trader.constant import Interval


class BarGenerator(BarGeneratorBase):
    def __init__(
            self,
            on_bar: Callable,
            window: int = 0,
            on_window_bar: Callable = None,
            interval: Interval = Interval.MINUTE,
            strict=False
    ):
        super().__init__(on_bar, window, on_window_bar, interval)
        # self.instrument_type = None
        # 统一按照 15点整收盘计算
        self.trade_end_time = time(15, 0, 0)
        # 记录上一个触发 self.on_window_bar 的 bar 实例
        self.last_finished_bar = None
        # 记录 1m bar的数量
        self.bar_count = 0
        # 记录 有多少根bar合成一个win_bar
        self.bar_count_of_window_bar = 0
        # 记录上一次生产 window_bar 时，对应的 bar_count
        self._last_finished_bar_no = 0
        self.strict = strict
        # 记录上一次 (bar.datetime.minute + 1) % self.window 的余数结果
        self._last_mod_remainder = 0
        self.logger = logging.getLogger(self.__class__.__name__)

    def is_end_day(self, bar):
        """判断交易日是否结束，以15点作为分界点"""
        is_end = bar.datetime.time() == self.trade_end_time
        if not is_end:
            if self.last_bar.datetime.date() == bar.datetime.date():
                # 有夜盘的情况
                is_end = self.last_bar != self.last_finished_bar and \
                         self.last_bar.datetime.hour <= 15 < bar.datetime.hour
            else:
                # 没有夜盘的情况
                is_end = self.last_bar != self.last_finished_bar and \
                         9 <= bar.datetime.hour < self.last_bar.datetime.hour <= 15

        return is_end

    def is_end_week(self, bar):
        """判断但却bar是否是周末最后一根"""
        # isocalendar()[:2] 匹配年号和周数
        # if self.is_end_day(bar):
        #     # 判断当日是否是收盘时间，且即将跨周(周五+2天为周日，跨周）
        #     # 该逻辑不够严谨，对于周一跨周的计算机需要+3，这里暂不考虑
        #
        #     is_end = (bar.datetime + timedelta(days=2)).isocalendar()[:2] != self.last_bar.datetime.isocalendar()[:2]
        # else:
        #     # 有些情况下，当前最后一个时段bar没有，这种情况下只能通过下一个交易日的bar与当前bar周数是否一致来判断
        #     is_end = bar.datetime.isocalendar()[:2] != self.last_bar.datetime.isocalendar()[:2]
        if not self.is_end_day(bar):
            return False
        # from vnpy_extra.db.orm import TradeDateModel 不能放在外层引用，会导致循环引用问题。
        # orm包中部分功能会用到 enhancement.py 中的功能
        from vnpy_extra.db.orm import TradeDateModel
        next_trade_date_dic, _ = TradeDateModel.get_trade_date_dic()
        win_bar_date = self.window_bar.datetime.date()
        if win_bar_date in next_trade_date_dic:
            next_day_dt = next_trade_date_dic[win_bar_date]
            is_end = next_day_dt.isocalendar()[:2] != win_bar_date.isocalendar()[:2]
        else:
            date_time_list = list(next_trade_date_dic.keys())
            date_time_list.sort()
            next_day_date = get_first(date_time_list, lambda x: x > win_bar_date)
            if next_day_date is None:
                self.logger.error(f"TradeDateModel 数据有误,没有找到 {win_bar_date} 以后的交易日数据")
                is_end = False
            else:
                is_end = next_day_date.isocalendar()[:2] != win_bar_date.isocalendar()[:2]

        return is_end

    def is_end_month(self, bar):
        """判断但却bar是否是月末最后一根（下一个大版本时再启用）"""
        if not self.is_end_day(bar):
            return False
        from vnpy_extra.db.orm import TradeDateModel
        next_trade_date_dic, _ = TradeDateModel.get_trade_date_dic()
        win_bar_date = self.window_bar.datetime.date()
        if win_bar_date in next_trade_date_dic:
            next_day_dt = next_trade_date_dic[win_bar_date]
            is_end = next_day_dt.year != win_bar_date.year or next_day_dt.month != win_bar_date.month
        else:
            date_time_list = list(next_trade_date_dic.keys())
            date_time_list.sort()
            next_day_date = get_first(date_time_list, lambda x: x > win_bar_date)
            is_end = next_day_date.year != win_bar_date.year or next_day_date.month != win_bar_date.month

        return is_end

    def update_bar(self, bar: BarData) -> None:
        """
        Update 1 minute bar into generator
        """
        if bar is None:
            return
        self.bar_count += 1
        # if self.instrument_type is None:
        #     self.instrument_type = get_instrument_type(bar.symbol)
        #     if self.instrument_type in INSTRUMENT_TRADE_TIME_PAIR_DIC:
        #         self.trade_end_time = INSTRUMENT_TRADE_TIME_PAIR_DIC[self.instrument_type][1]
        #     else:
        #         self.logger.error("当前合约 %s 对应品种 %s 没有对应的交易时段，默认15点收盘",
        #                      bar.symbol, self.instrument_type)
        #         self.trade_end_time = time(15, 0, 0)

        # If not inited, create window bar object
        if not self.window_bar:
            # Generate timestamp for bar data
            if self.interval == Interval.MINUTE:
                dt = bar.datetime.replace(second=0, microsecond=0)
            else:
                dt = bar.datetime.replace(minute=0, second=0, microsecond=0)

            self.window_bar = BarData(
                symbol=bar.symbol,
                exchange=bar.exchange,
                datetime=dt,
                gateway_name=bar.gateway_name,
                open_price=bar.open_price,
                high_price=bar.high_price,
                low_price=bar.low_price
            )
            self.bar_count_of_window_bar = 0
        # Otherwise, update high/low price into window bar
        else:
            self.window_bar.high_price = max(
                self.window_bar.high_price, bar.high_price)
            self.window_bar.low_price = min(
                self.window_bar.low_price, bar.low_price)
            self.bar_count_of_window_bar += 1

        # Update close price/volume into window bar
        self.window_bar.close_price = bar.close_price
        self.window_bar.volume += int(bar.volume)
        self.window_bar.open_interest = bar.open_interest

        # Check if window bar completed
        finished = False

        if self.interval == Interval.MINUTE:
            # x-minute bar
            if self.strict:
                remainder = (bar.datetime.minute + 1) % self.window
                if self.bar_count_of_window_bar == 1 < self.window:
                    # self.window > 1 的情况下不允许单根bar形成 window_bar
                    pass
                elif remainder == 0 or remainder < self._last_mod_remainder:
                    # remainder < self._last_mod_remainder 说明跨时间段情况出现。
                    # 例如：30分钟周期情况下 10:15 交易所进入休息时段，下一次开盘时间10:30。
                    # 用 (bar.datetime.minute + 1) % self.window 的逻辑将错过此次bar生成。
                    # 而在当前逻辑下，将会在10:30分时生成一个 10:00 ~ 10:15时段的 bar 最为 30m bar
                    finished = True

                self._last_mod_remainder = remainder
            elif not (bar.datetime.minute + 1) % self.window:
                finished = True

        elif self.interval == Interval.HOUR:
            if self.last_bar:
                new_hour = self.last_finished_bar != self.last_bar and bar.datetime.hour != self.last_bar.datetime.hour
                last_minute = bar.datetime.minute == 59

                if new_hour or last_minute:
                    # 1-hour bar
                    if self.window == 1:
                        finished = True
                    # x-hour bar
                    else:
                        self.interval_count += 1

                        if not self.interval_count % self.window:
                            finished = True
                            self.interval_count = 0

        elif self.interval == Interval.DAILY:
            if self.last_bar and self.last_finished_bar != self.last_bar and self.is_end_day(bar):
                # 1-day bar
                if self.window == 1:
                    finished = True
                # x-day bar
                else:
                    self.interval_count += 1

                    if not self.interval_count % self.window:
                        finished = True
                        self.interval_count = 0
        elif self.interval == Interval.WEEKLY:
            if self.last_bar and self.last_finished_bar != self.last_bar and self.is_end_week(bar):
                # 1-day bar
                if self.window == 1:
                    finished = True
                # x-day bar
                else:
                    self.interval_count += 1

                    if not self.interval_count % self.window:
                        finished = True
                        self.interval_count = 0

        # 判断是否当前 bar 结束
        if finished:
            self.on_window_bar(self.window_bar)
            self.last_finished_bar = bar
            self._last_finished_bar_no = self.bar_count
            self.window_bar: Optional[BarData] = None
            self.bar_count_of_window_bar = 0

        # Cache last bar object
        self.last_bar = bar
