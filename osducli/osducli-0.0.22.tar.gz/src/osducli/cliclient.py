#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Useful functions."""

import os
import sys
from configparser import NoOptionError, NoSectionError
from functools import wraps
from typing import Union
from urllib.parse import urljoin

import requests
from osdu.client import OsduClient
from osdu.identity import OsduMsalInteractiveCredential, OsduTokenCredential
from requests.models import HTTPError

from osducli.config import (
    CLI_CONFIG_DIR,
    CONFIG_AUTHENTICATION_AUTHORITY,
    CONFIG_AUTHENTICATION_MODE,
    CONFIG_AUTHENTICATION_SCOPES,
    CONFIG_CLIENT_ID,
    CONFIG_CLIENT_SECRET,
    CONFIG_DATA_PARTITION_ID,
    CONFIG_REFRESH_TOKEN,
    CONFIG_SERVER,
    CONFIG_TOKEN_ENDPOINT,
    CLIConfig,
)
from osducli.log import get_logger
from osducli.util.exceptions import CliError

MSG_JSON_DECODE_ERROR = (
    "Unable to decode the response. Try running again with the --debug command line argument for"
    " more information"
)
MSG_HTTP_ERROR = (
    "An error occurred when accessing the api. Try running again with the --debug command line argument for"
    " more information"
)


logger = get_logger(__name__)


def handle_cli_exceptions(function):
    """Decorator to provide common cli error handling"""

    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except HTTPError as ex:
            logger.error(MSG_HTTP_ERROR)
            logger.error("Error (%s) - %s", ex.response.status_code, ex.response.reason)
        except CliError as ex:
            logger.error("Error %s", ex.message)
        except ValueError as ex:
            logger.error(MSG_JSON_DECODE_ERROR)
            logger.debug(ex)
        except (NoOptionError, NoSectionError) as ex:
            logger.warning(
                "Configuration missing from config ('%s'). Run 'osdu config update'", ex.args[0]
            )
        sys.exit(1)

    return decorated


class CliOsduClient(OsduClient):
    """Specific class for use from the CLI that provides common error handling, use of configuration
    and messaging

    Args:
        OsduClient ([type]): [description]
    """

    def __init__(self, config: CLIConfig):
        """Setup the new client

        Args:
            config (CLIConfig): cli configuration
        """

        self.config = config

        try:
            # required
            server = config.get("core", CONFIG_SERVER)
            data_partition = config.get("core", CONFIG_DATA_PARTITION_ID)
            retries = config.getint("core", "retries", 0)
            authentication_mode = config.get("core", CONFIG_AUTHENTICATION_MODE)

            if authentication_mode == "refresh_token":
                client_id = config.get("core", CONFIG_CLIENT_ID)
                token_endpoint = config.get("core", CONFIG_TOKEN_ENDPOINT, None)
                refresh_token = config.get("core", CONFIG_REFRESH_TOKEN, None)
                client_secret = config.get("core", CONFIG_CLIENT_SECRET, None)
                credentials = OsduTokenCredential(
                    client_id, token_endpoint, refresh_token, client_secret
                )
            elif authentication_mode == "msal_interactive":
                client_id = config.get("core", CONFIG_CLIENT_ID)
                authority = config.get("core", CONFIG_AUTHENTICATION_AUTHORITY, None)
                scopes = config.get("core", CONFIG_AUTHENTICATION_SCOPES, None)
                cache_path = os.path.join(CLI_CONFIG_DIR, "msal_token_cache.bin")
                credentials = OsduMsalInteractiveCredential(
                    client_id, authority, scopes, cache_path
                )
            else:
                logger.error(
                    "Unknown type of authentication mode %s. Run 'osdu config update'.",
                    authentication_mode,
                )
                sys.exit(2)

            super().__init__(server, data_partition, credentials, retries)
        except (NoOptionError, NoSectionError) as ex:
            logger.warning(
                "Authentication information missing from config ('%s'). Run 'osdu config update'",
                ex.args[0],
            )
            sys.exit(1)

    def _url_from_config(self, config_url_key: str, url_extra_path: str) -> str:
        """Construct a url using values from configuration"""
        unit_url = self.config.get("core", config_url_key)
        url = urljoin(self.server_url, unit_url) + url_extra_path
        return url

    def cli_get(
        self, config_url_key: str, url_extra_path: str, ok_status_codes: list = None
    ) -> requests.Response:
        """[summary]

        Args:
            config_url_key (str): key in configuration for the base path
            url_extra_path (str): extra path to add to the base path
            ok_status_codes (list, optional): Status codes for successful call. Defaults to [200].
        """
        url = self._url_from_config(config_url_key, url_extra_path)
        response = self.get(url)
        if ok_status_codes is not None and response.status_code not in ok_status_codes:
            raise HTTPError(response=response)
        return response

    def cli_get_returning_json(
        self, config_url_key: str, url_extra_path: str, ok_status_codes: list = None
    ) -> dict:
        """[summary]

        Args:
            config_url_key (str): key in configuration for the base path
            url_extra_path (str): extra path to add to the base path
            ok_status_codes (list, optional): accepted ok response codes. Defaults to None.
        """
        url = self._url_from_config(config_url_key, url_extra_path)
        return self.get_returning_json(url, ok_status_codes)

    def cli_post_returning_json(
        self,
        config_url_key: str,
        url_extra_path: str,
        data: Union[str, dict],
        ok_status_codes: list = None,
    ) -> dict:
        """[summary]

        Args:
            config_url_key (str): key in configuration for the base path
            url_extra_path (str): extra path to add to the base path
            data (Union[str, dict]): json data as string or dict to send as the body
            ok_status_codes (list, optional): Status codes indicating successful call. Defaults to [200].

        Returns:
            dict: returned json
        """
        url = self._url_from_config(config_url_key, url_extra_path)
        return self.post_returning_json(url, data, ok_status_codes)

    def cli_delete(
        self,
        config_url_key: str,
        url_extra_path: str,
        ok_status_codes: list = None,
    ):
        """[summary]

        Args:
            config_url_key (str): key in configuration for the base path
            url_extra_path (str): extra path to add to the base path
            data (Union[str, dict]): json data as string or dict to send as the body
            ok_status_codes (list, optional): Status codes indicating successful call. Defaults to [200].

        Returns:
            [type]: [description]
        """
        try:
            url = self._url_from_config(config_url_key, url_extra_path)
            self.delete(url, ok_status_codes)
            return
        except HTTPError as ex:
            logger.error(MSG_HTTP_ERROR)
            logger.error("Error (%s) - %s", ex.response.status_code, ex.response.reason)
        except ValueError as ex:
            logger.error(MSG_JSON_DECODE_ERROR)
            logger.debug(ex)
        except (NoOptionError, NoSectionError) as ex:
            logger.warning(
                "Configuration missing from config ('%s'). Run 'osdu config update'", ex.args[0]
            )

        sys.exit(1)

    def cli_put(
        self,
        config_url_key: str,
        url_extra_path: str,
        data: Union[str, dict],
        ok_status_codes: list = None,
    ) -> requests.Response:
        """[summary]

        Args:
            config_url_key (str): key in configuration for the base path
            url_extra_path (str): extra path to add to the base path
            ok_status_codes (list, optional): Status codes for successful call. Defaults to [200].
        """
        url = self._url_from_config(config_url_key, url_extra_path)
        response = self.put(url, data)
        if ok_status_codes is not None and response.status_code not in ok_status_codes:
            raise HTTPError(response=response)
        return response

    def cli_put_returning_json(
        self,
        config_url_key: str,
        url_extra_path: str,
        data: Union[str, dict],
        ok_status_codes: list = None,
    ) -> dict:
        """PUT the data to the given url.

        Args:
            config_url_key (str): key in configuration for the base path
            url_extra_path (str): extra path to add to the base path
            data (Union[str, dict]): data to send
            ok_status_codes (list, optional): accepted ok response codes. Defaults to None.

        Returns:
            dict: returned json
        """
        url = self._url_from_config(config_url_key, url_extra_path)
        return self.put_returning_json(url, data, ok_status_codes)
