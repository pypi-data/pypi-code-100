import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.ats_type import AtsType
from ..models.mercury_assessment import MercuryAssessment
from ..models.mercury_assessment_order_metadata import MercuryAssessmentOrderMetadata
from ..models.mercury_candidate import MercuryCandidate
from ..models.mercury_report import MercuryReport
from ..models.mercury_result import MercuryResult
from ..models.pontem_order_statuses import PontemOrderStatuses
from ..types import UNSET, Unset

T = TypeVar("T", bound="MercuryAssessmentOrder")


@attr.s(auto_attribs=True)
class MercuryAssessmentOrder:
    """  """

    id: str
    invite_link: str
    status: PontemOrderStatuses
    create_date: datetime.datetime
    candidate: MercuryCandidate
    assessment_id: str
    assessment: MercuryAssessment
    application_id: str
    ats_type: AtsType
    requisition_id: Union[Unset, str] = UNSET
    requisition_title: Union[Unset, str] = UNSET
    metadata: Union[Unset, MercuryAssessmentOrderMetadata] = UNSET
    recruiter_report: Union[Unset, str] = UNSET
    results: Union[Unset, List[MercuryResult]] = UNSET
    reports: Union[Unset, List[MercuryReport]] = UNSET
    candidate_redirect_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        invite_link = self.invite_link
        status = self.status.value

        create_date = self.create_date.isoformat()

        candidate = self.candidate.to_dict()

        assessment_id = self.assessment_id
        assessment = self.assessment.to_dict()

        application_id = self.application_id
        ats_type = self.ats_type.value

        requisition_id = self.requisition_id
        requisition_title = self.requisition_title
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        recruiter_report = self.recruiter_report
        results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.results, Unset):
            results = []
            for results_item_data in self.results:
                results_item = results_item_data.to_dict()

                results.append(results_item)

        reports: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.reports, Unset):
            reports = []
            for reports_item_data in self.reports:
                reports_item = reports_item_data.to_dict()

                reports.append(reports_item)

        candidate_redirect_url = self.candidate_redirect_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "invite_link": invite_link,
                "status": status,
                "create_date": create_date,
                "candidate": candidate,
                "assessment_id": assessment_id,
                "assessment": assessment,
                "application_id": application_id,
                "ats_type": ats_type,
            }
        )
        if requisition_id is not UNSET:
            field_dict["requisition_id"] = requisition_id
        if requisition_title is not UNSET:
            field_dict["requisition_title"] = requisition_title
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if recruiter_report is not UNSET:
            field_dict["recruiter_report"] = recruiter_report
        if results is not UNSET:
            field_dict["results"] = results
        if reports is not UNSET:
            field_dict["reports"] = reports
        if candidate_redirect_url is not UNSET:
            field_dict["candidate_redirect_url"] = candidate_redirect_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        invite_link = d.pop("invite_link")

        status = PontemOrderStatuses(d.pop("status"))

        create_date = isoparse(d.pop("create_date"))

        candidate = MercuryCandidate.from_dict(d.pop("candidate"))

        assessment_id = d.pop("assessment_id")

        assessment = MercuryAssessment.from_dict(d.pop("assessment"))

        application_id = d.pop("application_id")

        ats_type = AtsType(d.pop("ats_type"))

        requisition_id = d.pop("requisition_id", UNSET)

        requisition_title = d.pop("requisition_title", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MercuryAssessmentOrderMetadata]
        if isinstance(_metadata, Unset) or _metadata is None:
            metadata = UNSET
        else:
            metadata = MercuryAssessmentOrderMetadata.from_dict(_metadata)

        recruiter_report = d.pop("recruiter_report", UNSET)

        results = []
        _results = d.pop("results", UNSET)
        for results_item_data in _results or []:
            results_item = MercuryResult.from_dict(results_item_data)

            results.append(results_item)

        reports = []
        _reports = d.pop("reports", UNSET)
        for reports_item_data in _reports or []:
            reports_item = MercuryReport.from_dict(reports_item_data)

            reports.append(reports_item)

        candidate_redirect_url = d.pop("candidate_redirect_url", UNSET)

        mercury_assessment_order = cls(
            id=id,
            invite_link=invite_link,
            status=status,
            create_date=create_date,
            candidate=candidate,
            assessment_id=assessment_id,
            assessment=assessment,
            application_id=application_id,
            ats_type=ats_type,
            requisition_id=requisition_id,
            requisition_title=requisition_title,
            metadata=metadata,
            recruiter_report=recruiter_report,
            results=results,
            reports=reports,
            candidate_redirect_url=candidate_redirect_url,
        )

        mercury_assessment_order.additional_properties = d
        return mercury_assessment_order

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
