from enum import Enum
from typing import Generic, Literal, Optional, TypeVar, Union

import pydantic
from pydantic.generics import GenericModel

from classiq_interface.generator.arith.arithmetic import DEFAULT_OUT_NAME
from classiq_interface.generator.arith.fix_point_number import FixPointNumber
from classiq_interface.generator.arith.register_user_input import RegisterUserInput
from classiq_interface.generator.function_params import FunctionParams

DEFAULT_RIGHT_ARG_NAME = "right_arg"
DEFAULT_LEFT_ARG_NAME = "left_arg"
LeftDataT = TypeVar("LeftDataT")
RightDataT = TypeVar("RightDataT")
Numeric = (float, int)


class BinaryOpParams(GenericModel, FunctionParams, Generic[LeftDataT, RightDataT]):
    left_arg: LeftDataT
    right_arg: RightDataT
    output_size: Optional[pydantic.PositiveInt]
    output_name: str = DEFAULT_OUT_NAME

    @pydantic.validator("left_arg")
    def set_left_arg_name(cls, left_arg):
        if isinstance(left_arg, RegisterUserInput):
            left_arg.name = DEFAULT_LEFT_ARG_NAME
        return left_arg

    @pydantic.validator("right_arg")
    def set_right_arg_name(cls, right_arg):
        if isinstance(right_arg, RegisterUserInput):
            right_arg.name = DEFAULT_RIGHT_ARG_NAME
        return right_arg

    @pydantic.root_validator()
    def validate_one_is_register(cls, values):
        if isinstance(values.get("left_arg"), Numeric) and isinstance(
            values.get("right_arg"), Numeric
        ):
            raise ValueError("One argument must be a register")
        return values

    def create_io_enums(self):
        self._output_enum = Enum(
            "BinaryOpOutputs", {self.output_name: self.output_name}
        )

        if isinstance(self.left_arg, RegisterUserInput) and isinstance(
            self.right_arg, RegisterUserInput
        ):
            self._input_enum = Enum(
                "BinaryOpInputs",
                {
                    self.left_arg.name: self.left_arg.name,
                    self.right_arg.name: self.right_arg.name,
                },
            )
            return

        if isinstance(self.left_arg, RegisterUserInput):
            arg_name = self.left_arg.name
        else:
            assert isinstance(
                self.right_arg, RegisterUserInput
            ), "At least one argument should be a register"
            arg_name = self.right_arg.name

        self._input_enum = Enum("BinaryOpInputs", {arg_name: arg_name})

    class Config:
        arbitrary_types_allowed = True


class BinaryOpWithIntInputs(
    BinaryOpParams[Union[int, RegisterUserInput], Union[int, RegisterUserInput]]
):
    @pydantic.root_validator()
    def validate_int_registers(cls, values):
        left_arg = values.get("left_arg")
        is_left_arg_float_register = (
            isinstance(left_arg, RegisterUserInput) and left_arg.fraction_places > 0
        )
        right_arg = values.get("right_arg")
        is_right_arg_float_register = (
            isinstance(right_arg, RegisterUserInput) and right_arg.fraction_places > 0
        )
        if is_left_arg_float_register or is_right_arg_float_register:
            raise ValueError("Boolean operation are defined only for integer")

        return values


class BinaryOpWithFloatInputs(
    BinaryOpParams[
        Union[float, FixPointNumber, RegisterUserInput],
        Union[float, FixPointNumber, RegisterUserInput],
    ]
):
    @pydantic.validator("left_arg", "right_arg")
    def convert_numeric_to_fix_point_number(cls, val):
        if isinstance(val, Numeric):
            val = FixPointNumber(float_value=val)
        return val


class BitwiseAnd(BinaryOpWithIntInputs):
    pass


class BitwiseOr(BinaryOpWithIntInputs):
    pass


class BitwiseXor(BinaryOpWithIntInputs):
    pass


class Adder(BinaryOpWithFloatInputs):
    inplace: bool = True


class Subtractor(BinaryOpWithFloatInputs):
    inplace: bool = True


class Comparator(BinaryOpWithFloatInputs):
    output_size: Literal[1] = 1
    _include_equal: bool = pydantic.PrivateAttr(default=True)


class Equal(Comparator):
    pass


class NotEqual(Comparator):
    pass


class GreaterThan(Comparator):
    pass


class GreaterEqual(Comparator):
    pass


class LessThan(Comparator):
    pass


class LessEqual(Comparator):
    pass


class BinaryOpWithLeftRegRightInt(
    BinaryOpParams[RegisterUserInput, pydantic.PositiveInt]
):
    pass


class LShift(BinaryOpWithLeftRegRightInt):
    pass


class RShift(BinaryOpWithLeftRegRightInt):
    use_arithmetic_bit_shift: bool = True


class CyclicShift(BinaryOpParams[RegisterUserInput, int]):
    pass
