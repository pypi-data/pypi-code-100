from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.get_object_list_response_200o_list_item_mp_list_item_m_list_item import (
    GetObjectListResponse200OListItemMpListItemMListItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetObjectListResponse200OListItemMpListItem")


@attr.s(auto_attribs=True)
class GetObjectListResponse200OListItemMpListItem:
    """ """

    mp_nr: Union[Unset, str] = UNSET
    m_list: Union[Unset, List[GetObjectListResponse200OListItemMpListItemMListItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mp_nr = self.mp_nr
        m_list: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.m_list, Unset):
            m_list = []
            for m_list_item_data in self.m_list:
                m_list_item = m_list_item_data.to_dict()

                m_list.append(m_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if mp_nr is not UNSET:
            field_dict["mpNr"] = mp_nr
        if m_list is not UNSET:
            field_dict["mList"] = m_list

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mp_nr = d.pop("mpNr", UNSET)

        m_list = []
        _m_list = d.pop("mList", UNSET)
        for m_list_item_data in _m_list or []:
            m_list_item = GetObjectListResponse200OListItemMpListItemMListItem.from_dict(m_list_item_data)

            m_list.append(m_list_item)

        get_object_list_response_200o_list_item_mp_list_item = cls(
            mp_nr=mp_nr,
            m_list=m_list,
        )

        get_object_list_response_200o_list_item_mp_list_item.additional_properties = d
        return get_object_list_response_200o_list_item_mp_list_item

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
