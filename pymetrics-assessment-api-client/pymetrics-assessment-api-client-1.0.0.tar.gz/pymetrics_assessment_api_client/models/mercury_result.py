import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.mercury_assessment import MercuryAssessment
from ..types import UNSET, Unset

T = TypeVar("T", bound="MercuryResult")


@attr.s(auto_attribs=True)
class MercuryResult:
    """  """

    assessment: MercuryAssessment
    create_date: datetime.datetime
    description: Union[Unset, str] = UNSET
    score: Union[Unset, float] = UNSET
    band: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        assessment = self.assessment.to_dict()

        create_date = self.create_date.isoformat()

        description = self.description
        score = self.score
        band = self.band

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"assessment": assessment, "create_date": create_date,}
        )
        if description is not UNSET:
            field_dict["description"] = description
        if score is not UNSET:
            field_dict["score"] = score
        if band is not UNSET:
            field_dict["band"] = band

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assessment = MercuryAssessment.from_dict(d.pop("assessment"))

        create_date = isoparse(d.pop("create_date"))

        description = d.pop("description", UNSET)

        score = d.pop("score", UNSET)

        band = d.pop("band", UNSET)

        mercury_result = cls(
            assessment=assessment, create_date=create_date, description=description, score=score, band=band,
        )

        mercury_result.additional_properties = d
        return mercury_result

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
