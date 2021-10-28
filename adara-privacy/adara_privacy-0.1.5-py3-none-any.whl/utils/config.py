import os
import json
import requests
import datetime

from adara_privacy.exceptions import (
    MissingEnvironmentVariableError,
    MissingRequiredSettingError,
    InvalidConfigurationFormatError,
)

CONFIG_ENVIRONMENT_VARIABLE = 'ADARA_SDK_CREDENTIALS'

# top-level config keys
CONFIG_KEY_CLIENT_ID = 'client_id'
CONFIG_KEY_CLIENT_SECRET = 'client_secret'
CONFIG_KEY_AUTH_URI = 'auth_uri'

# privacy config keys
CONFIG_KEY_PRIVACY = 'privacy'  # section key

CONFIG_KEY_PRIVATE_SALT = 'private_salt'
CONFIG_KEY_TRANSMIT_ROOT_TOKEN = 'transmit_root_token'
CONFIG_KEY_COMMON_SALT = 'common_salt'
CONFIG_KEY_COMMON_SALTS = 'common_salts'
CONFIG_KEY_AUDIENCE_URI = 'audience_uri'
CONFIG_KEY_PIPELINE_ID = 'pipeline_id'
CONFIG_KEY_IGNORE_EMPTY_IDENTIFIERS = 'ignore_empty_identifiers'

# reserved value names
RESERVED_PRIVATE = 'private'
RESERVED_COMMON = 'common'
RESERVED_TYPE = 'type'
RESERVED_LABEL = 'label'


def _get_config_keys(keys: list, config: dict) -> dict:
    result = dict()
    sought_keys = {k.strip().lower() for k in keys}
    for k in config.keys():
        key = k.strip().lower()
        if key in sought_keys:
            result[key] = config[k]

    return result


class PrivacyConfig():
    def __init__(self, parent_config, config_data: dict, *args, **kwargs):
        super().__init__()

        if not isinstance(config_data, dict):
            raise TypeError('Privacy configuration module must be a dictionary.')

        config = _get_config_keys([
            CONFIG_KEY_PRIVATE_SALT,
            CONFIG_KEY_TRANSMIT_ROOT_TOKEN,
            CONFIG_KEY_COMMON_SALT,
            CONFIG_KEY_COMMON_SALTS,
            CONFIG_KEY_AUDIENCE_URI,
            CONFIG_KEY_PIPELINE_ID,
        ], config_data)

        # REQUIRED: Private Salt setting
        try:
            self._private_salt = config[CONFIG_KEY_PRIVATE_SALT]
        except KeyError:
            raise MissingRequiredSettingError(CONFIG_KEY_PRIVATE_SALT) from None

        # OPTIONAL: Transmit root token setting
        try:
            self._transmit_root_token = config[CONFIG_KEY_TRANSMIT_ROOT_TOKEN]
        except KeyError:
            # defaults to False (do not transmit root token)
            self._transmit_root_token = False

        self._common_salts = dict()
        # OPTIONAL: Common Salt setting
        # NOTE: This provides backward functionality to a single "common_salt" key; this is
        # deprecated with the introduction of an arbitrary number of named salts
        # TODO: REMOVE THIS!
        try:
            self._common_salts[RESERVED_COMMON] = config[CONFIG_KEY_COMMON_SALT]
        except KeyError:
            pass

        # OPTIONAL: Named Salts
        try:
            salts = config[CONFIG_KEY_COMMON_SALTS]
            assert isinstance(salts, dict)
            assert all(isinstance(salts[k], str) and k.strip().lower() != RESERVED_PRIVATE for k in salts)
            self._common_salts.update(salts)
        except KeyError:
            pass
        except AssertionError:
            raise TypeError(f'Configuration key "{CONFIG_KEY_COMMON_SALTS}" must contain a dictionary of key/value string pairs.')

        # OPTIONAL: Audience URI setting
        try:
            self._audience_uri = config[CONFIG_KEY_AUDIENCE_URI]
        except KeyError:
            self._audience_uri = None

        # OPTIONAL: Pipeline ID setting
        try:
            self._pipeline_id = config[CONFIG_KEY_PIPELINE_ID]
        except KeyError:
            self._pipeline_id = None

        # OPTIONAL: Ignore empty identifiers setting
        try:
            self._ignore_empty_identifiers = config[CONFIG_KEY_IGNORE_EMPTY_IDENTIFIERS]
        except KeyError:
            self._ignore_empty_identifiers = True

        self._parent_config = parent_config
        self._access_token = None
        self._access_token_expiry = None

    @property
    def private_salt(self):
        return self._private_salt

    @property
    def transmit_root_token(self):
        return self._transmit_root_token

    @property
    def common_salts(self):
        return self._common_salts

    @property
    def audience_uri(self):
        return self._audience_uri

    @property
    def pipeline_id(self):
        return self._pipeline_id

    @property
    def ignore_empty_identifiers(self):
        return self._ignore_empty_identifiers

    def _get_access_token(self):
        r = requests.post(
            self._parent_config.auth_uri,
            json=dict(
                client_id=self._parent_config.client_id,
                client_secret=self._parent_config.client_secret,
                audience=self._parent_config.privacy.audience_uri,
                grant_type="client_credentials"
            )
        )
        r_json = r.json()
        self._access_token = r_json['access_token']
        self._access_token_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=r_json['expires_in'] - 300)

    @property
    def privacy_api_access_token(self):
        if (not self._access_token) or (not self._access_token_expiry) or (
                isinstance(self._access_token_expiry, datetime.datetime) and datetime.datetime.utcnow() >= self._access_token_expiry):
            self._get_access_token()
        return self._access_token


class Config():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self._path = os.environ[CONFIG_ENVIRONMENT_VARIABLE]
        except KeyError as e:
            raise MissingEnvironmentVariableError() from None

        # read in the local file - must be valid json
        try:
            with open(self._path) as f:
                config_data = json.load(f)
        except FileNotFoundError as e:
            raise e from None
        except json.decoder.JSONDecodeError as e:
            raise InvalidConfigurationFormatError() from None
        except Exception as e:
            raise e from None

        # now parse out the settings
        config = _get_config_keys([
            CONFIG_KEY_CLIENT_ID,
            CONFIG_KEY_CLIENT_SECRET,
            CONFIG_KEY_AUTH_URI,
            CONFIG_KEY_PRIVACY,
        ], config_data)

        # OPTIONAL: Client ID
        try:
            self._client_id = config[CONFIG_KEY_CLIENT_ID]
        except KeyError:
            self._client_id = None

        # OPTIONAL: Client Secret
        try:
            self._client_secret = config[CONFIG_KEY_CLIENT_SECRET]
        except KeyError:
            self._client_secret = None

        # OPTIONAL: Authorization URI
        try:
            self._auth_uri = config[CONFIG_KEY_AUTH_URI]
        except KeyError:
            self._auth_uri = None

        # OPTIONAL: Privacy (config section)
        try:
            self._privacy = PrivacyConfig(self, config[CONFIG_KEY_PRIVACY])
        except KeyError:
            self._privacy = None

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def auth_uri(self):
        return self._auth_uri

    @property
    def privacy(self):
        return self._privacy
