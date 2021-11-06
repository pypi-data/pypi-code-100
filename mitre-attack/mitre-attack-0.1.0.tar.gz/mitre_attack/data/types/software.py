from dataclasses import dataclass, field
from mitre_attack import MALWARE, TOOL
from mitre_attack.data.types.object import Object
from typing import List, Union


@dataclass(frozen=True)
class Software(Object):
    name: str
    old_attack_id: Union[str, None] = None
    aliases: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    contributors: List[str] = field(default_factory=list)
    platforms: List[str] = field(default_factory=list)

    def is_malware(self):
        return MALWARE in self.labels

    def is_tool(self):
        return TOOL in self.labels
