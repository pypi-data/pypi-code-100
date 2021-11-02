import ast
import enum
import keyword
import random
import re
from enum import Enum
from typing import Dict, Optional, Union

import pydantic

from classiq_interface.generator.arith.fix_point_number import (
    MAX_FRACTION_PLACES,
    FixPointNumber,
)
from classiq_interface.generator.arith.register_user_input import RegisterUserInput
from classiq_interface.generator.function_params import FunctionParams

DEFAULT_OUT_NAME = "out"
DEFAULT_ARG_NAME = "in_arg"

SUPPORTED_FUNC_NAMES = ("CLShift", "CRShift")

white_list = {"or", "and"}.union(SUPPORTED_FUNC_NAMES)
black_list = set(keyword.kwlist) - white_list


class MappingMethods(str, enum.Enum):
    topological = "topological"
    pebble = "pebble"


class Arithmetic(FunctionParams):
    max_fraction_places: pydantic.conint(ge=0) = MAX_FRACTION_PLACES
    expression: str
    definitions: Dict[
        str,
        Union[
            pydantic.StrictInt, pydantic.StrictFloat, FixPointNumber, RegisterUserInput
        ],
    ]
    method: MappingMethods = MappingMethods.pebble
    qubit_count: Optional[pydantic.conint(ge=0)] = None
    output_name: Optional[str]
    random_seed: Optional[int] = None

    @pydantic.validator("expression")
    def check_expression_is_legal(cls, expression):
        ast.parse(expression, "", "eval")
        return expression

    @pydantic.root_validator()
    def check_all_variable_are_defined(cls, values):
        expression, definitions = values.get("expression"), values.get("definitions")

        literals = set(re.findall("[A-Za-z][A-Za-z0-9]*", expression))

        not_allowed = literals.intersection(black_list)
        undefined_literals = literals.difference(definitions, white_list)
        if not_allowed:
            raise ValueError(f"The following names: {not_allowed} are not allowed")

        if undefined_literals:
            raise ValueError(f"{undefined_literals} need to be defined in definitions")
        return values

    @pydantic.root_validator()
    def substitute_expression(cls, values):
        # TODO there isn't a secure way to simplify the expression which does not involve using eval.
        #  Can be done with sdk on client side
        expression, definitions = values.get("expression"), values.get("definitions")
        new_definition = dict()
        for var_name, value in definitions.items():
            if isinstance(value, RegisterUserInput):
                new_definition[var_name] = value
                continue
            elif isinstance(value, int):
                pass
            elif isinstance(value, float):
                value = FixPointNumber(float_value=value).actual_float_value
            elif isinstance(value, FixPointNumber):
                value = value.actual_float_value
            else:
                raise ValueError(f"{type(value)} type is illegal")

            expression = re.sub(r"\b" + var_name + r"\b", str(value), expression)
        values["expression"] = expression
        values["definitions"] = new_definition
        return values

    @pydantic.validator("definitions")
    def set_register_names(cls, definitions):
        for k, v in definitions.items():
            if isinstance(v, RegisterUserInput):
                v.name = k
        return definitions

    @pydantic.validator("random_seed", always=True)
    def validate_random_seed(cls, random_seed):
        return random.randint(0, 1000) if not random_seed else random_seed

    def create_io_enums(self):
        literals = set(re.findall("[A-Za-z][A-Za-z0-9]*", self.expression))
        output_name = self.output_name if self.output_name else DEFAULT_OUT_NAME
        self._input_enum = Enum(
            "ArithmeticInputs",
            {literal: literal for literal in literals if literal not in white_list},
        )
        self._output_enum = Enum("ArithmeticOutputs", {output_name: output_name})

    class Config:
        extra = "forbid"


class ArithmeticOracle(Arithmetic):
    @pydantic.validator("expression")
    def validate_compare_expression(cls, value):
        ast_obj = ast.parse(value, "", "eval")
        if not isinstance(ast_obj.body, (ast.Compare, ast.BoolOp)):
            raise ValueError("Must a comparison expression")

        return value
