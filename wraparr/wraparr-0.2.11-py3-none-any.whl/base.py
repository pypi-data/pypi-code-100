import httpx


class BaseAPI:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        quality_profile: int,
        root_folder: str,
        timeout: int = 60,
    ) -> None:

        self.base_url = base_url
        self.api_url = base_url.rstrip("/") + "/api/v3"
        self.api_key = api_key
        self.quality_profile = quality_profile
        self.root_folder = root_folder
        self.timeout = timeout

        async def raise_on_4xx_5xx(response: httpx.Response) -> None:
            response.raise_for_status()

        self._client = httpx.AsyncClient(
            base_url=self.api_url,
            headers={"X-Api-Key": self.api_key},
            event_hooks={"response": [raise_on_4xx_5xx]},
            timeout=timeout,
        )
