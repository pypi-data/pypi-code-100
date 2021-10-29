# bellstate.py
from dataclasses import dataclass
from qilimanjaroq_client.typings.algorithm import (AlgorithmDefinition,
                                                   AlgorithmName,
                                                   AlgorithmOptions,
                                                   AlgorithmType,
                                                   InitialValue)
from ..algorithm import Algorithm


@dataclass
class BellState(Algorithm):
    number_qubits: int
    initial_state: InitialValue

    @property
    def definition(self) -> AlgorithmDefinition:
        return AlgorithmDefinition(name=AlgorithmName.BELLSTATE,
                                   type=AlgorithmType.GATE_BASED,
                                   options=AlgorithmOptions(number_qubits=self.number_qubits,
                                                            initial_value=self.initial_state))
