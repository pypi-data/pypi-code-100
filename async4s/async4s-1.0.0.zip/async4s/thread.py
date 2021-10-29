#!/usr/bin/env python
from __future__ import annotations

import multiprocessing
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread
from typing import Any, Callable, Iterable, List, Sequence


__all__ = ["Master", "Worker"]


class Master(object):
    def __init__(self, workers: Iterable[Worker], callback: Callable[[Sequence], Any] = None, max_workers: int = None):
        if max_workers is None:
            max_workers = multiprocessing.cpu_count()
        self._worker_pool = ThreadPoolExecutor(max_workers=max_workers)
        self._results: List[Future] = []
        for worker in workers:
            t = self._worker_pool.submit(worker)
            self._results.append(t)
        self._callback = callback
        self._master = Thread(target=self.on_finished, daemon=True)
        self._master.start()

    def on_finished(self):
        result = [i.result() for i in self._results]
        if self._callback is not None:
            return self._callback(result)

    def wait(self):
        self._master.join()


class Worker(object):
    def __init__(self, func, *args, **kargs):
        self._func = func
        self._args = args
        self._kargs = kargs

    def __call__(self):
        return self._func(*self._args, **self._kargs)
