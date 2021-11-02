from typing import Set, Tuple, Union

import pydantic

from classiq_interface.generator.custom_functions.custom_function_implementation import (
    CustomFunctionImplementation,
)

ImplementationsType: type = Union[
    Tuple[CustomFunctionImplementation, ...], CustomFunctionImplementation
]


class CustomFunctionData(pydantic.BaseModel):
    """
    Facilitates the creation of a user-defined custom function
    """

    name: pydantic.constr(
        strict=True, regex=r"^([a-z][a-z0-9]*)(_[a-z0-9]+)*\Z"  # noqa: F722
    ) = pydantic.Field(description="The name of a custom function")

    implementations: ImplementationsType = pydantic.Field(
        description="The implementations of the custom function",
    )

    @property
    def input_set(self) -> Set[str]:
        return set(
            register.name for register in self.implementations[0].input_registers
        )

    @property
    def output_set(self) -> Set[str]:
        return set(
            register.name for register in self.implementations[0].output_registers
        )

    @pydantic.validator("implementations")
    def validate_implementations(cls, implementations: ImplementationsType):
        if not implementations:
            raise ValueError(
                "The implementations of a custom function must be non-empty."
            )
        if isinstance(implementations, CustomFunctionImplementation):
            implementations = (implementations,)

        distinct_io_signatures = set(
            tuple(
                tuple(sorted((register.name, register.width) for register in registers))
                for registers in (
                    implementation.input_registers,
                    implementation.output_registers,
                )
            )
            for implementation in implementations
        )
        if len(distinct_io_signatures) != 1:
            raise ValueError(
                "All implementations of a custom function must have matching IO register names and widths."
            )
        return implementations
