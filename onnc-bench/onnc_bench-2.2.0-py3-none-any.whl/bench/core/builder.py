from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict
from .project import ProjectData
from .deployment import Deployment
from .benchmark import Metric
from .compiler import ONNCSaaSCompiler
from ..config import api_protocol, api_url, api_port
from .model.serializer import serialize as serialize_model
from .dataset.serializer import serialize as serialize_dataset
from ..utils import get_tmp_path


class IBuilder(ABC):
    def __init__(self, name: str, info: Dict) -> None:
        self.project_data = None

    @abstractmethod
    def calibrate(self, model: object, dataset: object, parameters: Dict):
        pass

    @abstractmethod
    def build(self, device: str, parameters: Dict):
        pass

    @abstractmethod
    def save(self, output: Path) -> Deployment:
        pass

    @abstractmethod
    def measure_perf(self) -> Metric:
        pass


class ONNCSaaSAPISBuilder(IBuilder):
    def __init__(self, project: ProjectData):
        self.project = project
        self.compiler = ONNCSaaSCompiler(protocol=api_protocol,
                                         url=api_url, port=api_port)
        self._to_be_removed = []

        def __init__(name: str, info: Dict) -> None:
            pass

        def calibrate(self, parameters):
            for mp in self.project.model_packages:
                model = mp.model
                dataset = mp.dataset

                tmp_model_path = get_tmp_path()
                tmp_ds_path = get_tmp_path()

                self._to_be_removed.append(tmp_model_path)
                self._to_be_removed.append(tmp_ds_path)

                serialize_model(model, tmp_model_path)
                serialize_dataset(dataset, tmp_ds_path)

                self.compiler.upload_model(tmp_model_path, tmp_ds_path)

        def build(self, device: str, params: Dict):
            params['device': device]
            self.compiler.compile(params)

        def save(path: Path):
            self.compiler.download(path)

        def measure_perf(device: str):
            pass

