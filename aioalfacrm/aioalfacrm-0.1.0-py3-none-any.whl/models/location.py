from typing import Optional

from .. import fields
from ..core import AlfaObject


class Location(AlfaObject):
    id = fields.Integer()
    branch_id = fields.Integer()
    is_active = fields.Integer()
    name = fields.String()
    weight = fields.Integer()

    def __init__(
            self,
            id_: Optional[int] = None,
            branch_id: Optional[int] = None,
            is_active: Optional[bool] = None,
            name: Optional[str] = None,
            **kwargs,
    ):
        super(Location, self).__init__(
            id=id_,
            branch_id=branch_id,
            is_active=is_active,
            name=name,
            **kwargs,
        )
