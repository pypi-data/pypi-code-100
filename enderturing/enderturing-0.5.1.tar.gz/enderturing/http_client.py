import logging

from typing import Optional, Union

import requests
import urllib3


log = logging.getLogger("enderturing")


class HttpClient:
    def __init__(self, config):
        self.config = config
        self._auth_token = None
        if not config.ssl_verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _get_full_api_url(self, path) -> str:
        return f"{self.config.url.strip('/')}/api/{self.config.api_version}{path}"

    def _get_auth_token(self) -> None:
        if self._auth_token:
            # todo: check expiration time
            return self._auth_token
        auth_data = {"username": self.config.auth_key, "password": self.config.auth_secret}
        log.info("Authenticating to Ender Turing SpeechEngine: %s", self.config.url)
        auth = requests.post(
            self._get_full_api_url("/login/access-token"), data=auth_data, verify=self.config.ssl_verify
        )
        auth.raise_for_status()
        authorization_json = auth.json()
        self._auth_token = authorization_json["access_token"]
        log.info("Authenticated, got token: xxxxx%s", self._auth_token[-4:])
        return self._auth_token

    def _get_auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self._get_auth_token()}"}

    def get(self, url: str, params: Optional[dict] = None) -> Union[dict, list]:
        """Executes authorized GET requests to API.

        Args:
            url : Target URL, excluding api version prefix (e.g. /events).
            params : Query parameters, which would be serialized as HTTP GET parameters.

        Returns:
            Parsed response JSON, can be any type that can be returned by json.loads(), but in most cases it's either
            dict or list.
        """
        response = requests.get(
            self._get_full_api_url(url), headers=self._get_auth_headers(), params=params, verify=self.config.ssl_verify
        )
        response.raise_for_status()
        response_json = response.json()
        log.debug("JSON response for %s: %s", url, str(response_json))
        return response_json

    def put(self, url: str, json: Union[dict, list] = None, **kwargs) -> Union[dict, list]:
        """Executes authorized PUT requests to API.

        Args:
            url : Target URL, excluding api version prefix (e.g. /events/).
            json : Request body, would be serialized as json.

        Returns:
            Parsed response JSON, can be any type that can be returned by json.loads(), but in most cases it's either
            dict or list.
        """
        response = requests.put(
            self._get_full_api_url(url),
            headers=self._get_auth_headers(),
            json=json,
            verify=self.config.ssl_verify,
            **kwargs,
        )
        response.raise_for_status()
        response_json = response.json()
        log.debug("JSON response for %s: %s", url, str(response_json))
        return response_json

    def post(self, url: str, json: Union[dict, list] = None, **kwargs) -> dict:
        """Executes authorized POST requests to API.

        Args:
            url : Target URL, excluding api version prefix (e.g. /events).
            json : Request body, would be serialized as json.

        Returns:
            Parsed response JSON, can be any type that can be returned by json.loads(), but in most cases it's either
            dict or list.
        """
        response = requests.post(
            self._get_full_api_url(url),
            headers=self._get_auth_headers(),
            json=json,
            verify=self.config.ssl_verify,
            **kwargs,
        )
        response.raise_for_status()
        response_json = response.json()
        log.debug("JSON response for %s: %s", url, str(response_json))
        return response_json
