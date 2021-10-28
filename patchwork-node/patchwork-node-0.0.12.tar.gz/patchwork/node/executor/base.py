# -*- coding: utf-8 -*-

import asyncio
import logging
from datetime import datetime
from functools import partial
from typing import MutableMapping, List, Union, Coroutine, Type

from patchwork.core import Task, AsyncSubscriber
from patchwork.core.config.base import ComponentConfig
from patchwork.core.utils import cached_property
from patchwork.node.core import Module
from patchwork.node.core.exceptions import TaskControlException, TaskRetry, TaskFatal, TaskDrop
from patchwork.node.core.router import TaskRouter
from patchwork.node.executor.unit import InlineUnit
from patchwork.node.executor.unit.base import ProcessingUnit


class BaseExecutor(Module):
    """
    Executor is responsible of taking tasks from supported queue, spawn and manage workers
    to run these tasks and implement ability to send new tasks to the queue though clients.
    """

    class Config(Module.Config):

        # executor termination timeout in seconds
        terminate_timeout: int = 10
        unit: ComponentConfig[Type[ProcessingUnit]] = ComponentConfig(InlineUnit)

    logger_name = 'executor'
    _loop_task: asyncio.Future
    _routers: List[TaskRouter]
    _unit_monitor_task: asyncio.Future

    def __init__(self, *, parent, **options):
        super().__init__(parent=parent, **options)

        self._terminate_request = asyncio.Event()
        self._current_tasks = set()
        self._routers = []

    def __repr__(self):
        res = super().__repr__()
        return f"<{res[1:-1]} [subscribers={'|'.join(self.settings.listen_on)} " \
               f"unit={self.unit.__class__.__name__}]>"

    def get_state(self) -> MutableMapping:
        return {
            'worker': self.unit.get_state(),
            'current_tasks': len(self._current_tasks)
        }

    @cached_property
    def unit(self) -> ProcessingUnit:
        return self.settings.unit.instantiate(parent=self)

    def add_router(self, router: TaskRouter):
        router.bind(self.worker)
        self._routers.append(router)

    async def _start(self):
        """
        Setups executor
        :return:
        """

        # clear terminate request flag
        self._terminate_request.clear()

        # start processing unit
        await self.unit.run()

        self._unit_monitor_task = asyncio.create_task(self._unit_monitor())

        # put executor loop task on event loop
        self._loop_task = asyncio.ensure_future(self._loop(), loop=self.app_loop)
        self._loop_task.add_done_callback(self._loop_completed_callback)

    async def _unit_monitor(self):
        try:
            await self.unit.state.wait_for(False)
        except asyncio.CancelledError:
            return

        self.logger.error(f"Executor processing unit unexpectedly terminated. Executor can't continue")

        self.harakiri()

    def _loop_completed_callback(self, fut: asyncio.Future):

        if fut.cancelled():
            # loop should never be cancelled
            raise AssertionError("DO NOT CANCEL executor loop! Set termination_request event instead to make"
                                 "sure that loop is stopped cleanly and no message was lost")

        exc = fut.exception()
        if exc:
            self.logger.error(f"Executor loop completed with exception: {exc.__class__.__name__}({exc})")
            self.harakiri()

    async def _stop(self):
        """
        Stops executor and all running tasks, when method returns event loop can be stopped
        :return:
        """

        # set terminate request flag
        self._terminate_request.set()
        self.logger.debug(f"Executor termination requested, "
                          f"waiting {self.settings.terminate_timeout}s to complete...")

        # wait for termination
        done, pending = await asyncio.wait([self._loop_task], timeout=self.settings.terminate_timeout)

        if pending:
            self.logger.warning("Loop task termination timeout, cancelling")

            # this raises CancelledError in loop task, there is no way to predict where exactly in code
            # it happens
            self._loop_task.cancel()

            # timeout to be safe
            done, pending = await asyncio.wait([self._loop_task], timeout=self.settings.terminate_timeout)

            if pending:
                self.logger.error("Unable to terminate executor main loop")

        # stop processing unit, executor loop is stopped so no more task may come,
        # drop what unit has queued and what is currently processing
        # there should be no more job to do about tasks, commit() method has been not
        # called so tasks assigned to the processing unit should be not lost
        try:
            await asyncio.wait_for(self.unit.busy.wait_for(False), timeout=self.settings.terminate_timeout)
        except asyncio.TimeoutError:
            self.logger.warning(f"Processing unit is still busy, timeout elapsed")

        self._unit_monitor_task.cancel()
        await self.unit.terminate()

        # wait for tasks callbacks to complete (commit, retry..., the last job is removing task from the
        # _current_tasks set)
        if self._current_tasks:
            await asyncio.wait(self._current_tasks)

    async def _loop(self):
        """
        This is an executor main loop task. Waits on all listen_on subscribers simultaneously for
        incoming task.
        DO NOT CANCEL THIS CORO as it can break flow in a way which may leads to message lost.
        Set self._termination_request event to request the loop termination.
        :return:
        """
        # future of termination request
        term_future = asyncio.create_task(self._terminate_request.wait())
        subscriber = self.worker.get_subscriber()

        while True:

            try:
                done, pending = await asyncio.wait((asyncio.create_task(subscriber.get()), term_future,),
                                                   return_when=asyncio.FIRST_COMPLETED)
            except Exception as e:
                self.logger.error(f"Client get() raises exception: {e.__class__.__name__}({e})",
                                  exc_info=True)
            else:
                for task in done:
                    if task == term_future:
                        # termination future done, even if there is more done futures skip them
                        # worker is going down
                        for fut in pending:
                            fut.cancel()
                        return

                    await self._handle_done_waiter(task, subscriber)

    async def _handle_done_waiter(self, future: asyncio.Future, receiver: AsyncSubscriber) -> bool:
        """
        Handles done waiter future of the client
        :param future:
        :param receiver:
        :return: True if loop should still listen on this client, False otherwise
        """

        if future.cancelled():
            # ygm? maybe something else disabled this client... do not put it back
            self.logger.info(f"Waiter of client {receiver} cancelled")
            await receiver.terminate()
            return False

        exc = future.exception()
        if exc:
            self.logger.error(f"Client {receiver} waiter completed with exception: "
                              f"{exc.__class__.__name__}({exc})")
            return True

        task: Task = future.result()
        self.logger.debug(f"Client {receiver} waiter returned a task message: {task.uuid}")

        try:
            await self.handle(task, receiver)
        except Exception as e:
            # log error and rollback task if something went wrong during internal scheduling
            self.logger.error(f"Unable to handle task '{task.uuid}', exception raised: {e.__class__.__name__}({e})")
            try:
                await self.retry(task, receiver)
            except Exception as e:
                self.logger.error(f"Unable to retry unhandled task '{task}', "
                                  f"exception raised: {e.__class__.__name__}({e})")
                await self.backoff_task(task, reason="Internal retry failed")

        return True

    async def retry(self, task: Task, receiver: AsyncSubscriber = None, *, countdown: float = None,
                    not_before: datetime = None, bump_attempts: bool = True) -> Union[Task, None]:
        """
        Retries given task by cloning it and sending back to originating client saved in 'receiver' task argument.
        If receiver is unknown task is send through default client using `send_task` method. When new task
        is delivered to the queue old one is committed.
        :param task:
        :param receiver:
        :param countdown:
        :param not_before:
        :param bump_attempts:
        :return:
        """
        new_task = Task()
        new_task.CopyFrom(task)
        new_task.uuid = ''

        if bump_attempts:
            new_task.meta.attempt += 1
            if new_task.meta.attempt > new_task.meta.max_retries:
                await self.backoff_task(task, reason="Max number of retries exceeded")
                return

        if countdown is not None:
            assert not_before is None, "both `countdown` and `not_before` arguments cannot be set at the same time"

            not_before = datetime.utcnow().timestamp() + countdown

        if not_before is not None:
            new_task.meta.not_before.FromDatetime(not_before)

        await self.worker.get_publisher('default').send_task(new_task)

        await self._commit_task(task, receiver)
        return new_task

    async def backoff_task(self, task, reason: str = None):
        """
        Stores given task on backoff queue. If task cannot be executed for some reason (eg retries limit exceeded)
        can be logged and saved in special place for future investigation. This method allows to notify administrator
        that something has been not executed and should be manually verified.

        In base implementation this method just logs task using 'backoff' standard python logger and passes
        task in `extra` argument, which means that in basic configuration task contents might be lost.
        :param task:
        :param reason:
        :return:
        """
        backoff_log = logging.getLogger('backoff')
        backoff_log.log(logging.NOTSET,
                        f"Task '{task.uuid}' backoffed.{(' Reason: ' + reason) if reason is not None else ''}",
                        extra={'task': task})
        self.logger.debug(f"Task '{task.uuid}' backoffed.{(' Reason: ' + reason) if reason is not None else ''}")

    async def handle(self, task: Task, receiver: AsyncSubscriber) -> Union[asyncio.Future, None]:
        """
        Executes given task, handles all exceptions which may rise during task
        processing.

        :: warning:
            This method may raise exception if task scheduling fail.

        :: note:
            This method awaits only for task scheduling, not task execution itself. When returns task
            is internally scheduled on processing unit. If you need task execution result await on returned
            future.

        :param task:
        :param receiver:
        :return: future of task processing function or None if processing was not scheduled because of
                 task control exception
        """

        try:
            for router in self._routers:
                processor = router.handle(task, receiver)
                if processor is not None:
                    task_future = await self._execute(task, receiver, processor)
                    self._current_tasks.add(task_future)
                    return task_future

            self.logger.error(f"No processor to handle message type '{task.task_type}'")
            raise TaskFatal(task, reason="No processor to handle this message type")

        except TaskControlException as exc:
            # allow _execute to raise task control exceptions
            await self._handle_task_control(task, receiver, exc)
            return None

    async def _execute(self, task: Task, receiver: AsyncSubscriber, processor: Coroutine):
        """
        Executes a task on given processor
        :param task:
        :param receiver:
        :param processor:
        :return:
        """
        # verify if task is still valid
        self.check_task(task)

        # await for submit which may hold if processing unit is full
        fut: asyncio.Future = await self.unit.submit(processor)
        fut.add_done_callback(partial(self._task_done_callback, receiver=receiver, task=task))

        return fut

    def check_task(self, task: Task):
        """
        Validates if given task is still valid and should be executed
        :param task:
        :return:
        """
        now = datetime.utcnow().timestamp()
        if task.meta.HasField('expires') and now > task.meta.expires.ToSeconds():
            # task has expired
            self.logger.debug(f"Task '{task.uuid}' is not valid after: {task.meta.expires}, now: {now}")
            raise TaskFatal(task, reason="Task has expired")
        elif task.meta.HasField('not_before') and now < task.meta.not_before.ToSeconds():
            # task is not ready yet
            self.logger.debug(f"Task '{task.uuid}' is not valid before: {task.meta.not_before}, now: {now}")
            raise TaskRetry(task, countdown=(now-task.meta.not_before))

    def _task_done_callback(self, fut: asyncio.Future, receiver: AsyncSubscriber, task: Task):
        """
        Handles value returned by task processing future.
        :param task:
        :param receiver:
        :param fut:
        :return:
        """
        def _callback(f: asyncio.Future):
            self._current_tasks.remove(fut)
            if f.cancelled():
                # task has been cancelled
                return

            exc = f.exception()
            if exc is not None:
                self.logger.fatal(f"Can't handle task result: {exc.__class__.__name__}({exc})")
                self.harakiri()

        handle_fut = self.app_loop.create_task(self._handle_task_result(task, receiver, fut))
        handle_fut.add_done_callback(_callback)

    async def _handle_task_result(self, task: Task, receiver: AsyncSubscriber, task_fut: asyncio.Future):
        """
        Handles task future result.
        :param task:
        :param receiver:
        :param task_fut:
        :return:
        """
        exc = task_fut.exception()
        if task_fut.cancelled():
            self.logger.debug(f"Task '{task}' execution cancelled internally")
            await self.retry(task, receiver)
        elif exc is not None:
            if isinstance(exc, TaskControlException):
                await self._handle_task_control(task, receiver, exc)
            else:
                self.logger.warning(f"Task '{task}' execution failed with exception {exc.__class__.__name__}({exc})")
                await self.retry(task, receiver)
        else:
            await self._commit_task(task, receiver)

    async def _handle_task_control(self, task: Task, receiver: AsyncSubscriber, exc: TaskControlException):
        """
        Takes appropriate action for the task depending on given task control exception.
        This method commits task.
        :param task:
        :param receiver:
        :param exc:
        :return:
        """
        if isinstance(exc, TaskRetry):
            # schedule new task
            await self.retry(task, receiver, not_before=exc.not_before)
        elif isinstance(exc, TaskFatal):
            await self.backoff_task(task, reason=(exc.reason or "Task processing fatal error"))
            # backoff just logs task, commit it to truly remove from the queue
            await self._commit_task(task, receiver)
        elif isinstance(exc, TaskDrop):
            await self._commit_task(task, receiver)
        else:
            self.logger.error(f"Unsupported task control exception '{exc.__class__.__name__}({exc})'")
            raise ValueError(f"Unsupported task control exception: '{exc.__class__.__name__}({exc})'") from exc

    async def _commit_task(self, task: Task, receiver: AsyncSubscriber):
        """
        Commits the task on the underlying queue.
        :param task:
        :return:
        """
        await receiver.commit(task)

    def harakiri(self):
        """
        Stops executor immediately due to critical internal error.
        Call this method if something went so wrong that there is no better way than killing this executor
        which cause clients disconnection from message broker and leaving uncommitted all tasks which
        are in progress or pending. Broker should consider this worker as dead and stop delivering new messages.
        :return:
        """
        self.logger.error("Executor harakiri requested")
        self.app_loop.create_task(self.terminate())
