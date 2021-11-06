from dataclasses import dataclass, field
from typing import List
from mitre_attack import INTRUSION_SET
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class Group(Object):
    type: str = field(default=INTRUSION_SET, init=False)
    name: str
    aliases: List[str] = field(default_factory=list)
    contributors: List[str] = field(default_factory=list)
