#! /usr/bin/env python3
"""
@author  : MG
@Time    : 2021/9/17 10:54
@File    : cta_signal.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging
import math
import weakref
from typing import Callable, Optional

from vnpy.app.cta_strategy import (
    BarData,
    CtaSignal as CtaSignalBase,
)
from vnpy.trader.constant import Interval
from vnpy.trader.object import TickData

from vnpy_extra.constants import SYMBOL_MINUTES_COUNT_DIC
from vnpy_extra.utils.enhancements.am import ArrayManager, PriceTypeEnum
from vnpy_extra.utils.enhancements.bg import BarGenerator
from vnpy_extra.utils.symbol import get_instrument_type


def get_daily_min_bar_count(symbol: Optional[str] = None):
    """返回每天有多少分钟线数据"""
    if symbol is None:
        return 350
    instrument_type = get_instrument_type(symbol)
    min_bar_count = SYMBOL_MINUTES_COUNT_DIC[instrument_type.upper()]
    return min_bar_count


class PublicSignal(CtaSignalBase):

    def __init__(self, period: int, array_size: int, interval: Interval = Interval.MINUTE, *,
                 strict=False, base_price_type=PriceTypeEnum.close.name,
                 strategy_obj=None, generate_daily=False, win_bar_log=False, **kwargs):
        """

        :param period 周期数
        :param array_size 行情队列大小
        :param interval 周期类型
        :param strict 是否使用 strict 模式生成 window bar
        :param base_price_type 基础价格类型，用于计算 am 的指标
        :param strategy_obj 策略实例
        :param generate_daily 是否计算daily数据
        """
        super().__init__()
        self.period = period
        self.interval = interval
        self.array_size = array_size
        # 2021-07-29 MG
        # 回测状态下无法通过 tick 合成 bar 而是直接通过 template 的 on_bar 事件，将 bar 传入 bg.on_bar(bar)
        # 为了避免实盘情况下，on_tick 合成 bar 与 on_bar 中bar重复调用 bg.on_bar 的问题，这里将 bg 的 on_bar 事件替换掉
        self.bg = BarGenerator(
            on_bar=lambda bar: bar, window=self.period, on_window_bar=self.on_window, interval=self.interval,
            strict=strict)
        self.am = ArrayManager(size=array_size, base_price_type=base_price_type)
        self._generate_daily = generate_daily
        self.bg_daily: Optional[BarGenerator] = BarGenerator(
            window=1,
            on_bar=lambda _: _,
            on_window_bar=lambda bar: self.am_daily.update_bar(bar),
            interval=Interval.DAILY,
            strict=strict
        ) if generate_daily else None
        self.am_daily = ArrayManager(size=array_size)
        self.win_bar_log = win_bar_log
        self.bar: Optional[BarData] = None
        self.win_bar: Optional[BarData] = None
        self.win_bar_count = 0

        from vnpy_extra.backtest.cta_strategy.template import CtaTemplate
        from vnpy_extra.backtest.portfolio_strategy.template import StrategyTemplate
        if strategy_obj:
            if not isinstance(strategy_obj, CtaTemplate) and not isinstance(strategy_obj, StrategyTemplate):
                raise ValueError(f"{strategy_obj}{type(strategy_obj)} 必須是 CtaTemplate 或 StrategyTemplate 的子类")
            self._strategy_obj: Callable[[], Optional[CtaTemplate]] = weakref.ref(strategy_obj)
        else:
            raise ValueError(f"{self.__class__.__name__} 需要传入 strategy_obj 参数")

        self.logger = logging.getLogger(strategy_obj.strategy_name)

    @property
    def strategy_parameters(self):
        return self._strategy_obj().parameters

    @property
    def current_bar_daily(self):
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.bg_daily.last_finished_bar if self.bg_daily.window_bar is None else self.bg_daily.window_bar

    @property
    def generate_daily(self) -> bool:
        return self._generate_daily

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.bar = bar
        self.bg.update_bar(bar)
        if self.bg_daily:
            self.bg_daily.update_bar(bar)

    def on_window(self, bar: BarData):
        """"""
        self.am.update_bar(bar)
        self.win_bar = bar
        self.win_bar_count += 1

    @classmethod
    def get_short_name(cls, name: Optional[str] = None) -> str:
        """返回信号简称，用于设置 signal_name_list 以及相应的参数头部字段"""
        if hasattr(cls, "short_name"):
            short_name = getattr(cls, "short_name")
        else:
            signal_cls_name = cls.__name__.lower() if name is None else name
            short_name = signal_cls_name[:-len('signal')] if signal_cls_name.endswith(
                'signal') else signal_cls_name
        return short_name

    @classmethod
    def get_signal_name_header(cls, name: Optional[str] = None) -> str:
        """返回类名称剔除尾部 Signal"""
        signal_cls_name = cls.__name__ if name is None else name
        cls_name_header = signal_cls_name[:-len('Signal')] if signal_cls_name.endswith(
            'Signal') else signal_cls_name
        return cls_name_header

    @property
    def market_position(self):
        return self._strategy_obj().pos

    @property
    def current_bar(self):
        return self.bg.last_finished_bar if self.bg.window_bar is None else self.bg.window_bar

    @property
    def open_current(self):
        return self.current_bar.open_price

    @property
    def high_current(self):
        return self.current_bar.high_price

    @property
    def low_current(self):
        return self.current_bar.low_price

    @property
    def close_current(self):
        return self.current_bar.close_price

    @property
    def volume_current(self):
        return self.current_bar.volume

    @property
    def open(self):
        return self.am.open_array[-1]

    @property
    def high(self):
        return self.am.high_array[-1]

    @property
    def low(self):
        return self.am.low_array[-1]

    @property
    def close(self):
        return self.am.close_array[-1]

    @property
    def volume(self):
        return self.am.volume_array[-1]

    @property
    def open_array(self):
        return self.am.open_array

    @property
    def high_array(self):
        return self.am.high_array

    @property
    def low_array(self):
        return self.am.low_array

    @property
    def close_array(self):
        return self.am.close_array

    @property
    def volume_array(self):
        return self.am.volume_array

    @property
    def open_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.open_price

    @property
    def high_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.high_price

    @property
    def low_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.low_price

    @property
    def close_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.close_price

    @property
    def volume_daily_current(self) -> float:
        """当天的日级别信号(当前bar还未完成)"""
        if not self._generate_daily:
            raise AttributeError(f'generate_daily={self._generate_daily} 需要设置为 True')
        return self.current_bar_daily.volume

    @property
    def open_daily_array(self):
        return self.am_daily.open_array

    @property
    def high_daily_array(self):
        return self.am_daily.high_array

    @property
    def low_daily_array(self):
        return self.am_daily.low_array

    @property
    def close_daily_array(self):
        return self.am_daily.close_array

    @property
    def volume_daily_array(self):
        return self.am_daily.volume_array


class CtaSignal(PublicSignal):

    def __init__(self, period: int, array_size: int, interval: Interval = Interval.MINUTE, *, filter_n_available=1,
                 strict=False, base_price_type=PriceTypeEnum.close.name, vt_symbol=None,
                 strategy_obj=None, generate_daily=False, **kwargs):
        """

        :param period 周期数
        :param array_size 行情队列大小
        :param interval 周期类型
        :param filter_n_available 有效信号过滤器,超过指定次数后才真正改变 signal_pos 信号数值
        :param strict 是否使用 strict 模式生成 window bar
        :param base_price_type 基础价格类型，用于计算 am 的指标
        :param vt_symbol 合约
        :param strategy_obj 策略实例
        :param generate_daily 是否计算daily数据
        """
        super().__init__(
            period, array_size, interval, strict=strict, base_price_type=base_price_type,
            strategy_obj=strategy_obj, generate_daily=generate_daily, **kwargs)

        self.filter_n_available = filter_n_available
        self._n_available_counter = 0
        self._n_available_pos = self.signal_pos
        self.vt_symbol = vt_symbol
        # 一跳价格单位
        self.price_scale = getattr(strategy_obj, "vt_symbol_price_tick", 1)
        # 记录上一状态时的 market_position
        self._market_position_last_window_bar = 0

        # 对应 TB 中用于记录上一次进场到现在的数量
        self.bar_count_since_entry = 0
        # 对应 TB 中用于记录上一次出场到现在的数量
        self.bar_count_since_exit = 0

        # 记录最小的 high
        self._min_high_after_entry = 0
        # 记录最大的 low
        self._max_low_after_entry = 0
        # 记录上一根 win bar时的对应变量
        self._min_high_after_entry_last = 0
        self._max_low_after_entry_last = 0

    def on_window(self, bar: BarData):
        """"""
        super().on_window(bar)
        market_position_temp = self.market_position
        market_position = market_position_temp if isinstance(market_position_temp, int) \
            else market_position_temp.get(self._strategy_obj().vt_symbol1, 0)

        self._max_low_after_entry_last = self._max_low_after_entry
        self._min_high_after_entry_last = self._min_high_after_entry
        if market_position != 0:
            if (
                    self._market_position_last_window_bar <= 0 < market_position
            ) or (
                    self._market_position_last_window_bar >= 0 > market_position
            ):
                # 首次建仓或者仓位反转
                self.bar_count_since_entry = self.win_bar_count
                self._max_low_after_entry = bar.low_price
                self._min_high_after_entry = bar.high_price
            else:
                # 持仓期间更新相关价格
                self._max_low_after_entry = max(self._max_low_after_entry, bar.low_price)
                self._min_high_after_entry = min(self._min_high_after_entry, bar.high_price)

        elif self._market_position_last_window_bar != 0 and market_position == 0:
            self.bar_count_since_exit = self.win_bar_count
            self._max_low_after_entry = 0
            self._min_high_after_entry = 0

        self._market_position_last_window_bar = market_position

    def set_signal_pos(self, signal_pos, ignore_filter=False):
        """对 set_signal_pos 增加过滤器,重复超过 self.filter_n_available 次时才算有效"""
        if ignore_filter or signal_pos != self._n_available_pos:
            self._n_available_pos = signal_pos
            self._n_available_counter = 1
        else:
            self._n_available_counter += 1

        if ignore_filter or self._n_available_counter >= self.filter_n_available:
            super().set_signal_pos(signal_pos)

    def daily_bars_needed_at_least(self, symbol: Optional[str] = None):
        """返回至少需要多少日线数据"""
        if symbol is None:
            symbol = self.vt_symbol

        if self.interval == Interval.MINUTE:
            min_bar_count = get_daily_min_bar_count(symbol)
            step = 1 / min_bar_count
        elif self.interval == Interval.HOUR:
            min_bar_count = get_daily_min_bar_count(symbol)
            step = 60 / min_bar_count
        elif self.interval == Interval.DAILY:
            step = 1
        elif self.interval == Interval.WEEKLY:
            step = 7
        else:
            raise ValueError(f"interval={self.interval} 无效")

        daily_bar_count = math.ceil(self.period * self.am.size * step)
        if self.interval != Interval.WEEKLY:
            daily_bar_count *= 1.5

        return daily_bar_count

    @property
    def bars_since_entry(self):
        if self.bar_count_since_entry == 0:
            return 0
        else:
            return self.win_bar_count - self.bar_count_since_entry

    @property
    def bars_since_exit(self):
        return self.win_bar_count - self.bar_count_since_exit if self.bar_count_since_exit != 0 else 0

    @property
    def entry_price(self):
        return self._strategy_obj().entry_price

    @property
    def exit_price(self):
        return self._strategy_obj().exit_price

    @property
    def lowest_after_entry(self):
        return self._strategy_obj().lowest_after_entry

    @property
    def highest_after_entry(self):
        return self._strategy_obj().highest_after_entry

    @property
    def max_low_after_entry(self):
        return self._max_low_after_entry

    @property
    def min_high_after_entry(self):
        return self._min_high_after_entry

    @property
    def max_low_after_entry_last(self):
        return self._max_low_after_entry_last

    @property
    def min_high_after_entry_last(self):
        return self._min_high_after_entry_last


class CtaExitSignal(CtaSignal):
    """
    出场信号
    set_stop_order_price 设置停止单出场价格
    fire_exit_signal 激活出场信号
    reset_exit_signal 重置信号状态
    不要使用 set_signal_pos 参数
    """

    def __init__(self, period: int, array_size: int, *,
                 strategy_obj, enable_on_tick_signal=False, enable_on_bar_signal=True, **kwargs):
        """
        用于产生平仓信号
        :param period 周期数
        :param array_size 行情队列大小
        :param strategy_obj 策略实例
        :param enable_on_tick_signal tick级别信号更新
        :param enable_on_bar_signal bar 级别信号更新
        """
        super().__init__(period=period, array_size=array_size, strategy_obj=strategy_obj, **kwargs)
        self.enable_on_tick_signal = enable_on_tick_signal
        self.enable_on_bar_signal = enable_on_bar_signal
        # 用于记录当前信号从产生平仓信号前的持仓状态：持仓N
        # self._close_from_position != 0 即为平仓信号
        self._close_from_position = 0
        # 信号为 None：代表不对进场信号进行干预
        self.signal_pos = None
        # 上一次仓位改变时的仓位状态
        # self.last_pos = 0
        # 指定平仓价格
        self.stop_order_price = 0
        self.kwargs = kwargs

    def on_tick(self, tick: TickData):
        if self.enable_on_tick_signal:
            # 平仓信号出现之前，与当前持仓保持一致
            self._check_and_reset_signal_pos()

        super().on_tick(tick)

    def on_bar(self, bar: BarData):
        if self.enable_on_bar_signal:
            # 平仓信号出现之前，与当前持仓保持一致
            self._check_and_reset_signal_pos()

        super().on_bar(bar)

    def reset_exit_signal(self):
        """重置平仓信号：仓位方向已经调整，此前平仓信号将被重置"""
        self._close_from_position = 0
        self.stop_order_price = 0
        self.signal_pos = None

    def _check_and_reset_signal_pos(self):
        """
        以下条件成立时，重置状态
        1）持仓与信号方向不一致

        pos == 0 的情况下不会重置信号，是为了防止出现信号抖动的情况，导致频繁进出场
        """
        pos = self.market_position
        # if self.last_pos == pos:
        #     return
        if self._close_from_position < 0 < pos or pos < 0 < self._close_from_position:
            # 重置平仓信号：仓位方向已经调整，此前平仓信号将被重置
            self.reset_exit_signal()

        # self.last_pos = pos

    def fire_exit_signal(self):
        pos = self.market_position
        if pos == 0:
            return
        # 触发平仓信号，pos != 0。
        # 记录平仓信号发出时，持仓状态。
        self._close_from_position = pos
        super().set_signal_pos(signal_pos=0, ignore_filter=True)

    def get_signal_pos(self) -> int:
        return self.signal_pos

    def set_stop_order_price(self, price):
        """设置停损价格，当多头时，价格低于此价格将强制平仓，当空头是，价格高于此价格将强制平仓"""
        pos = self.market_position
        if pos == 0:
            return
        # 触发平仓信号，但当前持仓！=0。
        # 记录平仓信号发出时，持仓状态。
        self._close_from_position = pos
        self.stop_order_price = price

    def set_signal_pos(self, signal_pos, ignore_filter=False):
        raise ValueError("出场信号类不允许使用 set_signal_pos 方法")
