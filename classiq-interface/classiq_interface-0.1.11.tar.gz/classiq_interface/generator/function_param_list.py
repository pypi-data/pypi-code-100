from typing import Set, Type

from classiq_interface.generator.amplitude_estimation import AmplitudeEstimation
from classiq_interface.generator.arith.arithmetic import Arithmetic, ArithmeticOracle
from classiq_interface.generator.arith.binary_ops import (
    Adder,
    BitwiseAnd,
    BitwiseOr,
    BitwiseXor,
    Equal,
    GreaterEqual,
    GreaterThan,
    LessEqual,
    LessThan,
    NotEqual,
    Subtractor,
)
from classiq_interface.generator.arith.unary_ops import Negation
from classiq_interface.generator.custom_functions.custom_function import CustomFunction
from classiq_interface.generator.entangler_params import (
    GridEntangler,
    HypercubeEntangler,
    TwoDimensionalEntangler,
)
from classiq_interface.generator.finance import Finance, FinanceModels, FinancePayoff
from classiq_interface.generator.function_params import FunctionParams
from classiq_interface.generator.grover_operator import GroverOperator
from classiq_interface.generator.hadamard_amp_load import HadamardAmpLoad
from classiq_interface.generator.hardware_efficient_ansatz import (
    HardwareEfficientAnsatz,
)
from classiq_interface.generator.integer_comparator import IntegerComparator
from classiq_interface.generator.mcx import Mcx
from classiq_interface.generator.qaoa_ansatz import QaoaAnsatz
from classiq_interface.generator.qft import QFT
from classiq_interface.generator.sparse_amp_load import SparseAmpLoad
from classiq_interface.generator.state_preparation import StatePreparation
from classiq_interface.generator.state_propagator import StatePropagator
from classiq_interface.generator.unitary_gate import UnitaryGate
from classiq_interface.generator.vqe_ansatz import VQEAnsatz

_function_param_list = {
    StatePreparation,
    VQEAnsatz,
    QaoaAnsatz,
    StatePropagator,
    QFT,
    BitwiseAnd,
    BitwiseOr,
    BitwiseXor,
    Adder,
    Arithmetic,
    ArithmeticOracle,
    Equal,
    NotEqual,
    GreaterThan,
    GreaterEqual,
    LessThan,
    LessEqual,
    Negation,
    Subtractor,
    TwoDimensionalEntangler,
    IntegerComparator,
    Finance,
    FinanceModels,
    FinancePayoff,
    HypercubeEntangler,
    AmplitudeEstimation,
    SparseAmpLoad,
    GridEntangler,
    HadamardAmpLoad,
    GroverOperator,
    Mcx,
    CustomFunction,
    HardwareEfficientAnsatz,
    UnitaryGate,
}


def get_function_param_list() -> Set[Type[FunctionParams]]:
    return _function_param_list
