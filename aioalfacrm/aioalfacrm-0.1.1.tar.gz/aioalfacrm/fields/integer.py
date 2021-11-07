import typing

from ..core import BaseField


class Integer(BaseField):

    def serialize(self, value: typing.Any) -> typing.Any:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Any:
        if value is None:
            return value
        try:
            value = int(value)
            return value
        except ValueError:
            raise ValueError(f'{value} is not integer')
