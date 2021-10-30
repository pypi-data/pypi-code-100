import aiohttp


class EndpointNotFound(aiohttp.InvalidURL):

    def __init__(self, error="Endpoint not found.", *args: object) -> None:
        super().__init__(error, *args)
