from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.update_time_series_request_values import UpdateTimeSeriesRequestValues
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateTimeSeriesRequest")


@attr.s(auto_attribs=True)
class UpdateTimeSeriesRequest:
    """ """

    time_series_id: Union[Unset, str] = UNSET
    values: Union[Unset, None, UpdateTimeSeriesRequestValues] = UNSET
    warnings: Union[Unset, None, List[str]] = UNSET
    unit: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        time_series_id = self.time_series_id
        values: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values.to_dict() if self.values else None

        warnings: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.warnings, Unset):
            if self.warnings is None:
                warnings = None
            else:
                warnings = self.warnings

        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if time_series_id is not UNSET:
            field_dict["timeSeriesId"] = time_series_id
        if values is not UNSET:
            field_dict["values"] = values
        if warnings is not UNSET:
            field_dict["warnings"] = warnings
        if unit is not UNSET:
            field_dict["unit"] = unit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        time_series_id = d.pop("timeSeriesId", UNSET)

        _values = d.pop("values", UNSET)
        values: Union[Unset, None, UpdateTimeSeriesRequestValues]
        if _values is None:
            values = None
        elif isinstance(_values, Unset):
            values = UNSET
        else:
            values = UpdateTimeSeriesRequestValues.from_dict(_values)

        warnings = cast(List[str], d.pop("warnings", UNSET))

        unit = d.pop("unit", UNSET)

        update_time_series_request = cls(
            time_series_id=time_series_id,
            values=values,
            warnings=warnings,
            unit=unit,
        )

        return update_time_series_request
