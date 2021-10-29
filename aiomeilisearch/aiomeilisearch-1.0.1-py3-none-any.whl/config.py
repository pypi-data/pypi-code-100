from typing import Optional

class Config:
    def __init__(self, url: str, api_key: Optional[str] = None, timeout: Optional[int] = None) -> None:
        self.__url = url
        self.__api_key = api_key
        self.__timeout = timeout

    @property
    def url(self):
        return self.__url

    @property
    def api_key(self):
        return self.__api_key

    @property
    def timeout(self):
        return self.__timeout
