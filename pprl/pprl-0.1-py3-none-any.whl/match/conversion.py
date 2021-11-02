from .model import MatchConfig, MatchRequest, Match


def serialize_match_config(config: MatchConfig) -> dict:
    """
    Converts a match configuration object into a dictionary.

    :param config: Match configuration to convert
    :return: Converted match configuration
    """
    return {
        "match-function": config.match_function,
        "selection-strategy": config.selection_strategy,
        "threshold": str(config.threshold)
    }


def serialize_bit_string(bit_string: str) -> dict:
    """
    Converts a bit string into a dictionary.

    :param bit_string: Bit string to convert
    :return: Converted bit string
    """
    return {
        "bit-string": bit_string
    }


def serialize_match_request(request: MatchRequest) -> dict:
    """
    Converts a match request into a dictionary.

    :param request: Match request object to convert
    :return: Converted match request
    """
    return {
        "domain-entity-list": [
            serialize_bit_string(d) for d in request.domain_bit_strings
        ],
        "range-entity-list": [
            serialize_bit_string(r) for r in request.range_bit_strings
        ],
        "match-configuration": serialize_match_config(request.match_config)
    }


def deserialize_match(d: dict) -> Match:
    """
    Converts a match dictionary into a match object.

    :param d: Dictionary to convert
    :return: Converted dictionary
    """
    return Match(
        domain_bit_string=d["domain-bit-string"],
        range_bit_string=d["range-bit-string"],
        confidence=d["confidence"]
    )
