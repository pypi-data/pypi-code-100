import os
from logging import Logger, LoggerAdapter
from typing import Optional, Union

from .default_logger import DefaultLogger
from .exceptions import ConfigError
from .service.url_validator import is_valid_url


class Config(object):
    KEYCLOAK_DEFAULT_URL = "https://auth.paretos.io/auth/"
    SOCRATES_API_DEFAULT_URL = "https://api.paretos.io/socrates/"
    ATHENA_API_DEFAULT_URL = "https://athena.paretos.io/"
    KEYCLOAK_REALM_NAME = "paretos"
    KEYCLOAK_CLIENT_ID = "main"

    def __init__(
        self,
        username: str = "",
        password: str = "",
        keycloak_server_url: str = None,
        keycloak_realm_name: str = KEYCLOAK_REALM_NAME,
        keycloak_socrates_api_client_id: str = KEYCLOAK_CLIENT_ID,
        socrates_url: str = None,
        athena_url: str = None,
        logger: Optional[Union[Logger, LoggerAdapter]] = None,
        dashboard_host: str = "127.0.0.1",
        dashboard_port: str = "8080",
    ):
        self.__username = username
        self.__password = password
        self.__keycloak_server_url = self.__canonize_url(
            keycloak_server_url
            or os.environ.get("KEYCLOAK_SERVER_URL")
            or self.KEYCLOAK_DEFAULT_URL
        )
        self.__keycloak_realm_name = keycloak_realm_name
        self.__keycloak_socrates_api_client_id = keycloak_socrates_api_client_id
        self.__socrates_url = self.__canonize_url(
            socrates_url
            or os.environ.get("SOCRATES_URL")
            or self.SOCRATES_API_DEFAULT_URL
        )
        self.__athena_url = self.__canonize_url(
            athena_url or os.environ.get("ATHENA_URL") or self.ATHENA_API_DEFAULT_URL
        )
        self.__logger = logger or DefaultLogger()
        self.__dashboard_host = dashboard_host
        self.__dashboard_port = dashboard_port

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_keycloak_realm_name(self) -> str:
        return self.__keycloak_realm_name

    def get_keycloak_socrates_api_client_id(self) -> str:
        return self.__keycloak_socrates_api_client_id

    @staticmethod
    def __canonize_url(api_url):
        if not is_valid_url(api_url):
            raise ConfigError(f"'{api_url}' is not a valid url")
        if api_url[len(api_url) - 1] != "/":
            api_url = api_url + "/"
        return api_url

    def get_socrates_api_url(self) -> str:
        return self.__socrates_url

    def get_athena_api_url(self) -> str:
        return self.__athena_url

    def get_keycloak_server_url(self) -> str:
        return self.__keycloak_server_url

    def get_logger(self) -> Logger:
        return self.__logger

    def get_dashboard_host(self) -> str:
        return self.__dashboard_host

    def get_dashboard_port(self) -> str:
        return self.__dashboard_port
