from dataclasses import dataclass, field
from typing import List
from mitre_attack import DATA_SOURCE
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class DataSource(Object):
    type: field(init=False, default=DATA_SOURCE)
    name: str
    platforms: List[str]
    collection_layers: List[str]
    contributors: List[str]
