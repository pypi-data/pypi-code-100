from typing import Optional

from .. import fields
from ..core import AlfaObject


class StudyStatus(AlfaObject):
    id = fields.Integer()
    name = fields.String()
    is_enabled = fields.Integer()

    def __init__(
            self,
            id_: Optional[int] = None,
            name: Optional[str] = None,
            is_enabled: Optional[bool] = None,
            **kwargs,
    ):
        super(StudyStatus, self).__init__(
            id=id_,
            name=name,
            is_enabled=is_enabled,
            **kwargs,
        )
