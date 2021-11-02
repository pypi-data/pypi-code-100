from typing import Tuple

import pydantic

QubitsType: type = Tuple[pydantic.NonNegativeInt, ...]


class CustomRegister(pydantic.BaseModel):
    """
    A user-defined custom register.
    """

    name: pydantic.constr(min_length=1) = pydantic.Field(
        description="The name of the custom register",
    )

    qubits: QubitsType = pydantic.Field(
        description="A tuple of qubits as integers as indexed within a custom function code",
    )

    @property
    def width(self) -> pydantic.PositiveInt:
        """The number of qubits of the custom register"""
        return len(self.qubits)

    @pydantic.validator("qubits")
    def validate_qubits(cls, qubits: QubitsType):
        if len(qubits) == 0:
            raise ValueError("qubits field must be non-empty.")
        if len(set(qubits)) != len(qubits):
            raise ValueError("All qubits of a register must be distinct.")
        return qubits
