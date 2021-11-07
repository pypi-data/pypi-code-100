import typing

from ..core import BaseField


class Bool(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value

    def deserialzie(self, value: typing.Any) -> typing.Any:
        try:
            return bool(value)
        except ValueError:
            raise ValueError(f'{value} is not bool')
