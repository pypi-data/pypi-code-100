import functools
import urllib.parse
from typing import List

import requests

from .conversion import serialize_match_request, deserialize_match
from .model import MatchRequest, Match
from ..restutil import prepare_url_for_relative_urljoin, ApiError


def match_bit_strings(base_url: str, request: MatchRequest) -> List[Match]:
    """
    Matches the bit strings contained within the request.

    :param base_url: URL at which the match service is hosted
    :param request: Match request
    :return: List of matched entities
    """
    if len(request.domain_bit_strings) == 0 or len(request.range_bit_strings) == 0:
        raise ValueError("Request must contain domain and range bit strings")

    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "match")
    r = requests.post(url, json=serialize_match_request(request))

    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.bad_request:
            raise ApiError("Invalid match parameters", r.status_code)

        raise ApiError("Couldn't match entities", r.status_code)

    result = r.json()

    return [
        deserialize_match(m) for m in result["correspondence-list"]
    ]


class MatchClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around all match client API functions.

        :param base_url: URL at which the match service is hosted
        """
        self.match_bit_strings = functools.partial(match_bit_strings, base_url)
