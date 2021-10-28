from abc import abstractmethod
from typing import Any, Dict

from tgedr.pipeline.common.common import PipelineComponent


class PipelineSource(PipelineComponent):
    """
    abstract class to extend in order to implement various sources
    """

    def __init__(self, config: Dict[str, Any]):
        super(PipelineSource, self).__init__(config)

    @abstractmethod
    def get(self) -> Any:
        """
        gets data from a source

        Returns
        ----------
        Any
            data
        """
