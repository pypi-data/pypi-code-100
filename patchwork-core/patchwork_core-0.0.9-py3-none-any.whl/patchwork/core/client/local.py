# -*- coding: utf-8 -*-

import asyncio
import weakref

from .base import SynchronousPublisher, SynchronousSubscriber, AsyncPublisher, AsyncSubscriber


class SyncLocalPublisher(SynchronousPublisher):
    """
    Patchwork is asynchronous framework with fully async nodes, so locally async Python must be supported
    to run the worker. Synchronous client make no sense in that case.
    """
    def __init__(self):
        raise NotImplementedError("There is no synchronous local client")


class SyncLocalSubscriber(SynchronousSubscriber):
    """
    Patchwork is asynchronous framework with fully async nodes, so locally async Python must be supported
    to run the worker. Synchronous client make no sense in that case.
    """
    def __init__(self):
        raise NotImplementedError("There is no synchronous local client")


class DummySerializer:

    @classmethod
    def dumps(cls, data):
        return data

    @classmethod
    def loads(cls, data):
        return data


class AsyncLocalPublisher(AsyncPublisher):
    """
    Simple patchwork client working on local event loop using given asyncio.Queue.

    !!! danger
        For development purposes only!
    """

    __queues = weakref.WeakKeyDictionary()

    def __init__(self, parent=None, queue: asyncio.Queue = None, **options):
        """
        :param queue:   asyncio queue to bind to
        """
        super().__init__(parent=parent, **options)
        if queue is None:
            queue = self.get_queue()

        self._queue = weakref.ref(queue)

    @classmethod
    def get_queue(cls):
        loop = asyncio.get_event_loop()
        if loop not in cls.__queues:
            cls.__queues[loop] = asyncio.Queue()

        return cls.__queues[loop]

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]}, queue={self.queue}]>"

    @property
    def queue(self) -> asyncio.Queue:
        queue = self._queue()
        if queue is None:
            raise ConnectionAbortedError("Local queue lost")

        return queue

    async def _setup(self):
        self.logger.debug(f"Publisher attached to local queue {self.queue}")

    async def _teardown(self):
        self.logger.debug(f"Publisher left local queue {self.queue.qsize()}")

    async def _send(self, payload, task, timeout: float = None):
        try:
            if timeout == 0:
                self.queue.put_nowait(payload)
            else:
                await asyncio.wait_for(self.queue.put(payload), timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"send operation timeout, can't deliver in {timeout}s")


class AsyncLocalSubscriber(AsyncSubscriber):

    def __init__(self, parent=None, queue: asyncio.Queue = None, **options):
        """
        :param queue:   asyncio queue to bind to
        """
        self._queue = weakref.ref(queue or AsyncLocalPublisher.get_queue())
        super().__init__(parent=parent, **options)
        self._uncommitted = set()

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]}, queue={self.queue}]>"

    @property
    def queue(self) -> asyncio.Queue:
        queue = self._queue()
        if queue is None:
            raise ConnectionAbortedError("Local queue lost")

        return queue

    async def _setup(self):
        self.logger.debug(f"Subscriber attached to local queue {self.queue}")

    async def _teardown(self):
        self.logger.debug(f"Subscriber stopped with {self.queue.qsize()} messages left on the queue")

    async def _fetch_one(self, timeout: float = None):
        try:
            return await asyncio.wait_for(self.queue.get(), timeout=timeout), {}
        except asyncio.TimeoutError:
            raise TimeoutError(f"fetch operation timeout, no messages in {timeout}s")

    async def commit(self, task, *, timeout: float = None):
        self._uncommitted.remove(task.uuid)

    async def get(self, *, timeout: float = None):
        task = await super().get(timeout=timeout)
        self._uncommitted.add(task.uuid)
        self.queue.task_done()
        return task
