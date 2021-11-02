import pydantic

from classiq_interface.chemistry.ground_state_problem import GroundStateProblem
from classiq_interface.executor.execution_preferences import ExecutionPreferences
from classiq_interface.generator.constraints import QuantumCircuitConstraints


class GroundStateProblemExecution(pydantic.BaseModel):
    molecule: GroundStateProblem
    quantum_circuit_constraints: QuantumCircuitConstraints
    preferences: ExecutionPreferences
