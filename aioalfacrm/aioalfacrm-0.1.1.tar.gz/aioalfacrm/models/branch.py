import typing

from .. import fields
from ..core import AlfaObject


class Branch(AlfaObject):
    id = fields.String()
    name = fields.String()
    is_active = fields.Bool()
    subject_ids = fields.ListField(base=fields.Integer())

    def __init__(
            self,
            id_: typing.Optional[int] = None,
            name: str = '',
            is_active: bool = True,
            subject_ids: typing.Optional[typing.List[int]] = None,
            **kwargs,
    ):
        if subject_ids is None:
            subject_ids = []
        super(Branch, self).__init__(id=id_, name=name, is_active=is_active, subject_ids=subject_ids, **kwargs)
