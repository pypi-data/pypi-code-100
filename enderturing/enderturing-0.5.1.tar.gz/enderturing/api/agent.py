from enderturing import Config
from enderturing.http_client import HttpClient


class Agent:
    """Contains methods for agents data access.

    Args:
        config (Config): configuration to use.
        client (HttpClient): HTTP client instance to use for requests
    """
    def __init__(self, config: Config, client: HttpClient):
        self._config = config
        self._http_client = client

    def upload_csv(self, filepath: str):
        result = self._http_client.post(
            "/agents/csv",
            files={"file": ("csv_filename", open(filepath, "rb"), "text/csv")}
        )
        return {
            'created': result['created']
        }
