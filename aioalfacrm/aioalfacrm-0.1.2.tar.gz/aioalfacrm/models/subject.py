from typing import Optional

from .. import fields
from ..core import AlfaObject


class Subject(AlfaObject):
    id: Optional[int] = fields.Integer()
    name: Optional[str] = fields.String()

    def __init__(
            self,
            id_: Optional[int] = None,
            name: Optional[str] = None,
            **kwargs,
    ):
        super(Subject, self).__init__(
            id=id_,
            name=name,
            **kwargs,
        )
