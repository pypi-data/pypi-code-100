#!/usr/bin/env python
from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine, Iterable, Sequence

__all__ = ["Master", "Worker"]


class Master(object):
    def __init__(self, workers: Iterable[Worker], callback: Callable[[Sequence], Any] = None):
        self._worker_tasks = [asyncio.ensure_future(worker()) for worker in workers]
        self._callback = callback
        self._master_task = asyncio.ensure_future(self.on_finished())

    async def on_finished(self):
        results = await asyncio.gather(*self._worker_tasks)
        if self._callback is not None:
            return self._callback(results)

    def wait(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(self._master_task))
        return self._master_task.result()


class Worker(object):
    def __init__(self, func: Callable[..., Coroutine], *args, **kargs):
        self._func = func
        self._args = args
        self._kargs = kargs

    async def __call__(self):
        return await self._func(*self._args, **self._kargs)
