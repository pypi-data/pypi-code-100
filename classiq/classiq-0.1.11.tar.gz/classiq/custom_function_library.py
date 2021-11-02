"""Custom function library module, implementing facilities for adding user defined functions to the Classiq platform."""

from typing import Dict, Tuple

from classiq_interface.generator.custom_functions.custom_function import CustomFunction
from classiq_interface.generator.custom_functions.custom_function_data import (
    CustomFunctionData,
)
from classiq_interface.generator.custom_functions.custom_function_library_data import (
    DEFAULT_CUSTOM_FUNCTION_LIBRARY_NAME,
    CustomFunctionLibraryData,
)

from classiq.exceptions import ClassiqValueError


class CustomFunctionLibrary:
    """Facility to manage user-defined custom functions."""

    def __init__(self, name: str = DEFAULT_CUSTOM_FUNCTION_LIBRARY_NAME):
        """
        Args:
            name (:obj:`str`, optional): The name of the custom function library.
        """
        self._data = CustomFunctionLibraryData(name=name)
        self._params: Dict[str, CustomFunction] = dict()

    def get_function(self, function_name: str) -> CustomFunction:
        """Gets a function from the function library.

        Args:
            function_name (str): The name of the custom function.

        Returns:
            The custom function parameters.
        """
        return self._params[function_name]

    def add_function(
        self,
        function_data: CustomFunctionData,
        override_existing_custom_functions: bool = False,
    ) -> CustomFunction:
        """Adds a function to the function library.

        Args:
            function_data (CustomFunctionData): The custom function data object.
            override_existing_custom_functions (:obj:`bool`, optional): Defaults to False.

        Returns:
            The custom function parameters.
        """

        function_name = function_data.name
        if (
            not override_existing_custom_functions
            and function_name in self._data.custom_functions_dict
        ):
            raise ClassiqValueError("Cannot override existing custom functions.")
        self._data.custom_functions_dict[function_name] = function_data
        self._params[function_name] = self._to_params(function_data)
        return self.get_function(function_name=function_name)

    def remove_function(self, function_name: str) -> CustomFunctionData:
        """Removes a function from the function library.

        Args:
            function_name (str): The name of the custom function.

        Returns:
            The removed custom function data.
        """
        self._params.pop(function_name)
        return self._data.custom_functions_dict.pop(function_name)

    @property
    def name(self) -> str:
        """The library name."""
        return self._data.name

    @property
    def function_names(self) -> Tuple[str, ...]:
        """Get a tuple of the names of the custom functions in the library.

        Returns:
            The names of the custom functions in the library.
        """
        return tuple(self._data.custom_functions_dict.keys())

    @property
    def data(self) -> CustomFunctionLibraryData:
        return self._data

    @staticmethod
    def _to_params(data: CustomFunctionData) -> CustomFunction:
        params = CustomFunction(name=data.name)
        params.generate_io_names(
            input_set=data.input_set,
            output_set=data.output_set,
        )
        return params
