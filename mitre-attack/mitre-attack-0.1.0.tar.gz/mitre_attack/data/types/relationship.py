from dataclasses import dataclass, field
from mitre_attack import RELATIONSHIP
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class Relationship(Object):
    type: str = field(default=RELATIONSHIP, init=False)
    source_ref: str
    source_ref_type: str
    target_ref: str
    target_ref_type: str
    relationship_type: str
