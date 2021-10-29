import typing

from . import base

def is_sentinel(obj: typing.Any) -> bool:
    return type(obj) is base.SentinelMeta
