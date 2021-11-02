from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.get_object_consumption_response_200_item_m_list_item_c_list_item import (
    GetObjectConsumptionResponse200ItemMListItemCListItem,
)

T = TypeVar("T", bound="GetObjectConsumptionResponse200ItemMListItem")


@attr.s(auto_attribs=True)
class GetObjectConsumptionResponse200ItemMListItem:
    """ """

    m_nr: str
    c_list: List[GetObjectConsumptionResponse200ItemMListItemCListItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        m_nr = self.m_nr
        c_list = []
        for c_list_item_data in self.c_list:
            c_list_item = c_list_item_data.to_dict()

            c_list.append(c_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mNr": m_nr,
                "cList": c_list,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        m_nr = d.pop("mNr")

        c_list = []
        _c_list = d.pop("cList")
        for c_list_item_data in _c_list:
            c_list_item = GetObjectConsumptionResponse200ItemMListItemCListItem.from_dict(c_list_item_data)

            c_list.append(c_list_item)

        get_object_consumption_response_200_item_m_list_item = cls(
            m_nr=m_nr,
            c_list=c_list,
        )

        get_object_consumption_response_200_item_m_list_item.additional_properties = d
        return get_object_consumption_response_200_item_m_list_item

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
