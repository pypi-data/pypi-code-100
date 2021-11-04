from logging import Logger, LoggerAdapter
from typing import Union
from urllib.parse import urljoin

from requests import ConnectionError, Response, Session
from requests.adapters import HTTPAdapter

from paretos.authentication.access_token_provider import AccessTokenProvider
from paretos.service.exceptions import (
    InvalidResponseStructure,
    RequestFailed,
    ResponseParsingError,
)
from paretos.version import VERSION


class ApiHttpSession:
    def __init__(
        self,
        api_url: str,
        api_name: str,
        access_token_provider: AccessTokenProvider,
        logger: Union[Logger, LoggerAdapter],
    ):
        self.__api_url = api_url
        self.__api_name = api_name
        self.__access_token_provider = access_token_provider
        self.__logger = logger
        self.__session = Session()
        self.__build_session()

    def __build_session(self):
        retry_adapter = HTTPAdapter(max_retries=5)
        self.__session.mount("http://", retry_adapter)
        self.__session.mount("https://", retry_adapter)
        self.__session.headers.update(
            {
                "Accept-Charset": "utf-8",
                "Content-Type": "application/json",
                "User-Agent": "paretos/{}".format(VERSION),
            }
        )

    def __get_data_from_response(self, response):
        try:
            response_json = response.json()
        except ValueError:
            self.__logger.error(
                "Unable to parse " + self.__api_name + " API response json."
            )
            raise ResponseParsingError()

        if "status" not in response_json:
            self.__logger.error("Unexpected " + self.__api_name + " API response.")
            raise InvalidResponseStructure()

        if response_json["status"] != "success":
            self.__logger.error(
                "" + self.__api_name + " API request failed.",
                extra={"response": response_json},
            )

            raise RequestFailed()

        if "data" not in response_json:
            self.__logger.error("Unexpected " + self.__api_name + " API response.")
            raise InvalidResponseStructure()

        return response_json["data"]

    def authenticated_request(
        self,
        path: str,
        version: str,
        contains_sensitive_data: bool,
        data: dict = None,
        method: str = "POST",
    ):
        if method not in ["POST", "GET"]:
            raise ValueError("Invalid Request method chosen.")

        self.__update_authorization_in_session_headers()

        url = self.__get_url_from_path_and_version(path, version)

        self.__log_request(
            url=url,
            method=method,
            data=data,
            contains_sensitive_data=contains_sensitive_data,
        )

        try:
            response = self.__session.request(method, url, json=data)
        except ConnectionError:
            self.__logger.error(
                "Unable to connect to " + self.__api_name + " API.", extra={"url": url}
            )

            raise RuntimeError("Unable to connect to " + self.__api_name + " API.")

        self.__log_response(
            contains_sensitive_data=contains_sensitive_data, response=response
        )

        return self.__get_data_from_response(response)

    def __get_url_from_path_and_version(self, path, version) -> str:
        path = self.__get_versioned_path(path, version)
        url = urljoin(self.__api_url, path)
        return url

    def __update_authorization_in_session_headers(self):
        access_token_string = self.__access_token_provider.get_access_token()
        auth_header = "Bearer {}".format(access_token_string)
        self.__session.headers["Authorization"] = auth_header

    @staticmethod
    def __get_versioned_path(path: str, version: str = "v1") -> str:
        return f"{version}/{path}"

    def __log_request(self, url: str, method: str, data, contains_sensitive_data: bool):
        details = {"url": url, "method": method}

        if not contains_sensitive_data:
            details["data"] = data

        self.__logger.debug(self.__api_name + " API request.", extra=details)

    def __log_response(self, contains_sensitive_data: bool, response: Response):
        details = {"status": response.status_code}

        if not contains_sensitive_data:
            details["data"] = response.text

        self.__logger.debug(self.__api_name + " API response.", extra=details)
