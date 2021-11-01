from typing import Any, List

from abc import abstractmethod
from pathlib import Path
from onnc.bench.core.project import ProjectData
from onnc.bench.core.deployment import Deployment

class IBuilder:

    BUILDER_NAME = ""

    def __init__(self, project_data: ProjectData):
        self.project_data = project_data
        self.model_ids: List = []

    @abstractmethod
    def prepare_model(self, model, dataset, model_meta, dataset_meta) -> Any:
        """Make files of a model and its corresponding dataset ready in given
           path and place.
        """
        pass

    @abstractmethod
    def calibrate(self, model_id, params) -> Any:
        """Calibrate a model package(model and its corresponding samples)
        """
        pass

    @abstractmethod
    def compile(self, model_id, params) -> Any:
        """Compile a model package(model and its corresponding samples)
        """
        pass

    @abstractmethod
    def build(self, device) -> Any:
        """build a project witch contains multiple models

        for model in model_ids:
            ...
        """
        pass

    @abstractmethod
    def save(self, output: Path) -> Deployment:
        pass
