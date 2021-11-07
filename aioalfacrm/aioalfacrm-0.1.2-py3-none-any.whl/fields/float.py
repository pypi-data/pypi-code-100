import typing

from ..core import BaseField


class Float(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Any:
        try:
            value = float(value)
            return value
        except ValueError:
            raise ValueError('{value} is not float')
