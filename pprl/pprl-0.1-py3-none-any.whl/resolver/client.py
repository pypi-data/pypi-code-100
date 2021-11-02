import functools
from typing import List

import requests
from requests import Response

from .conversion import serialize_resolve_request, deserialize_pseudonym_match
from .model import ResolveRequest, PseudonymMatch
from ..restutil import append_auth_header, ApiError


def _try_raise_error(r: Response):
    """
    Tries to read an error message from a HTTP response to raise it as an instance of ``ApiError``.
    """
    try:
        data = r.json()
        error = data["error"]

        raise ApiError(f"Couldn't submit bit strings: {error}", r.status_code)
    except ValueError:
        raise ApiError(f"Couldn't submit bit strings: {r.text}", r.status_code)
    except KeyError:
        raise ApiError(f"Couldn't submit bit strings: {r.text}", r.status_code)


def submit_pseudonyms(base_url: str, secret: str, request: ResolveRequest):
    """
    Submits pseudonyms to a pseudonym resolver service.

    :param base_url: URL at which the pseudonym resolver service is hosted
    :param secret: Session secret obtained at the broker
    :param request: Request to send to pseudonym resolver
    """
    r = requests.post(base_url, json=serialize_resolve_request(request),
                      headers=append_auth_header(secret))

    if r.status_code >= 400:
        _try_raise_error(r)


def get_results(base_url: str, secret: str) -> List[PseudonymMatch]:
    """
    Retrieves results from a pseudonym resolver service.

    :param base_url: URL at which the pseudonym resolver service is hosted
    :param secret: Session secret obtained at the broker
    """
    r = requests.get(base_url, headers=append_auth_header(secret))

    if r.status_code >= 400:
        _try_raise_error(r)

    return [
        deserialize_pseudonym_match(match) for match in r.json()["matches"]
    ]


class ResolverClient:

    def __init__(self, base_url: str):
        self.submit_pseudonyms = functools.partial(submit_pseudonyms, base_url)
        self.get_results = functools.partial(get_results, base_url)
