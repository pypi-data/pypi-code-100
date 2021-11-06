from dataclasses import dataclass
from typing import List, Union
from mitre_attack.data.types.external_reference import ExternalReference

import hodgepodge.types
import datetime


@dataclass(frozen=True)
class Object:
    id: str
    type: str
    created: datetime.datetime
    created_by_ref: Union[str, None]
    modified: datetime.datetime
    description: str
    external_references: List[ExternalReference]
    object_marking_refs: List[str]
    version: str

    @property
    def created_at(self) -> datetime.datetime:
        return self.created

    @property
    def update_time(self) -> datetime.datetime:
        return self.modified

    @property
    def markings(self):
        return self.object_marking_refs

    def to_dict(self):
        return hodgepodge.types.dataclass_to_dict(data=self)

    def to_json(self):
        return hodgepodge.types.dict_to_json(self.to_dict())

