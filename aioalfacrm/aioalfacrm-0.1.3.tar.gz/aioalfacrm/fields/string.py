import typing

from ..core import BaseField


class String(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Any:
        if value is None:
            return value

        value = str(value)
        return value
