from dataclasses import dataclass, field
from mitre_attack import TACTIC
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class Tactic(Object):
    type: str = field(default=TACTIC, init=False)
    name: str
    shortname: str
