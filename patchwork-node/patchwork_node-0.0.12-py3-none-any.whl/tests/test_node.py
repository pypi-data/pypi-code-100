# -*- coding: utf-8 -*-
import asyncio

import pytest as pytest

from patchwork.core import Task
from patchwork.node import PatchworkWorker
from patchwork.node.core.router import TaskRouter


@pytest.fixture
async def worker():
    worker = PatchworkWorker()
    await worker.run()
    yield worker

    await worker.terminate()


@pytest.mark.asyncio
async def test_simple_use(worker):

    caught_tasks = []

    router = TaskRouter()

    @router.on('test-msg')
    async def processor(task: Task):
        caught_tasks.append(task)

    worker.include_router(router)
    await worker.get_publisher().send_task(Task(task_type='test-msg'))

    # wait until executor processing unit becomes busy which means given message has been consumed
    await asyncio.wait_for(worker.executor.unit.busy.wait(), timeout=1)

    assert len(caught_tasks) == 1
