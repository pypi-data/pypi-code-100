from dataclasses import dataclass, field
from mitre_attack import TOOL
from mitre_attack.data.types.software import Software


@dataclass(frozen=True)
class Tool(Software):
    type: str = field(init=False, default=TOOL)

