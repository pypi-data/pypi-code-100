import typing

from ..core import BaseField


class ListField(BaseField):

    def __init__(self, *args, **kwargs):
        default = kwargs.pop('default', None)
        if default is None:
            default = []

        super(ListField, self).__init__(*args, default=default, **kwargs)

    def serialize(self, value: typing.List[typing.Any]) -> typing.Any:
        serialize = self.base_field.serialize
        return [serialize(item) for item in value]

    def deserialzie(self, value: typing.Any) -> typing.Optional[typing.List[typing.Any]]:
        if value is None:
            return None
        deserialize = self.base_field.deserialzie
        return [deserialize(item) for item in value]
