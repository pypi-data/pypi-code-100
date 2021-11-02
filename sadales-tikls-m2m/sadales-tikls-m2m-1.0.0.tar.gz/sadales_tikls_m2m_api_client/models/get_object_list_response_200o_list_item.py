import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.get_object_list_response_200o_list_item_mp_list_item import GetObjectListResponse200OListItemMpListItem
from ..models.get_object_list_response_200o_list_item_o_addr import GetObjectListResponse200OListItemOAddr
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetObjectListResponse200OListItem")


@attr.s(auto_attribs=True)
class GetObjectListResponse200OListItem:
    """ """

    o_eic: str
    o_name: str
    o_status: str
    o_addr: GetObjectListResponse200OListItemOAddr
    mp_list: List[GetObjectListResponse200OListItemMpListItem]
    o_date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        o_eic = self.o_eic
        o_name = self.o_name
        o_status = self.o_status
        o_addr = self.o_addr.to_dict()

        mp_list = []
        for mp_list_item_data in self.mp_list:
            mp_list_item = mp_list_item_data.to_dict()

            mp_list.append(mp_list_item)

        o_date: Union[Unset, str] = UNSET
        if not isinstance(self.o_date, Unset):
            o_date = self.o_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "oEIC": o_eic,
                "oName": o_name,
                "oStatus": o_status,
                "oAddr": o_addr,
                "mpList": mp_list,
            }
        )
        if o_date is not UNSET:
            field_dict["oDate"] = o_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        o_eic = d.pop("oEIC")

        o_name = d.pop("oName")

        o_status = d.pop("oStatus")

        o_addr = GetObjectListResponse200OListItemOAddr.from_dict(d.pop("oAddr"))

        mp_list = []
        _mp_list = d.pop("mpList")
        for mp_list_item_data in _mp_list:
            mp_list_item = GetObjectListResponse200OListItemMpListItem.from_dict(mp_list_item_data)

            mp_list.append(mp_list_item)

        _o_date = d.pop("oDate", UNSET)
        o_date: Union[Unset, datetime.datetime]
        if isinstance(_o_date, Unset):
            o_date = UNSET
        else:
            o_date = isoparse(_o_date)

        get_object_list_response_200o_list_item = cls(
            o_eic=o_eic,
            o_name=o_name,
            o_status=o_status,
            o_addr=o_addr,
            mp_list=mp_list,
            o_date=o_date,
        )

        get_object_list_response_200o_list_item.additional_properties = d
        return get_object_list_response_200o_list_item

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
