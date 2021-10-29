import types
import typing

class Namespace(types.SimpleNamespace):
    def __setitem__(self, key: str, value: typing.Any) -> None:
        setattr(self, key, value)

    def __call__(self, entity: typing.Union[types.FunctionType, typing.Type]) -> None:
        self[entity.__name__] = entity

def new() -> Namespace:
    return Namespace()
