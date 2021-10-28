from abc import abstractmethod
from typing import Any, Dict

from tgedr.pipeline.common.common import PipelineComponent


class PipelineSink(PipelineComponent):
    """
    abstract class to extend in order to implement various sinks
    """

    def __init__(self, config: Dict[str, Any]):
        super(PipelineSink, self).__init__(config)

    @abstractmethod
    def put(self, msg: str) -> None:
        """
        puts data into a sink

        Parameters
        ----------
        msg : str
            the msg to be sent, in a specific format,  json or other, the consumers will have to adapt
        """
