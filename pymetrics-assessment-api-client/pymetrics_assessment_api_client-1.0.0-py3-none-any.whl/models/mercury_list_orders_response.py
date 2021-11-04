from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.mercury_assessment_order import MercuryAssessmentOrder

T = TypeVar("T", bound="MercuryListOrdersResponse")


@attr.s(auto_attribs=True)
class MercuryListOrdersResponse:
    """  """

    orders: List[MercuryAssessmentOrder]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        orders = []
        for orders_item_data in self.orders:
            orders_item = orders_item_data.to_dict()

            orders.append(orders_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"orders": orders,}
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        orders = []
        _orders = d.pop("orders")
        for orders_item_data in _orders:
            orders_item = MercuryAssessmentOrder.from_dict(orders_item_data)

            orders.append(orders_item)

        mercury_list_orders_response = cls(orders=orders,)

        mercury_list_orders_response.additional_properties = d
        return mercury_list_orders_response

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
