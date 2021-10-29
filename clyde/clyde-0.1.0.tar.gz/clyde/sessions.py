import requests

import urllib.parse

class BaseUrlSession(requests.Session):
    base_url = None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}(base_url={self.base_url!r})>'

    def prepare_request(self, request: requests.Request) -> requests.PreparedRequest:
        if self.base_url is not None:
            request.url = urllib.parse.urljoin(self.base_url, request.url)

        return super().prepare_request(request)
