import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

from configlookup.main import Configuration


class PipelineException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)


class PipelineConfigException(PipelineException):
    def __init__(self, *args, **kwargs):
        super(PipelineException, self).__init__(*args, **kwargs)


class PipelineSinkException(PipelineException):
    def __init__(self, *args, **kwargs):
        super(PipelineException, self).__init__(*args, **kwargs)


class PipelineSourceException(PipelineException):
    def __init__(self, *args, **kwargs):
        super(PipelineException, self).__init__(*args, **kwargs)


class PipelineComponent(ABC):
    """
    abstract class to extend in order to implement various pipeline components
    """

    def __init__(self, config: Dict[str, Any]):
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.info(f"[__init__|in] ({config})")
        self._validate_config(config)
        self._config = config
        self._log.info("[__init__|out]")

    @property
    def log(self) -> logging.Logger:
        return self._log

    def text_fragment(self, text: str, length: int = 10) -> str:
        self.log.info("[_text_fragment|in]")
        if text is None:
            raise ValueError("[_text_fragment] no text provided")
        substr_len = min(max(0, length - 3), len(text))
        result = text[0:substr_len] + "..."
        self.log.info(f"[_text_fragment|out] => {result}")
        return result

    def _get_config(self, entry):
        self.log.info(f"[_get_config|in] ({entry})")
        result = None
        try:
            config_entry = self._config[entry]
            if "value" in config_entry.keys():
                result = config_entry["value"]
            elif "key" in config_entry.keys():
                result = Configuration.get(config_entry["key"])
            else:
                raise ValueError(f"[_get_config] no value or key defined in config entry: {entry}")
        except Exception as le:
            raise PipelineConfigException(f"[_get_config] config not found: {entry}") from le
        self.log.info(f"[_get_config|out] => {self.text_fragment(str(result))}")
        return result

    @abstractmethod
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        validates config being provided

        Raises
        ----------
        PipelineConfigException
            exception with description of config failure
        """
