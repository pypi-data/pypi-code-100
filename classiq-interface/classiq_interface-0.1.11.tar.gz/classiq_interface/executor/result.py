import enum
from typing import Dict, Optional, Union

import pydantic

from classiq_interface.hybrid.result import VQESolverResult


class ExecutionStatus(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class VaRResult(pydantic.BaseModel):
    var: float = None
    alpha: float = None


class FinanceSimulationResults(pydantic.BaseModel):
    var_results: Optional[VaRResult] = None
    result: Optional[float] = None

    @pydantic.root_validator()
    def validate_atleast_one_field(cls, values: Dict) -> Dict:
        is_var_results_defined = values.get("var_results") is not None
        is_result_defined = values.get("result") is not None

        if not is_var_results_defined and not is_result_defined:
            raise ValueError(
                "At least one of var_results and result should be defined."
            )

        return values


class GroverSimulationResults(pydantic.BaseModel):
    result: Dict[str, Union[float, int]]


class ExecutionDetails(pydantic.BaseModel):
    vendor_format_result: Dict = pydantic.Field(
        ..., description="Result in proprietary vendor format"
    )


ExecutionData = Union[
    ExecutionDetails,
    FinanceSimulationResults,
    GroverSimulationResults,
    VQESolverResult,
    str,
]


class ExecutionResult(pydantic.BaseModel):
    status: ExecutionStatus
    details: ExecutionData
