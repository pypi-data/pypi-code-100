import asyncio
from typing import List, Optional

from pyomo.core import ConcreteModel

from classiq_interface import status
from classiq_interface.backend.backend_preferences import (
    BackendPreferences,
    IBMBackendPreferences,
)
from classiq_interface.chemistry import operator
from classiq_interface.combinatorial_optimization import (
    model_serializer,
    optimization_problem,
    sense,
)
from classiq_interface.executor.result import ExecutionData, ExecutionStatus
from classiq_interface.generator import result as generator_result
from classiq_interface.generator.result import GeneratedCircuit
from classiq_interface.hybrid import vqe_problem

from classiq import api_wrapper
from classiq.exceptions import (
    ClassiqError,
    ClassiqExecutionError,
    ClassiqGenerationError,
)


class CombinatorialOptimization:
    def __init__(
        self,
        model: ConcreteModel,
        vqe_preferences: Optional[vqe_problem.VQEPreferences] = None,
        backend_preferences: Optional[BackendPreferences] = None,
    ):
        if vqe_preferences is None:
            vqe_preferences = vqe_problem.VQEPreferences()
        if backend_preferences is None:
            backend_preferences = IBMBackendPreferences(
                backend_service_provider="IBMQ", backend_name="aer_simulator"
            )

        self.is_maximization = sense.is_maximization(model)
        self._serialized_model = model_serializer.to_json(model, return_dict=True)
        self._problem = optimization_problem.OptimizationProblem(
            serialized_model=self._serialized_model,
            vqe_preferences=vqe_preferences,
            backend_preferences=backend_preferences,
        )

    def generate(self) -> GeneratedCircuit:
        return asyncio.run(self.generate_async())

    async def generate_async(self) -> GeneratedCircuit:
        """Async version of `generate`"""
        wrapper = api_wrapper.ApiWrapper()
        result = await wrapper.call_combinatorial_optimization_generate_task(
            problem=self._problem
        )

        if result.status != generator_result.GenerationStatus.SUCCESS:
            raise ClassiqGenerationError(f"Solving failed: {result.details}")

        return result.details

    def solve(self) -> ExecutionData:
        return asyncio.run(self.solve_async())

    async def solve_async(self) -> ExecutionData:
        """Async version of `solve`"""
        wrapper = api_wrapper.ApiWrapper()
        result = await wrapper.call_combinatorial_optimization_solve_task(
            problem=self._problem
        )

        if result.status != ExecutionStatus.SUCCESS:
            raise ClassiqExecutionError(f"Solving failed: {result.details}")

        return result.details

    def get_operator(self) -> operator.OperatorResult:
        return asyncio.run(self.get_operator_async())

    async def get_operator_async(self) -> operator.PauliOperator:
        """Async version of `get_operator`"""
        wrapper = api_wrapper.ApiWrapper()
        result = await wrapper.call_combinatorial_optimization_operator_task(
            problem=self._problem
        )

        if result.status != operator.OperatorStatus.SUCCESS:
            raise ClassiqError(f"Get operator failed: {result.details}")

        return result.details

    def get_initial_point(self) -> List[float]:
        return asyncio.run(self.get_initial_point_async())

    async def get_initial_point_async(self) -> List[float]:
        """Async version of `get_initial_point`"""
        wrapper = api_wrapper.ApiWrapper()
        result = await wrapper.call_combinatorial_optimization_initial_point_task(
            problem=self._problem
        )

        if result.status != status.Status.SUCCESS:
            raise ClassiqError(f"Get inital point failed: {result.details}")

        return result.details
