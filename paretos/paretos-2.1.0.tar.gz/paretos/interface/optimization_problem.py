from typing import List, Optional

from .design_parameter import DesignParameter
from .kpi_parameter import KpiParameter


class OptimizationProblem:
    """
    Summing up all relevant information for an optimization run.
    """

    def __init__(
        self,
        design_parameters: List[DesignParameter],
        kpi_parameters: List[KpiParameter],
        computational_effort: Optional[float] = None,
    ):
        self.__design_parameters = design_parameters
        self.__kpi_parameters = kpi_parameters
        self.__computational_effort = computational_effort

    def get_design_parameters(self) -> List[DesignParameter]:
        return self.__design_parameters

    def get_kpi_parameters(self) -> List[KpiParameter]:
        return self.__kpi_parameters

    def get_computational_effort(self) -> Optional[float]:
        return self.__computational_effort
