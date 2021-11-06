from dataclasses import dataclass, field
from mitre_attack import DATA_COMPONENT
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class DataComponent(Object):
    type: field(init=False, default=DATA_COMPONENT)
    name: str
    data_source_ref: str
