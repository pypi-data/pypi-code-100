"""Conversion.

Utility functions that assist with common (or helpful) conversions.
"""
import logging
import re

log = logging.getLogger(__name__)


def underscore_to_camelcase(name: str) -> str:
    """Converts a string (snakecase) containing underscores to camelCase."""
    under_pat = re.compile(r'_([a-z])')
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def param_list_to_dict(params: list) -> dict:
    """Converts AWS response objects to dicts. Many APIs return tags and other
    data objects in the following format:

    [{'Key': 'hello', 'Value': 'world'}, {'Key': 'hi', 'Value': 'there'}]

    This function converts the list of key-value pairs to a simple
    Python dictionary, making it much easier to parse.

    Example Output:
    {
        'hello': 'world',
        'hi': 'there'
    }
    """

    if params is None:
        return dict()
    else:
        return dict((el['Key'], el['Value']) for el in params)
