from dataclasses import dataclass, field
from typing import List
from mitre_attack import MATRIX
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class Matrix(Object):
    type: str = field(init=False, default=MATRIX)
    name: str
    tactic_refs: List[str]
