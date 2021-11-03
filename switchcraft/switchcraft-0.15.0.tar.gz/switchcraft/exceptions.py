"""Switchcraft Exceptions.

All custom exceptions for Switchcraft must be defined here.
"""


class SwitchcraftException(Exception):
    """All custom exceptions must inherit this class."""

    pass


class MalformedArnError(SwitchcraftException):
    """Raised when an ARN is malformed."""

    pass
