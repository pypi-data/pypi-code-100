from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.mercury_candidate import MercuryCandidate
from ..models.mercury_order_request_metadata import MercuryOrderRequestMetadata
from ..types import UNSET, Unset

T = TypeVar("T", bound="MercuryOrderRequest")


@attr.s(auto_attribs=True)
class MercuryOrderRequest:
    """  """

    candidate: MercuryCandidate
    assessment_id: str
    application_id: str
    send_email: Union[Unset, bool] = False
    requisition_id: Union[Unset, str] = UNSET
    requisition_title: Union[Unset, str] = UNSET
    metadata: Union[Unset, MercuryOrderRequestMetadata] = UNSET
    candidate_redirect_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        candidate = self.candidate.to_dict()

        assessment_id = self.assessment_id
        application_id = self.application_id
        send_email = self.send_email
        requisition_id = self.requisition_id
        requisition_title = self.requisition_title
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        candidate_redirect_url = self.candidate_redirect_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"candidate": candidate, "assessment_id": assessment_id, "application_id": application_id,}
        )
        if send_email is not UNSET:
            field_dict["send_email"] = send_email
        if requisition_id is not UNSET:
            field_dict["requisition_id"] = requisition_id
        if requisition_title is not UNSET:
            field_dict["requisition_title"] = requisition_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if candidate_redirect_url is not UNSET:
            field_dict["candidate_redirect_url"] = candidate_redirect_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        candidate = MercuryCandidate.from_dict(d.pop("candidate"))

        assessment_id = d.pop("assessment_id")

        application_id = d.pop("application_id")

        send_email = d.pop("send_email", UNSET)

        requisition_id = d.pop("requisition_id", UNSET)

        requisition_title = d.pop("requisition_title", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MercuryOrderRequestMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MercuryOrderRequestMetadata.from_dict(_metadata)

        candidate_redirect_url = d.pop("candidate_redirect_url", UNSET)

        mercury_order_request = cls(
            candidate=candidate,
            assessment_id=assessment_id,
            application_id=application_id,
            send_email=send_email,
            requisition_id=requisition_id,
            requisition_title=requisition_title,
            metadata=metadata,
            candidate_redirect_url=candidate_redirect_url,
        )

        mercury_order_request.additional_properties = d
        return mercury_order_request

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
