from typing import Any, TYPE_CHECKING

from totype.annotation_types import RowT

if TYPE_CHECKING:
    from totype.fields import Field


class TransformError(ValueError):
    def __init__(self, field: "Field", value: Any, *args):
        self.field = field
        self.value = value
        super().__init__(*args)


class ValidationError(ValueError):
    def __init__(self, row: RowT, *args):
        self.row = row
        super().__init__(*args)
