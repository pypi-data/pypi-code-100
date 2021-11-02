"""Executor module, implementing facilities for executing quantum programs using Classiq platform."""
import asyncio
from typing import Union

import classiq_interface.executor.execution_preferences
from classiq_interface.executor import (
    execution_request,
    hamiltonian_minimization_problem,
    result as exc_result,
)
from classiq_interface.executor.result import (
    ExecutionDetails,
    FinanceSimulationResults,
    GroverSimulationResults,
)
from classiq_interface.generator import result as generation_result
from classiq_interface.hybrid.result import VQESolverResult

from classiq import api_wrapper
from classiq.exceptions import ClassiqExecutionError


class Executor:
    """Executor is the entry point for executing quantum programs on multiple quantum hardware vendors."""

    def __init__(
        self,
        preferences: classiq_interface.executor.execution_preferences.ExecutionPreferences,
    ) -> None:
        """Init self.

        Args:
            preferences (): Execution preferences, such as number of shots.
        """
        self._preferences = preferences
        self._api_wrapper = api_wrapper.ApiWrapper()

    def execute_quantum_program(
        self, quantum_program: classiq_interface.executor.quantum_program.QuantumProgram
    ) -> ExecutionDetails:
        return asyncio.run(self.execute_quantum_program_async(quantum_program))

    async def execute_quantum_program_async(
        self, quantum_program: classiq_interface.executor.quantum_program.QuantumProgram
    ) -> ExecutionDetails:
        """Async version of `execute_quantum_program`"""
        request = execution_request.ExecutionRequest(
            quantum_program=quantum_program, preferences=self._preferences
        )
        execution_result = await self._api_wrapper.call_execute_quantum_program_task(
            request=request
        )

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")

        return execution_result.details

    def execute_generated_circuit(
        self, generation_result: generation_result.GeneratedCircuit
    ) -> Union[FinanceSimulationResults, GroverSimulationResults]:
        return asyncio.run(self.execute_generated_circuit_async(generation_result))

    async def execute_generated_circuit_async(
        self, generation_result: generation_result.GeneratedCircuit
    ) -> Union[FinanceSimulationResults, GroverSimulationResults]:
        """Async version of `execute_generated_circuit`"""
        request = execution_request.ExecutionRequest(
            generation_data=generation_result.metadata, preferences=self._preferences
        )
        execution_result = await self._api_wrapper.call_execute_generated_circuit_task(
            request=request
        )

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")

        return execution_result.details

    def execute_hamiltonian_minimization(
        self,
        hamiltonian_minimization_problem: hamiltonian_minimization_problem.HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        return asyncio.run(
            self.execute_hamiltonian_minimization_async(
                hamiltonian_minimization_problem
            )
        )

    async def execute_hamiltonian_minimization_async(
        self,
        hamiltonian_minimization_problem: hamiltonian_minimization_problem.HamiltonianMinimizationProblem,
    ) -> VQESolverResult:
        """Async version of `execute_hamiltonian_minimization`"""
        request = execution_request.ExecutionRequest(
            hamiltonian_minimization_problem=hamiltonian_minimization_problem,
            preferences=self._preferences,
        )
        execution_result = (
            await self._api_wrapper.call_execute_hamiltonian_minimization(
                request=request
            )
        )

        if execution_result.status != exc_result.ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Execution failed: {execution_result.details}")

        return execution_result.details
