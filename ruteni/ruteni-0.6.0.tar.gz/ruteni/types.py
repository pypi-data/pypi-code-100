import typing

from starlette.applications import Starlette

Callback = typing.Callable[[Starlette], typing.Awaitable[None]]


class Service(typing.NamedTuple):
    name: str
    startup: Callback
    shutdown: Callback
