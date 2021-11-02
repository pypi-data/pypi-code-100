"""Module containing position constants."""

__all__ = [
    # Constants export
    "LONG",
    "SHORT",
]

LONG = "long"
SHORT = "short"


def is_valid_position(input_position: str) -> bool:
    return input_position in (LONG, SHORT)


def get_position_multiplier(input_position: str) -> int:
    return {LONG: 1, SHORT: -1}.get(input_position, 1)
