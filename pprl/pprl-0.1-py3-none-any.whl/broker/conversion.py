from .model import SessionCancellation, SessionRequest, BrokerMatch
from ..match.conversion import serialize_match_config


def serialize_session_cancellation(cancel: SessionCancellation) -> dict:
    """
    Converts a session cancellation object into a dictionary.

    :param cancel: Object to convert
    :return: Converted session cancellation
    """
    d = {"method": cancel.method}

    for k, v in cancel.options.items():
        d[str(k)] = str(v)

    return d


def serialize_session_request(request: SessionRequest) -> dict:
    """
    Converts a session request object into a dictionary.

    :param request: Object to convert
    :return: Converted session request
    """
    return {
        "match-configuration": serialize_match_config(request.match_config),
        "session-cancellation": serialize_session_cancellation(request.session_cancellation)
    }


def deserialize_match(d: dict) -> BrokerMatch:
    """
    Converts a dictionary into a match object.

    :param d: Dictionary to convert
    :return: Converted dictionary
    """
    return BrokerMatch(d["bit-string"], d["confidence"])
