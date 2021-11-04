from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MercuryListOrdersRequest")


@attr.s(auto_attribs=True)
class MercuryListOrdersRequest:
    """  """

    job_application_id: Union[Unset, str] = UNSET
    candidate_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_application_id = self.job_application_id
        candidate_id = self.candidate_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_application_id is not UNSET:
            field_dict["job_application_id"] = job_application_id
        if candidate_id is not UNSET:
            field_dict["candidate_id"] = candidate_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_application_id = d.pop("job_application_id", UNSET)

        candidate_id = d.pop("candidate_id", UNSET)

        mercury_list_orders_request = cls(job_application_id=job_application_id, candidate_id=candidate_id,)

        mercury_list_orders_request.additional_properties = d
        return mercury_list_orders_request

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
