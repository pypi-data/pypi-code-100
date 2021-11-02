import pydantic

from classiq_interface.generator.circuit_outline import Clbit, Cycle, Qubit


class Cif(pydantic.BaseModel):
    qubit: Qubit
    cycle: Cycle
    clbit: Clbit
    clvalue: bool
