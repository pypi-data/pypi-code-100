from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MercuryCandidate")


@attr.s(auto_attribs=True)
class MercuryCandidate:
    """  """

    email: str
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    external_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        external_id = self.external_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"email": email,}
        )
        if first_name is not UNSET:
            field_dict["first_name"] = first_name
        if last_name is not UNSET:
            field_dict["last_name"] = last_name
        if external_id is not UNSET:
            field_dict["external_id"] = external_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        first_name = d.pop("first_name", UNSET)

        last_name = d.pop("last_name", UNSET)

        external_id = d.pop("external_id", UNSET)

        mercury_candidate = cls(email=email, first_name=first_name, last_name=last_name, external_id=external_id,)

        mercury_candidate.additional_properties = d
        return mercury_candidate

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
