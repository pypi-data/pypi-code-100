import re

import phonenumbers

from .logger import get_logger

# ref: https://stackoverflow.com/a/201378/8282345
EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""  # noqa: E501

logger = get_logger(__package__)


def is_valid_email(email: str) -> bool:
    try:
        return re.fullmatch(EMAIL_REGEX, email) is not None
    except Exception as exp:
        logger.error(f"Invalid email: {exp}")
        return False


def is_valid_phone_number(phone_number: str) -> bool:
    try:
        return phonenumbers.is_valid_number(phonenumbers.parse(phone_number))
    except Exception as exp:
        logger.error(f"Invalid phonenumber: {exp}")
        return False


__all__ = [
    "is_valid_email",
    "is_valid_phone_number",
]
