from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Union

from clearml import Task
from numpy import ndarray
from pandas import DataFrame
from PIL.Image import Image


class ClearMLReporterI(ABC):
    @abstractmethod
    def report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        pass

    @abstractmethod
    def upload_artifact(
        self,
        name: str,
        artifact_object: Union[str, Mapping[Any, Any], DataFrame, ndarray, Image],
        metadata: Optional[Mapping[Any, Any]] = None,
    ) -> None:
        pass


class ClearMLReporterNull(ClearMLReporterI):
    def report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        pass

    def upload_artifact(
        self,
        name: str,
        artifact_object: Union[str, Mapping[Any, Any], DataFrame, ndarray, Image],
        metadata: Optional[Mapping[Any, Any]] = None,
    ) -> None:
        pass


class ClearMLReporter(ClearMLReporterI):
    def __init__(self, task: Task) -> None:
        self.task = task
        self.logger = self.task.get_logger()

    def report_scalar(self, title: str, series: str, value: Union[int, float], iteration: int) -> None:
        self.logger.report_scalar(title=title, series=series, value=value, iteration=iteration)

    def upload_artifact(
        self,
        name: str,
        artifact_object: Union[str, Mapping[Any, Any], DataFrame, ndarray, Image],
        metadata: Optional[Mapping[Any, Any]] = None,
    ) -> None:
        self.task.upload_artifact(name=name, artifact_object=artifact_object, metadata=metadata)
