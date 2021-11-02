from enum import Enum
from typing import List, Type

import numpy as np
import pydantic

from classiq_interface.generator import function_params
from classiq_interface.generator.complex_type import Complex
from classiq_interface.generator.state_preparation import is_power_of_two


class SparseAmpLoadOutputs(Enum):
    OUTPUT_STATE = "OUTPUT_STATE"


def amplitudes_sum_to_one(amp):
    if round(sum(abs(np.array(amp)) ** 2), 8) != 1:
        raise ValueError("Probabilities do not sum to 1")
    return amp


class SparseAmpLoad(function_params.FunctionParams):
    """
    loads a sparse amplitudes vector
    """

    num_qubits: pydantic.PositiveInt = pydantic.Field(
        description="The number of qubits in the circuit."
    )
    amplitudes: List[Complex] = pydantic.Field(description="amplitudes vector to load")

    _is_power_of_two = pydantic.validator("amplitudes", allow_reuse=True)(
        is_power_of_two
    )
    _is_sum_to_one = pydantic.validator("amplitudes", allow_reuse=True)(
        amplitudes_sum_to_one
    )

    _input_enum = pydantic.PrivateAttr(default=function_params.DefaultInputEnum)
    _output_enum: Type[Enum] = pydantic.PrivateAttr(default=SparseAmpLoadOutputs)
