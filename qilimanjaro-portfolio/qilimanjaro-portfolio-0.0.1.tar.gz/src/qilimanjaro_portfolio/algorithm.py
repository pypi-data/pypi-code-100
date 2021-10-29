# algorithm.py
from dataclasses import dataclass

from qilimanjaroq_client.typings.algorithm import AlgorithmDefinition


@dataclass
class Algorithm:

    @property
    def definition(self) -> AlgorithmDefinition:
        pass
