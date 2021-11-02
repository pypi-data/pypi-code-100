import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.get_object_consumption_response_200_item_m_list_item_c_list_item_cvr_st import (
    GetObjectConsumptionResponse200ItemMListItemCListItemCVRSt,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetObjectConsumptionResponse200ItemMListItemCListItem")


@attr.s(auto_attribs=True)
class GetObjectConsumptionResponse200ItemMListItemCListItem:
    """ """

    c_dt: datetime.datetime
    c_vr: float
    c_vr_st: Union[Unset, GetObjectConsumptionResponse200ItemMListItemCListItemCVRSt] = UNSET
    c_vv: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        c_dt = self.c_dt.isoformat()

        c_vr = self.c_vr
        c_vr_st: Union[Unset, str] = UNSET
        if not isinstance(self.c_vr_st, Unset):
            c_vr_st = self.c_vr_st.value

        c_vv = self.c_vv

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cDt": c_dt,
                "cVR": c_vr,
            }
        )
        if c_vr_st is not UNSET:
            field_dict["cVRSt"] = c_vr_st
        if c_vv is not UNSET:
            field_dict["cVV"] = c_vv

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        c_dt = isoparse(d.pop("cDt"))

        c_vr = d.pop("cVR")

        _c_vr_st = d.pop("cVRSt", UNSET)
        c_vr_st: Union[Unset, GetObjectConsumptionResponse200ItemMListItemCListItemCVRSt]
        if isinstance(_c_vr_st, Unset):
            c_vr_st = UNSET
        else:
            c_vr_st = GetObjectConsumptionResponse200ItemMListItemCListItemCVRSt(_c_vr_st)

        c_vv = d.pop("cVV", UNSET)

        get_object_consumption_response_200_item_m_list_item_c_list_item = cls(
            c_dt=c_dt,
            c_vr=c_vr,
            c_vr_st=c_vr_st,
            c_vv=c_vv,
        )

        get_object_consumption_response_200_item_m_list_item_c_list_item.additional_properties = d
        return get_object_consumption_response_200_item_m_list_item_c_list_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
