EMPTY_VALUES = {
    '',
    'null',
    'none',
    '0',
    '-',
    'na',
    'n/a',
}


def is_stringable(value) -> str:
    return isinstance(value, (str, int, float))


def is_empty_string(s: str) -> str:
    return not s or s.strip().lower() in EMPTY_VALUES


def identifiers_as_single_str(*args: str) -> str:
    """
    Private function for standardizing string coalescence for multi-value tokenization routines.

    Returns:
        str: Returns the single string output
    """
    return ':'.join(sorted(arg.strip().lower() for arg in args))
