from collections import namedtuple
from typing import Any, List, Dict

from totype.annotation_types import RowT, RowNum
from totype.exceptions import ValidationError
from totype.fields import Field


class RowTransform:
    def __init__(
        self,
        fields: List[Field],
        skip_error_rows: bool = False,
        store_rows_with_errors: bool = False,
    ):
        self.fields = fields
        self.store_rows_with_errors = store_rows_with_errors
        self.skip_error_rows = skip_error_rows

        self._rows_with_errors: Dict[RowNum, RowT] = {}
        self._iter = 0

    @property
    def rows_with_errors(self) -> Dict[RowNum, RowT]:
        if not self.skip_error_rows:
            raise AttributeError(
                "To collect errors enable the 'skip_error_rows' parameter"
            )
        return self._rows_with_errors

    @property
    def field_names(self) -> List[str]:
        names = []
        for f in self.fields:
            if f.name is None:
                raise ValueError("'None' value for 'name' field is not allowed")
            if f.name in names:
                raise ValueError("Fields must have unique names")
            names.append(f.name)

        return names

    def valid(self, row: RowT):
        if len(self.fields) != len(row) and isinstance(row, (tuple, list)):
            if self.skip_error_rows:
                if self.store_rows_with_errors:
                    self._rows_with_errors[self._iter] = row
            else:
                raise ValidationError(
                    row,
                    "The number of values in a row is not equal to the number of fields",
                )

    def _value_processing(self, row: RowT, field: Field, *, value: Any):
        valid, value = field(value)
        if self.skip_error_rows and not valid:
            if self.store_rows_with_errors:
                self._rows_with_errors[self._iter] = row

        return value

    def _row_processing(self, row: RowT) -> RowT:
        if isinstance(row, dict):
            for field in self.fields:
                value = row[field.name] if field.name in row else None
                row[field.name] = self._value_processing(row, field, value=value)

        elif isinstance(row, list):
            for i, field in enumerate(self.fields):
                row[i] = self._value_processing(row, field, value=row[i])

        elif isinstance(row, tuple):
            row = tuple(
                self._value_processing(row, field, value=v)
                for field, v in zip(self.fields, row)
            )

        return row

    def __call__(self, row: RowT) -> RowT:
        self.valid(row)
        row = self._row_processing(row)

        self._iter += 1

        return row

    def as_dict(self, row: RowT) -> dict:
        if isinstance(row, (tuple, list)):
            row = dict(zip(self.field_names, row))

        return row

    @classmethod
    def as_tuple(cls, row: RowT) -> tuple:
        if isinstance(row, dict):
            return tuple(row.values())

        return tuple(row)

    @classmethod
    def as_list(cls, row: RowT) -> list:
        if isinstance(row, dict):
            return list(row.values())

        return list(row)

    def as_namedtuple(self, row: RowT) -> namedtuple:
        if isinstance(row, dict):
            return namedtuple(f"Row{self._iter}", row)(**row)

        return namedtuple(f"Row{self._iter}", self.field_names)(*row)

    def __str__(self):
        text = "RowTransform(fields={}, skip_error_rows={}, store_rows_with_errors={})"
        return text.format(
            self.fields, self.skip_error_rows, self.store_rows_with_errors
        ).replace(" '\n ", " ")
