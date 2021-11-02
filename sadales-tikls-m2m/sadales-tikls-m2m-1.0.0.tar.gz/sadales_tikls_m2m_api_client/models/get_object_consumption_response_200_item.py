from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.get_object_consumption_response_200_item_m_list_item import GetObjectConsumptionResponse200ItemMListItem

T = TypeVar("T", bound="GetObjectConsumptionResponse200Item")


@attr.s(auto_attribs=True)
class GetObjectConsumptionResponse200Item:
    """ """

    mp_nr: str
    m_list: List[GetObjectConsumptionResponse200ItemMListItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mp_nr = self.mp_nr
        m_list = []
        for m_list_item_data in self.m_list:
            m_list_item = m_list_item_data.to_dict()

            m_list.append(m_list_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mpNr": mp_nr,
                "mList": m_list,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mp_nr = d.pop("mpNr")

        m_list = []
        _m_list = d.pop("mList")
        for m_list_item_data in _m_list:
            m_list_item = GetObjectConsumptionResponse200ItemMListItem.from_dict(m_list_item_data)

            m_list.append(m_list_item)

        get_object_consumption_response_200_item = cls(
            mp_nr=mp_nr,
            m_list=m_list,
        )

        get_object_consumption_response_200_item.additional_properties = d
        return get_object_consumption_response_200_item

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
