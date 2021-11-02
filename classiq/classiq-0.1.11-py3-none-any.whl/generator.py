"""Generator module, implementing facilities for generating circuits using Classiq platform."""
import asyncio
import functools
from typing import Dict, Optional

from classiq_interface.generator import (
    constraints,
    function_call,
    function_param_list,
    function_params,
    result,
)
from classiq_interface.generator.custom_functions.custom_function import CustomFunction

from classiq import api_wrapper, wire
from classiq.custom_function_library import CustomFunctionLibrary
from classiq.exceptions import ClassiqGenerationError, ClassiqValueError

# TODO: Add docstrings for auto generated methods.


class Generator:
    """Facility to generate circuits, based on the model."""

    def __init__(self, qubit_count: int, max_depth: int, **kwargs) -> None:
        """Init self with qubit count and maximal depth.

        Args:
            qubit_count (): The number of qubits in the generated circuit.
            max_depth (): The maximum depth of the generated circuit.
        """
        self._constraints = constraints.QuantumCircuitConstraints(
            qubit_count=qubit_count, max_depth=max_depth, **kwargs
        )

    def generate(self) -> result.GeneratedCircuit:
        """Generates a circuit, based on the aggregation of requirements in self.

        Returns:
            The results of the generation procedure.
        """
        return asyncio.run(self.generate_async())

    async def generate_async(self) -> result.GeneratedCircuit:
        """Async version of `generate`
        Generates a circuit, based on the aggregation of requirements in self.

        Returns:
            The results of the generation procedure.
        """
        # TODO: There something distorted with regards to the singleton and the configuration. Also, the need to pass
        #       conf here and not in init is weird.
        wrapper = api_wrapper.ApiWrapper()
        generation_result = await wrapper.call_generation_task(self._constraints)

        if generation_result.status != result.GenerationStatus.SUCCESS:
            raise ClassiqGenerationError(
                f"Generation failed: {generation_result.details}"
            )

        return generation_result.details

    @property
    def constraints(self) -> constraints.QuantumCircuitConstraints:
        """Get the constraints aggregated in self.

        Returns:
            The constraints data.
        """
        return self._constraints

    def _add_function_call(
        self,
        function: str,
        params: function_params.FunctionParams,
        in_wires: Optional[Dict[str, wire.Wire]] = None,
    ) -> Dict[str, wire.Wire]:
        if function != type(params).__name__:
            raise ClassiqValueError(
                "The FunctionParams type does not match function name"
            )
        if isinstance(params, CustomFunction):
            params.validate_custom_function_in_library(
                library=self._constraints.custom_function_library_data,
                error_handler=ClassiqValueError,
            )

        call = function_call.FunctionCall(function=function, function_params=params)

        if in_wires:
            for input_name, in_wire in in_wires.items():
                in_wire.connect_wire(end_call=call, input_name=input_name)

        self._constraints.logic_flow.append(call)

        return {
            output_name: wire.Wire(start_call=call, output_name=output_name)
            for output_name in params.get_io_names(function_params.IO.Output)
        }

    def include_library(self, library: CustomFunctionLibrary) -> None:
        """Includes a user-defined custom function library.

        Args:
            library (CustomFunctionLibrary): The custom function library.
        """
        if self._constraints.custom_function_library_data is not None:
            raise ClassiqValueError(
                "Another custom function library is already included."
            )
        self._constraints.custom_function_library_data = library.data

    def __getattribute__(self, item):
        is_item_function_name = any(
            item == func.__name__
            for func in function_param_list.get_function_param_list()
        )

        if is_item_function_name:
            return functools.partial(self._add_function_call, function=item)

        return super().__getattribute__(item)

    def __dir__(self):
        return list(super().__dir__()) + [
            func.__name__ for func in function_param_list.get_function_param_list()
        ]
