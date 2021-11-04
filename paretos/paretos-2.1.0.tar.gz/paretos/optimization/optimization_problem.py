from typing import Optional

from .design import DesignSpace
from .kpi import KpiSpace


class OptimizationProblem:
    """
    Summing up all relevant information for an optimization run.
    """

    def __init__(
        self,
        design_space: DesignSpace,
        kpi_space: KpiSpace,
        computational_effort: Optional[float] = None,
    ):
        self.__design_space = design_space
        self.__kpi_space = kpi_space
        self.__computational_effort = computational_effort

    def get_design_space(self) -> DesignSpace:
        return self.__design_space

    def get_kpi_space(self) -> KpiSpace:
        return self.__kpi_space

    def get_computational_effort(self) -> Optional[float]:
        return self.__computational_effort
