import typing

from . import errors

class SentinelMeta(type):
    def __repr__(cls: type) -> str:
        return f'<{cls.__name__}>'

    def __new__(self, name: str, bases: typing.Tuple[type], attributes: typing.Dict[str, typing.Any]) -> object:
        cls: object = type.__new__(self, name, bases, attributes)

        def __init__(self, *args, **kwargs) -> None:
            raise errors.SentinelInitialisationError

        type.__setattr__(cls, __init__.__name__, __init__)

        return cls

    def __setattr__(self, name: str, value: typing.Any) -> None:
        raise errors.SentinelMutationError

class Sentinel(metaclass = SentinelMeta): pass
