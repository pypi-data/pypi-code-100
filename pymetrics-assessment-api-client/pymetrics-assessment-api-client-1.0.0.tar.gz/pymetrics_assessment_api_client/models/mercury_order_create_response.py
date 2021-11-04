from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.mercury_assessment_order import MercuryAssessmentOrder

T = TypeVar("T", bound="MercuryOrderCreateResponse")


@attr.s(auto_attribs=True)
class MercuryOrderCreateResponse:
    """  """

    order: MercuryAssessmentOrder
    created: bool
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        order = self.order.to_dict()

        created = self.created

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"order": order, "created": created,}
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        order = MercuryAssessmentOrder.from_dict(d.pop("order"))

        created = d.pop("created")

        mercury_order_create_response = cls(order=order, created=created,)

        mercury_order_create_response.additional_properties = d
        return mercury_order_create_response

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
