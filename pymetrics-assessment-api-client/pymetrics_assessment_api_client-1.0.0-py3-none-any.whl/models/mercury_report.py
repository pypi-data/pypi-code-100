import datetime
from typing import Any, Dict, List, Type, TypeVar

import attr
from dateutil.parser import isoparse

T = TypeVar("T", bound="MercuryReport")


@attr.s(auto_attribs=True)
class MercuryReport:
    """  """

    download_url: str
    create_date: datetime.datetime
    modify_date: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        download_url = self.download_url
        create_date = self.create_date.isoformat()

        modify_date = self.modify_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"download_url": download_url, "create_date": create_date, "modify_date": modify_date,}
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        download_url = d.pop("download_url")

        create_date = isoparse(d.pop("create_date"))

        modify_date = isoparse(d.pop("modify_date"))

        mercury_report = cls(download_url=download_url, create_date=create_date, modify_date=modify_date,)

        mercury_report.additional_properties = d
        return mercury_report

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
