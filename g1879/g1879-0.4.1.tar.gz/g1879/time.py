# -*- coding:utf-8 -*-
from time import perf_counter


class Timer(object):
    """用于记录时间间隔的工具"""

    def __init__(self) -> None:
        self.times = []

    def record(self, show: bool = False) -> None:
        """记录一个时间点
        :param show: 是否打印与上一个时间点的差
        :return: None
        """
        self.times.append(perf_counter())
        if show:
            len_times = len(self.times)
            print(self.times[-1] - self.times[len_times - 2])

    def show(self) -> None:
        """打印所有时间差"""
        for k in range(1, len(self.times)):
            print(f't{k}-t{k - 1}: {self.times[k] - self.times[k - 1]}')
