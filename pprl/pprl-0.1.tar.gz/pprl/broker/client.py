import functools
import urllib.parse
from typing import List

import requests

from .conversion import serialize_session_request, deserialize_match
from .model import SessionRequest, SessionResponse, BrokerMatch
from ..restutil import prepare_url_for_relative_urljoin, ApiError, append_auth_header


def create_session(base_url: str, request: SessionRequest) -> SessionResponse:
    """
    Creates a match session with the specified arguments.

    :param base_url: URL at which the broker service is hosted
    :param request: Session creation request
    :return: Response from the broker service as well as additional custom headers
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "session")

    r = requests.post(url, json=serialize_session_request(request))

    if r.status_code != requests.codes.created:
        raise ApiError("Session couldn't be created", r.status_code)

    response_obj = r.json()

    secret = response_obj["secret"]
    headers: dict[str, str] = {}

    # check for any custom headers
    for header_name, header_value in r.headers.items():
        if header_name.startswith("X-") or header_name.startswith("x-"):
            headers[header_name.lower()] = r.headers[header_name]

    return SessionResponse(secret, headers)


def get_results(base_url: str, secret: str) -> List[BrokerMatch]:
    """
    Returns match results from an ongoing match session.

    :param base_url: URL at which the broker service is hosted
    :param secret: Match session client secret
    :return: List of matches for that client
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "result")
    r = requests.get(url, headers=append_auth_header(secret))

    # check for 200
    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.unauthorized:
            raise ApiError("Client has not been registered at the broker", r.status_code)

        raise ApiError("Couldn't fetch results", r.status_code)

    return [deserialize_match(match) for match in r.json()["matches"]]


def get_progress(base_url: str, secret: str) -> float:
    """
    Returns the progress of an ongoing match session.

    :param base_url: URL at which the broker service is hosted
    :param secret: Match session secret
    :return: Match session progress (from 0 to 1)
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "progress")
    r = requests.get(url, headers=append_auth_header(secret))

    # check for 200
    if r.status_code != requests.codes.ok:
        if r.status_code == requests.codes.unauthorized:
            raise ApiError("Session has not been registered at the broker", r.status_code)

        raise ApiError("Couldn't fetch session progress", r.status_code)

    return float(r.json()["progress"])


def submit_bit_strings(base_url: str, secret: str, bit_strings: List[str]) -> str:
    """
    Submits bit strings to an ongoing match session.

    :param base_url: URL at which the broker service is hosted
    :param secret: Match session secret
    :param bit_strings: List of bit strings to submit
    :return: Match session client secret
    """
    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "submit")

    # create submission request object
    submit_request = {
        "bit-strings": [
            {
                "bit-string": s
            } for s in bit_strings
        ]
    }

    r = requests.post(url, json=submit_request, headers=append_auth_header(secret))

    # check for 202
    if r.status_code != requests.codes.accepted:
        if r.status_code == requests.codes.unauthorized:
            raise ApiError("Session has not been registered at the broker", r.status_code)

        raise ApiError("Entities couldn't be submitted", r.status_code)

    return str(r.json()["secret"])


def cancel_session(base_url: str, secret: str, headers: dict[str, str] = None):
    """
    Cancels an ongoing match session.

    :param base_url: URL at which the broker service is hosted
    :param secret: Match session secret
    :param headers: Additional headers required for cancellation
    """
    if headers is None:
        headers = {}

    base_url = prepare_url_for_relative_urljoin(base_url)
    url = urllib.parse.urljoin(base_url, "session")

    r = requests.delete(url, headers=append_auth_header(secret, headers))

    # check for 202
    if r.status_code != requests.codes.accepted:
        raise ApiError("Session couldn't be cancelled", r.status_code)


class BrokerClient:

    def __init__(self, base_url: str):
        """
        Creates a convenience wrapper around all broker client API functions.

        :param base_url: URL at which the broker service is hosted
        """
        self.create_session = functools.partial(create_session, base_url)
        self.cancel_session = functools.partial(cancel_session, base_url)
        self.get_progress = functools.partial(get_progress, base_url)
        self.get_results = functools.partial(get_results, base_url)
        self.submit_bit_strings = functools.partial(submit_bit_strings, base_url)
