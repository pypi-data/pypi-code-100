import functools
import urllib.parse
from typing import List

import requests

from .conversion import serialize_encoder_request, deserialize_encoded_entity
from .model import EncoderRequest, EncodedEntity
from ..restutil import prepare_url_for_relative_urljoin, ApiError


def get_version(base_url: str) -> tuple[int]:
    """
    Gets the version of the encoder service hosted at the specified URL.

    :param base_url: URL at which the encoder service is hosted
    :return: Tuple of integers representing the running version
    """
    r = requests.get(base_url)
    r.raise_for_status()

    version_num = r.json()["version"][1:].split(".")
    return tuple([int(v) for v in version_num])


def encode_entities(base_url: str, request: EncoderRequest, force_include_schema=False) -> List[EncodedEntity]:
    """
    Encodes the entities contained within the request with the specified encoder configuration.
    Attribute schemas will be added to the request if present.
    Make sure that the service you're connecting to supports attribute schemas before running an encoder request.

    :param base_url: URL at which the encoder service is hosted
    :param request: Encoder request
    :param force_include_schema: ``True`` if attribute schemas should be generated even if none are specified,
    ``False`` otherwise
    :return: List of encoded entities
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "encode")
    request = serialize_encoder_request(request, force_include_schema)

    r = requests.post(url, json=request)

    # check for 200
    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.bad_request:
            raise ApiError("Invalid encoder parameters", r.status_code)

        raise ApiError("Couldn't encode entities", r.status_code)

    result = r.json()

    if "entity-list" not in result:
        raise ApiError("Response content is malformed", requests.codes.bad_gateway)

    return [
        deserialize_encoded_entity(e) for e in result["entity-list"]
    ]


class EncoderClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around all encoder client API functions.

        :param base_url: URL at which the encoder service is hosted
        """
        self.version = get_version(base_url)

        if self.version >= (0, 2):
            self.encode_entities = functools.partial(encode_entities, base_url, force_include_schema=True)
        else:
            self.encode_entities = functools.partial(encode_entities, base_url, force_include_schema=False)
