import typing

from ..core import BaseField


class Bool(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Any:
        if value is None:
            return None
        return bool(value)
