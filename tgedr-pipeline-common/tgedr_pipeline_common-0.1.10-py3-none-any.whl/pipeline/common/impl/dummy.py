from typing import Any, Dict

from tgedr.pipeline.common.common import PipelineConfigException
from tgedr.pipeline.common.sink import PipelineSink
from tgedr.pipeline.common.source import PipelineSource


class DummyPipelineSink(PipelineSink):
    def __init__(self, config: Dict[str, Any]) -> None:
        super(DummyPipelineSink, self).__init__(config=config)

    def put(self, msg: str) -> None:
        self.log.info("putting")

    def _validate_config(self, config: Dict[str, Any]) -> None:
        if "valid" in config.keys() and not config["valid"]:
            raise PipelineConfigException("not valid")


class DummyPipelineSource(PipelineSource):
    def __init__(self, config: Dict[str, Any]) -> None:
        super(DummyPipelineSource, self).__init__(config=config)

    def get(self) -> Any:
        self.log.info("getting")
        return "ola"

    def _validate_config(self, config: Dict[str, Any]) -> None:
        if "valid" in config.keys() and not config["valid"]:
            raise PipelineConfigException("not valid")
