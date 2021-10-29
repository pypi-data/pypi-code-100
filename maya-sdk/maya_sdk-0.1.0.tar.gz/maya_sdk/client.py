import requests
import maya_sdk
from .errors import AuthenticationError


class Client():
    def __init__(self, authorization=None, base_url="https://api.mayainsights.com"):
        self.authorization = authorization
        self.base_url = base_url
        super().__init__()

    @staticmethod
    def from_api_key(api_key):
        return Client(f"Bearer {api_key}")

    @staticmethod
    def from_access_token(access_token):
        return Client(f"Bearer {access_token}")

    def api_call(self, method: str, path: str, **kwargs) -> requests.Response:
        if self.authorization is None:
            if maya_sdk.api_key is None:
                 raise AuthenticationError(
                  "No API key provided. (HINT: set your API key using "
                  '"maya_sdk.api_key = <API-KEY>"). Contact support to generate api keys, '
                  "or if you have any questions."
                )                            
            authorization = f"Bearer {maya_sdk.api_key}"
        else:
            authorization = self.authorization
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = authorization
        url = f"{self.base_url}{path}"
        resp = requests.request(method, url=url, headers=headers, **kwargs)
        # print('response:', resp.text)
        resp.raise_for_status()
        return resp
