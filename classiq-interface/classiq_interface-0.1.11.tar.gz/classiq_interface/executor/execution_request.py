from typing import Dict, Optional

import pydantic

from classiq_interface.backend.backend_preferences import IonqBackendPreferences
from classiq_interface.executor.execution_preferences import ExecutionPreferences
from classiq_interface.executor.hamiltonian_minimization_problem import (
    HamiltonianMinimizationProblem,
)
from classiq_interface.executor.quantum_program import (
    QuantumInstructionSet,
    QuantumProgram,
)
from classiq_interface.generator.generation_metadata import GenerationMetadata


class ExecutionRequest(pydantic.BaseModel):
    generation_data: Optional[GenerationMetadata] = pydantic.Field(
        default=None, description="Data returned from the generation procedure."
    )
    quantum_program: Optional[QuantumProgram] = pydantic.Field(
        default=None,
        description="A quantum program to execute.",
    )
    hamiltonian_minimization_problem: Optional[
        HamiltonianMinimizationProblem
    ] = pydantic.Field(
        default=None,
        description="A hamiltonian minimization problem, including ansatz and hamiltonian to minimize",
    )
    preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences,
        description="preferences for the execution",
    )

    @pydantic.root_validator()
    def validate_mutual_exclusive_fields(cls, values: Dict) -> Dict:
        MUTUALLY_EXCLUSIVE_FIELDS_LIST = [
            "generation_data",
            "quantum_program",
            "hamiltonian_minimization_problem",
        ]
        is_valid = False
        for field in MUTUALLY_EXCLUSIVE_FIELDS_LIST:
            if values.get(field) is not None:
                if is_valid:
                    is_valid = False
                    break
                is_valid = True

        if not is_valid:
            raise ValueError(
                "Exactly one field can be defined out of: "
                "quantum_program, generation_data, hamiltonian_minimization_problem"
            )

        return values

    @pydantic.validator("preferences")
    def validate_ionq_backend(cls, preferences: ExecutionPreferences, values: Dict):
        quantum_program: QuantumProgram = values.get("quantum_program")
        if (
            isinstance(preferences.backend_preferences, IonqBackendPreferences)
            and quantum_program is None
        ):
            raise ValueError("IonQ backend supports only execution of QuantumPrograms")
        if (
            not isinstance(preferences.backend_preferences, IonqBackendPreferences)
            and quantum_program is not None
            and quantum_program.syntax == QuantumInstructionSet.IONQ
        ):
            raise ValueError("Can only execute IonQ code on IonQ backend.")

        return preferences
