from dataclasses import dataclass, field
from mitre_attack import IDENTITY
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class Identity(Object):
    type: str = field(init=False, default=IDENTITY)
    name: str
    identity_class: str
