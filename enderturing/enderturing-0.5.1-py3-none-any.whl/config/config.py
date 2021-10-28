from __future__ import annotations

import os

from dataclasses import dataclass

from enderturing.config.config_utils import _init_config_from_url, _str2bool


ENV_ET_URL = "ET_URL"
ENV_ET_AUTH_KEY = "ET_AUTH_KEY"
ENV_ET_AUTH_SECRET = "ET_AUTH_SECRET"
ENV_ET_API_VERSION = "ET_API_VERSION"
ENV_ET_SSL_VERIFY = "ET_SSL_VERIFY"


@dataclass
class Config:
    """Configuration for :class:`enderturing.EnderTuring`.
    Contains settings for API access.

    Attributes:
        auth_key: Login to use for API access.
        auth_secret: Password to use for API access.
        url: EnderTuring installation URL
        api_version: API version to use. For now only "v1" is supported
        ssl_verify: Allows to disable SSL certificate checks (ssl_verify=False). Useful if installation uses
            self-signed certificates.

    """

    auth_key: str = None
    auth_secret: str = None
    url: str = "https://local.enderturing.com/"
    api_version: str = "v1"
    ssl_verify: bool = False

    @classmethod
    def from_url(cls, ender_url: str) -> Config:
        """Creates `Config` from a URL.

        Args:
            ender_url: URL with all required options. Example:
                https://admin%40local.enderturing.com:My_password@local.enderturing.com/?ssl_verify=false

        Returns:
            Initialized `Config` instance.
        """
        return _init_config_from_url(Config(), ender_url)

    @classmethod
    def from_env(cls):
        """Creates `Config` from environment variables.
        Supported variables:
        - ET_URL: Ender Turing URL. Can be either just installation URL (e.g. https://local.enderturing.com/) or
          can contain other parameters
          (e.g. https://admin%40local.enderturing.com:My_password@local.enderturing.com/?ssl_verify=false).
          If parameters are set in the URL and as a separate variables - separate variables for parameters have higher
          priority.
        - ET_AUTH_KEY: Value of `auth_key`
        - ET_AUTH_SECRET: Value of `auth_secret`
        - ET_API_VERSION: Value of `api_version`
        - ET_SSL_VERIFY: Value of `ssl_verify`

        Returns:
            Initialized `Config` instance.
        """
        ender_url = os.getenv(ENV_ET_URL)
        config = cls.from_url(ender_url)
        if os.getenv(ENV_ET_AUTH_KEY):
            config.auth_key = os.getenv(ENV_ET_AUTH_KEY)
        if os.getenv(ENV_ET_AUTH_SECRET):
            config.auth_secret = os.getenv(ENV_ET_AUTH_SECRET)
        if os.getenv(ENV_ET_API_VERSION):
            config.api_version = os.getenv(ENV_ET_API_VERSION)
        if os.getenv(ENV_ET_SSL_VERIFY):
            config.ssl_verify = _str2bool(os.getenv(ENV_ET_SSL_VERIFY))
        return config
