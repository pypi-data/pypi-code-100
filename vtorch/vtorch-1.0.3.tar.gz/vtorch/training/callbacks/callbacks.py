from typing import Any, Dict, Mapping, Optional, Union

from numpy import ndarray
from pandas import DataFrame
from PIL.Image import Image

from .clearml_reporter import ClearMLReporterI, ClearMLReporterNull
from .early_stopping import EarlyStoppingI, EarlyStoppingNull


class Callbacks:
    def __init__(
        self, clearml_reporter: Optional[ClearMLReporterI] = None, early_stopping: Optional[EarlyStoppingI] = None
    ) -> None:
        self.clearml_reporter = clearml_reporter or ClearMLReporterNull()
        self.early_stopping = early_stopping or EarlyStoppingNull()

    def clearml_report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        self.clearml_reporter.report_scalar(title=title, series=series, value=value, iteration=iteration)

    def clearml_upload_artifact(
        self,
        name: str,
        artifact_object: Union[str, Mapping[Any, Any], DataFrame, ndarray, Image],
        metadata: Optional[Mapping[Any, Any]] = None,
    ) -> None:
        self.clearml_reporter.upload_artifact(name=name, artifact_object=artifact_object, metadata=metadata)

    def add_metric(self, val_metrics: Dict[str, float]) -> None:
        self.early_stopping.add_metric(val_metrics)

    def should_stop_early(self) -> bool:
        return self.early_stopping.should_stop_early()

    def is_best_so_far(self) -> bool:
        return self.early_stopping.is_best_so_far()
