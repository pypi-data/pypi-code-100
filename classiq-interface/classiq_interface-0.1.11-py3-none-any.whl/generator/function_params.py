import abc
from enum import Enum
from typing import Any, List, Optional, Type

import pydantic

DEFAULT_OUTPUT_NAME = "OUT"
DEFAULT_INPUT_NAME = "IN"


class DefaultInputEnum(Enum):
    pass


class DefaultOutputEnum(Enum):
    OUT = DEFAULT_OUTPUT_NAME


class IO(Enum):
    Input = "Input"
    Output = "Output"


class FunctionParams(pydantic.BaseModel, abc.ABC):
    _input_enum: Optional[Type[Enum]] = pydantic.PrivateAttr(default=None)
    _output_enum: Optional[Type[Enum]] = pydantic.PrivateAttr(default=None)

    _input_names: List[str] = pydantic.PrivateAttr(default_factory=list)
    _output_names: List[str] = pydantic.PrivateAttr(default=[DEFAULT_OUTPUT_NAME])

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.create_io_enums()
        self._create_io_names()

    def get_io_enum(self, io: IO) -> Type[Enum]:
        if io == IO.Input:
            return self._input_enum
        if io == IO.Output:
            return self._output_enum

    def get_io_names(self, io: IO) -> List[str]:
        if io == IO.Input:
            return self._input_names
        if io == IO.Output:
            return self._output_names

        raise AssertionError("Unsupported IO type")

    def create_io_enums(self):
        pass

    def _create_io_names(self):
        if self._input_enum is None and self._output_enum is None:
            return

        self._input_names = list(self._input_enum.__members__.keys())
        self._output_names = list(self._output_enum.__members__.keys())

    def is_valid_io_name(self, name: str, io: IO) -> bool:
        return name in self.get_io_names(io)
