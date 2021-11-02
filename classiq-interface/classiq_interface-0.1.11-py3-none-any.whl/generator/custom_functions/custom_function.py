from enum import Enum
from typing import Optional, Set

import pydantic

from classiq_interface.generator.custom_functions.custom_function_library_data import (
    CustomFunctionLibraryData,
)
from classiq_interface.generator.function_params import FunctionParams


class CustomFunction(FunctionParams):
    """
    A user-defined custom function parameters object.
    """

    name: str = pydantic.Field(description="The name of a custom function")

    def _generate_io_enums(self):
        self._input_enum = Enum(
            f"_input_enum of {self.name}",
            {name: name for name in self._input_names},
        )
        self._output_enum = Enum(
            f"_output_enum of {self.name}",
            {name: name for name in self._output_names},
        )

    def generate_io_names(self, input_set: Set[str], output_set: Set[str]):
        self._input_names = list(input_set)
        self._output_names = list(output_set)
        self._generate_io_enums()

    def validate_custom_function_in_library(
        self,
        library: Optional[CustomFunctionLibraryData],
        error_handler: Exception = ValueError,
    ) -> None:
        if library is None or self.name not in library.custom_functions_dict:
            raise error_handler("The custom function is not found in included library.")
