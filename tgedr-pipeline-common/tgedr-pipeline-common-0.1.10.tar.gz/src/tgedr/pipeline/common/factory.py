import inspect
import logging
from importlib import import_module
from typing import Any, Dict

from tgedr.pipeline.common.common import PipelineComponent
from tgedr.pipeline.common.sink import PipelineSink
from tgedr.pipeline.common.source import PipelineSource

logger = logging.getLogger(__name__)


class Factory:
    @staticmethod
    def __get(config: Dict[str, Any], clazz: Any) -> PipelineComponent:
        logger.info(f"[Factory.__get|in] ({config}, {clazz})")

        classname = config["class"]
        module = config["module"]
        config = config["config"]

        callable_object = getattr(import_module(module), classname)
        if not inspect.isclass(callable_object):
            raise TypeError("[Factory.__get] not a class")
        else:
            if not issubclass(callable_object, clazz):
                raise TypeError(f"[Factory.__get] Wrong class type, it is not a subclass of {clazz.__name__}")

        logger.info(f"[Factory.__get] loading PipelineComponent {module}.{classname}")
        instance = callable_object(config)
        logger.info(f"[Factory.__get|out] =>  {instance}")
        return instance

    @staticmethod
    def get_sink(config: Dict[str, Any]) -> PipelineSink:
        logger.info(f"[Factory.get_sink|in] ({config})")
        result = Factory.__get(config, PipelineSink)
        logger.info(f"[Factory.get_sink|out] =>  {result}")
        return result

    @staticmethod
    def get_source(config: Dict[str, Any]) -> PipelineSource:
        logger.info(f"[Factory.get_source|in] ({config})")
        result = Factory.__get(config, PipelineSource)
        logger.info(f"[Factory.get_source|out] =>  {result}")
        return result
