from typing import Dict
from dataclasses import dataclass, field
from mitre_attack import MARKING_DEFINITION
from mitre_attack.data.types.object import Object


@dataclass(frozen=True)
class MarkingDefinition(Object):
    type: str = field(default=MARKING_DEFINITION, init=False)
    definition: Dict[str, str]
    definition_type: str

    def is_statement(self):
        return self.definition_type == "statement"
