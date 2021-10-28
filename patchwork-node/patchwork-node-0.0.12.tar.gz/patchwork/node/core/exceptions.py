# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
from typing import Union


class TaskControlException(Exception):
    """
    Set of control exceptions raised by processors to notify executor.
    """
    def __init__(self, task):
        self.task = task


class TaskRetry(TaskControlException):
    """
    Requests task processing retry. Waits optional countdown seconds until next attempt.
    All processed data and stored outputs will be dropped. If retry attempts is reached
    task is backoffed.
    """

    def __init__(self, task, *, countdown: float = None, progress: Union[float, str, bytes] = None):
        super().__init__(task)
        if countdown is not None:
            self.not_before = datetime.utcnow() + timedelta(seconds=countdown)
        else:
            self.not_before = None

        self.progress = progress


class TaskFatal(TaskControlException):
    """
    Processor ends with fatal exception and task is unprocessable now and in the future.
    No retry, output dropped. Log task on backoff queue.
    """

    def __init__(self, task, *, reason: str = None):
        super().__init__(task)
        self.reason = reason


class TaskDrop(TaskControlException):
    """
    Drop this task without logging it on backoff queue.
    """
    pass
