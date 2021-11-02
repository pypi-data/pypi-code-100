import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

from ..models.get_object_list_response_200o_list_item import GetObjectListResponse200OListItem

T = TypeVar("T", bound="GetObjectListResponse200")


@attr.s(auto_attribs=True)
class GetObjectListResponse200:
    """ """

    s_date: datetime.datetime
    c_eic: str
    c_name: str
    o_list: List[GetObjectListResponse200OListItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        s_date = self.s_date.isoformat()

        c_eic = self.c_eic
        c_name = self.c_name
        o_list = []
        for o_list_item_data in self.o_list:
            o_list_item = o_list_item_data.to_dict()

            o_list.append(o_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sDate": s_date,
                "cEIC": c_eic,
                "cName": c_name,
                "oList": o_list,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        s_date = isoparse(d.pop("sDate"))

        c_eic = d.pop("cEIC")

        c_name = d.pop("cName")

        o_list = []
        _o_list = d.pop("oList")
        for o_list_item_data in _o_list:
            o_list_item = GetObjectListResponse200OListItem.from_dict(o_list_item_data)

            o_list.append(o_list_item)

        get_object_list_response_200 = cls(
            s_date=s_date,
            c_eic=c_eic,
            c_name=c_name,
            o_list=o_list,
        )

        get_object_list_response_200.additional_properties = d
        return get_object_list_response_200

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
