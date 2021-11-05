"""
Read a pins v1 pinned data set from RStudio Connect
"""

import json
import pandas
import requests
import tempfile


class NotAValidConnectServerError(Exception):
    """
    Throw an error if we don't find a valid Connect server instance
    """

    def __init__(
        self,
        message="Not a valid RStudio Connect instance. Check the URL and try again.",
    ):
        self.message = message
        super().__init__(self.message)


class AmbiguousUsernameError(Exception):
    """
    Throw an error if there's a problem with the username
    """

    def __init__(
        self,
        message="Ambiguous username (too many results). Check the username and try again.",
    ):
        self.message = message
        super().__init__(self.message)


class PinURLNotFoundError(Exception):
    """
    Throw an error if there's a problem with the pin name
    """

    def __init__(
        self,
        message="Pin not found. Check the pin name and try again.",
    ):
        self.message = message
        super().__init__(self.message)


class VersionMismatchError(Exception):
    """
    Throw an error if the version doesn't match
    """

    def __init__(
        self,
        message="Expected pins api version 1.0.",
    ):
        self.message = message
        super().__init__(self.message)


class SupportedTypeError(Exception):
    """
    Throw an error if the type is not supported
    """

    def __init__(
        self,
        message="pin data type not supported",
    ):
        self.message = message
        super().__init__(self.message)


def _is_connect_url(url):
    """
    Checks that the Connect URL is valid.
    """
    try:
        response = requests.get("{}/__ping__".format(url))
    except Exception:
        return False
    if response.status_code == 200:
        return True
    else:
        return False


def _get_user_guid(server, api_key, username):
    api_key_str = "key {}".format(api_key)
    headers = {"Authorization": api_key_str}

    api_user = requests.get(
        "{}/__api__/v1/users?prefix={}".format(server, username), headers=headers
    )
    user_data = json.loads(api_user.text)
    if len(user_data["results"]) > 1:
        raise AmbiguousUsernameError
    else:
        return user_data["results"][0]["guid"]


def _get_pin_url(server, api_key, user_guid, pin_name):
    api_key_str = "key {}".format(api_key)
    headers = {"Authorization": api_key_str}

    params = {"owner_guid": user_guid, "name": pin_name}

    api_user = requests.get(
        "{}/__api__/v1/content".format(server), headers=headers, params=params
    )
    content_data = json.loads(api_user.text)
    try:
        content_url = content_data[0]["content_url"]
    except IndexError:
        raise PinURLNotFoundError

    return content_url


def _get_pin_meta(pin_url, api_key):
    """
    Returns a dict
    """
    api_key_str = "key {}".format(api_key)
    headers = {"Authorization": api_key_str}

    api_pin_meta = requests.get("{}/data.txt".format(pin_url), headers=headers)
    metadata_raw = api_pin_meta.text
    print(metadata_raw)
    metadata_lines = metadata_raw.splitlines()
    print(metadata_lines)
    metadata = dict(
        (x.strip(), y.strip())
        for x, y in (line.split(": ", 1) for line in metadata_lines)
    )
    return metadata


def _pin_read(pin_url, api_key, metadata):
    """
    Gets the data from the server and crams it into memory
    """
    api_key_str = "key {}".format(api_key)
    headers = {"Authorization": api_key_str}

    if metadata["api_version"] != "1.0":
        raise VersionMismatchError

    if metadata["type"] != "csv":
        raise SupportedTypeError

    pins_tf = tempfile.NamedTemporaryFile()
    api_pin_data = requests.get(
        "{}/{}".format(pin_url, metadata["file"]), headers=headers
    )
    with open(pins_tf.name, "w") as f:
        f.write(api_pin_data.text)

    return pandas.read_csv(pins_tf)


def pin_read_v1_conect(server, api_key, pin_name, meta_only=False):
    """
    Read a v1 pin from an RStudio Connect instance

    Attributes:
        server -- a valid Connect instance URL
        api_key -- a working Connect API key
        pin -- the name of a pin on the Connect instance in the username/pin_name format
        meta_only -- controls whether only pin metadata is returned (default: False)
    """
    if _is_connect_url(server) is not True:
        raise NotAValidConnectServerError

    try:
        pin_parts = pin_name.split("/")
    except IndexError as err:
        print(err)
        print("Error: you must supply the pin name in the username/pin_name format")

    user = pin_parts[0]
    pin = pin_parts[1]

    user_guid = _get_user_guid(server, api_key, user)

    pin_url = _get_pin_url(server, api_key, user_guid, pin)

    metadata = _get_pin_meta(pin_url, api_key)

    if meta_only is True:
        return metadata

    pin_data = _pin_read(pin_url, api_key, metadata)

    return pin_data
