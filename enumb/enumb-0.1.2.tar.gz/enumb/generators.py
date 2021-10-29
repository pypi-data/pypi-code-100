import functools
import typing

import export

from . import models
from . import types

@export
def generate_next_value(func: typing.Callable[[models.Arguments], typing.Any]) -> types.EnumValueGenerator:
    @functools.wraps(func)
    def wrapper(name: str, start: int, count: int, last_values: typing.List[typing.Any]) -> typing.Any:
        return func \
        (
            models.Arguments \
            (
                name        = name,
                start       = start,
                count       = count,
                last_values = last_values,
            ),
        )

    return wrapper

@export
@generate_next_value
def name(arguments: models.Arguments) -> str:
    return arguments.name

@export
@generate_next_value
def count(arguments: models.Arguments) -> int:
    return arguments.count
