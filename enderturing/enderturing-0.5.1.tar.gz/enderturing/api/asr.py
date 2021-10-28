from typing import List, Optional

from enderturing import Config
from enderturing.http_client import HttpClient


class Asr:
    def __init__(self, config: Config, client: HttpClient):
        """
        Args:
            config (Config): configuration to use.
            client (HttpClient): HTTP client instance to use for requests
        """
        self._config = config
        self._http_client = client

    def _is_asr_up(self, asr_data):
        return (
            asr_data
            and "containers_status" in asr_data
            and asr_data["containers_status"]
            and all((x["running"] > 0 for x in asr_data["containers_status"]))
        )

    def get_instances(self, active_only: bool = True, languages: Optional[List[str]] = None):
        result = self._http_client.get("/asr")
        if active_only:
            result = (x for x in result if self._is_asr_up(x))
        if languages:
            result = (x for x in result if x["language"] in languages)
        return list(result)
