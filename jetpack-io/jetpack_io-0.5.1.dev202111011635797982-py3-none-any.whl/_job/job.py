from __future__ import annotations

import asyncio
import base64
import inspect
import os
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Union, ValuesView

from jetpack import utils
from jetpack._job.client import Client
from jetpack._remote import codec
from jetpack.proto.runtime.v1alpha1 import remote_pb2

client = Client()


def get_client() -> Client:
    return client


class AlreadyExistsError(Exception):
    pass


class Job:
    # Question: do we need a separate Dict for blocking jobs?
    jobs: Dict[str, Job] = {}

    def __init__(self, func: Callable[..., Any]) -> None:
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> Union[Any, Awaitable[Any]]:
        """
        No return value for now, but eventually this will return a handle
        or an awaitable
        """
        if inspect.iscoroutinefunction(self.func):
            return client.launch_async_job(self.name(), args, kwargs)
        else:
            return client.launch_job(self.name(), args, kwargs)

    def fire_and_forget(
        self, *args: Any, **kwargs: Any
    ) -> Union[remote_pb2.LaunchJobResponse, Awaitable[remote_pb2.LaunchJobResponse]]:
        if inspect.iscoroutinefunction(self.func):
            return client.launch_fire_and_forget_async_job(self.name(), args, kwargs)
        else:
            return client.launch_fire_and_forget_job(self.name(), args, kwargs)

    def name(self) -> str:
        return utils.qualified_func_name(self.func)

    def exec(self, exec_id: str, base64_encoded_args: str = "") -> None:

        args: Tuple[Any, ...] = ()
        kwargs: Dict[str, Any] = {}
        if base64_encoded_args:
            encoded_args = base64.b64decode(base64_encoded_args).decode("utf-8")
            decoded_args, decoded_kwargs = codec.decode_args(encoded_args)
            if decoded_args:
                args = decoded_args
            if decoded_kwargs:
                kwargs = decoded_kwargs

        retval, err = None, None
        try:
            if inspect.iscoroutinefunction(self.func):
                retval = asyncio.run(self.func(*args, **kwargs))
            else:
                retval = self.func(*args, **kwargs)
        except Exception as e:
            err = e

        # for now, we post the result back to the remotesvc. A slightly better approach is to
        # have the caller of this function post it (the CLI). Doing it here for now because
        # the remotesvc is already initialized and set up here.
        client.post_result(exec_id, value=retval, error=err)
