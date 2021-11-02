# -*- coding: utf-8 -*-

import asyncio
import pytest
from google.protobuf.struct_pb2 import Struct
from google.protobuf.wrappers_pb2 import BytesValue

from patchwork.core import Task
from patchwork.core.client.local import AsyncLocalPublisher, AsyncLocalSubscriber


@pytest.fixture
def local_queue():
    return asyncio.Queue()


@pytest.mark.asyncio
async def test_send(local_queue):
    client = AsyncLocalPublisher(queue=local_queue)

    await client.send(b'payload', some_extra=1)

    assert local_queue.qsize() == 1, \
        "Sent message missing on the queue"

    payload = local_queue.get_nowait()
    task = Task()
    task.ParseFromString(payload)
    assert task.payload.TypeName() == 'google.protobuf.BytesValue'

    wrapper = BytesValue()
    task.payload.Unpack(wrapper)
    assert wrapper.value == b'payload'

    extra = Struct()
    task.meta.extra.Unpack(extra)
    assert extra['some_extra'] == 1


@pytest.mark.asyncio
async def test_send_payload(local_queue):
    client = AsyncLocalPublisher(queue=local_queue)

    await client._send(b'payload', Task())

    assert local_queue.qsize() == 1, \
        "Sent message missing on the queue"

    payload = local_queue.get_nowait()
    assert payload == b'payload'


@pytest.mark.asyncio
async def test_send_timeout():
    queue = asyncio.Queue(maxsize=1)
    # put something to fell the queue
    queue.put_nowait(None)

    client = AsyncLocalPublisher(queue=queue)

    with pytest.raises(TimeoutError):
        await client._send(b'payload', Task(), timeout=0.01)


@pytest.mark.asyncio
async def test_shared_default_queue():
    """
    Test if all local async client instances share the same default queue instance
    :return:
    """
    client_1 = AsyncLocalPublisher()
    client_2 = AsyncLocalSubscriber()

    await client_1._send(b'payload', Task())
    payload, meta = await client_2._fetch_one()

    assert payload == b'payload'
    assert meta == {}


@pytest.mark.asyncio
async def test_fetch_one(local_queue):
    local_queue.put_nowait(b'payload')

    client = AsyncLocalSubscriber(queue=local_queue)
    payload, meta = await client._fetch_one()

    assert payload == b'payload'
    assert meta == {}


@pytest.mark.asyncio
async def test_fetch_one_timeout(local_queue):

    client = AsyncLocalSubscriber(queue=local_queue)
    with pytest.raises(TimeoutError):
        _payload, _meta = await client._fetch_one(timeout=0.01)


@pytest.mark.asyncio
def test_queue_ref():
    queue = asyncio.Queue()
    client = AsyncLocalSubscriber(queue=queue)
    del queue

    with pytest.raises(ConnectionAbortedError):
        """
        Client should not own queue (in the same way as clients working with external brokers are not
        owning them and remote queue may disappear at any time.
        """
        _ = client.queue

