from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.mercury_assessment import MercuryAssessment

T = TypeVar("T", bound="MercuryConfiguration")


@attr.s(auto_attribs=True)
class MercuryConfiguration:
    """  """

    assessments: List[MercuryAssessment]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assessments = []
        for assessments_item_data in self.assessments:
            assessments_item = assessments_item_data.to_dict()

            assessments.append(assessments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"assessments": assessments,}
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assessments = []
        _assessments = d.pop("assessments")
        for assessments_item_data in _assessments:
            assessments_item = MercuryAssessment.from_dict(assessments_item_data)

            assessments.append(assessments_item)

        mercury_configuration = cls(assessments=assessments,)

        mercury_configuration.additional_properties = d
        return mercury_configuration

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
