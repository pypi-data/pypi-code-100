# -*- coding:utf-8 -*-
from time import perf_counter, sleep


class Timer(object):
    """用于记录时间间隔的工具"""

    def __init__(self) -> None:
        self.times = []

    def record(self, show: bool = False) -> None:
        self.times.append(perf_counter())
        if show:
            if len(self.times) > 1:
                print(self.times[-1] - self.times[-2])
            else:
                print(0)

    def show(self) -> None:
        for k in range(1, len(self.times)):
            print(f't{k}-t{k - 1}: {self.times[k] - self.times[k - 1]}')


tt = Timer()
# sleep(.1)
tt.record(True)
sleep(.2)
tt.record(True)
tt.show()
