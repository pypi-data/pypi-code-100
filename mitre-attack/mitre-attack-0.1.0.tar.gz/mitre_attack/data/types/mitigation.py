from dataclasses import dataclass, field
from typing import Union
from mitre_attack import COURSE_OF_ACTION
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class Mitigation(Object):
    type: str = field(default=COURSE_OF_ACTION, init=False)
    name: str
    old_attack_id: Union[str, None] = None
