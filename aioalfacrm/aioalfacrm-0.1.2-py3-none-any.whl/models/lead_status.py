from typing import Optional

from .. import fields
from ..core import AlfaObject


class LeadStatus(AlfaObject):
    id: Optional[int] = fields.Integer()
    name: Optional[str] = fields.String()
    is_enabled: Optional[bool] = fields.Bool()

    def __init__(
            self,
            id_: Optional[int] = None,
            name: Optional[str] = None,
            is_enabled: Optional[bool] = None,
            **kwargs,
    ):
        super(LeadStatus, self).__init__(
            id=id_,
            name=name,
            is_enabled=is_enabled,
            **kwargs,
        )
