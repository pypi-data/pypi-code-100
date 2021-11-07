import typing

from ..core import BaseField


class String(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Any:
        try:
            value = str(value)
            return value
        except ValueError:
            raise ValueError(f'{value} if not string')
