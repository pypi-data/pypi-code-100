import enum
from typing import List

import pydantic

from classiq_interface.generator.complex_type import Complex


class PauliOperator(pydantic.BaseModel):
    pauli_str: str
    pauli_str_rounded: str
    table: List[List[bool]]
    coeffs: List[Complex]

    def show(self) -> str:
        return self.pauli_str


class OperatorStatus(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class OperatorResult(pydantic.BaseModel):
    status: OperatorStatus
    details: PauliOperator
