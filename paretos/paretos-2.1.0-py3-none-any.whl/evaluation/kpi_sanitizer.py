import math
from logging import Logger
from typing import Dict

from .. import optimization
from ..exceptions import (
    InfiniteValueInEvaluationResult,
    KpiNotFoundInEvaluationResult,
    NotANumberInEvaluationResult,
)


class KpiSanitizer:
    """
    Ensures that the KPIs provided by the individually Environment implementation
    are complete and well-formed.
    """

    def __init__(self, kpi_space: optimization.kpi.KpiSpace, logger: Logger):
        self.__kpi_space = kpi_space
        self.__logger = logger

    def clean_kpis(
        self,
        original_kpis: Dict[str, float],
        evaluation_uuid: str,
    ) -> optimization.kpi.KpiValues:
        clean_kpis = []

        for kpi in self.__kpi_space:
            name = kpi.get_name()

            if name not in original_kpis:
                self.__logger.error(
                    msg="KPI missing in evaluation result.",
                    extra={"kpi_name": name, "evaluation_uuid": evaluation_uuid},
                )

                raise KpiNotFoundInEvaluationResult(
                    f"KPI {name} missing in evaluation result."
                )

            value = original_kpis[name]
            value_type = type(value)

            if value_type is not float:
                if value_type is int:
                    value = float(value)
                else:
                    self.__logger.error(
                        msg="Evaluation result contains invalid types.",
                        extra={
                            "kpi_name": name,
                            "type": str(type(value)),
                            "evaluation_uuid": evaluation_uuid,
                        },
                    )

                    raise TypeError(
                        "Evaluation result contains invalid type. "
                        "Results have to be an instance of float."
                    )

            if math.isnan(value):
                raise NotANumberInEvaluationResult(
                    "Evaluation result contains invalid value 'nan'. "
                    "Results have to be real numbers."
                )

            if math.isinf(value):
                raise InfiniteValueInEvaluationResult(
                    "Evaluation result contains invalid infinite value. "
                    "Results have to be real numbers."
                )

            clean_kpi = optimization.parameter.ParameterValue(kpi, value)

            clean_kpis.append(clean_kpi)

        return optimization.kpi.KpiValues(clean_kpis)
