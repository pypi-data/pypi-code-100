# program.py
from dataclasses import dataclass
from typing import Any, List
from qilimanjaroq_client.api import API as QilimanjaroApi
from qilimanjaroq_client.typings.algorithm import ProgramDefinition
from .algorithm import Algorithm


@dataclass
class Program:
    api: QilimanjaroApi
    algorithms: List[Algorithm]

    def execute(self) -> Any:
        return self.api.execute(program=ProgramDefinition(
            algorithms=[algorithm.definition for algorithm in self.algorithms]))
