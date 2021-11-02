import pydantic

from classiq_interface.generator.circuit_outline import Cycle, Qubit


class Measurement(pydantic.BaseModel):
    qubit: Qubit
    cycle: Cycle
