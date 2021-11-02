from typing import Dict

import pydantic

from classiq_interface.generator.custom_functions.custom_function_data import (
    CustomFunctionData,
)

DEFAULT_CUSTOM_FUNCTION_LIBRARY_NAME = "default_custom_function_library_name"


class CustomFunctionLibraryData(pydantic.BaseModel):
    """Facility to store user-defined custom functions."""

    name: pydantic.constr(
        strict=True, regex=r"^([a-z][a-z0-9]*)(_[a-z0-9]+)*\Z"  # noqa: F722
    ) = pydantic.Field(
        default=DEFAULT_CUSTOM_FUNCTION_LIBRARY_NAME,
        description="The name of the custom function library",
    )

    custom_functions_dict: Dict[str, CustomFunctionData] = pydantic.Field(
        default_factory=dict,
        description="A dictionary containing the custom functions in the library.",
    )
