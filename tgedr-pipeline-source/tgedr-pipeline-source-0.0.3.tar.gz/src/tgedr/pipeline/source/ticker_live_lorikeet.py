import logging
from typing import Any, Dict

from tgedr.pipeline.common.common import PipelineConfigException, PipelineSourceException
from tgedr.pipeline.common.source import PipelineSource
from yahoo_fin import stock_info

log = logging.getLogger(__name__)


class TickerLiveLorikeet(PipelineSource):
    """
    gets live ticker with yahoo_fin library
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        super(TickerLiveLorikeet, self).__init__(config=config)
        self.__tickers = self._get_config("tickers")

    def get(self) -> Any:
        self.log.info("[get|in]")

        result = []
        for ticker in self.__tickers:
            try:
                d = stock_info.get_quote_table(ticker)
                result.append(d)
            except Exception as x:
                raise PipelineSourceException(f"could not retrieve ticker: {ticker}") from x
        self.log.info("[get|out]")
        return result

    def _validate_config(self, config: Dict[str, Any]) -> None:
        self.log.info(f"[_validate_config|in]{config}")
        expected_configs = ["tickers"]
        actual_configs = list(config.keys())
        if not all(conf in actual_configs for conf in expected_configs):
            raise PipelineConfigException(f"expected configs: {expected_configs} \n actual configs: {actual_configs}")
        self.log.info("[_validate_config|out]")
