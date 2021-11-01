import decimal
from enum import Enum


class RoundType(Enum):
    ROUND_HALF_UP = 'ROUND_HALF_UP'
    ROUND_HALF_DOWN = 'ROUND_HALF_DOWN'
    ROUND_HALF_EVEN = 'ROUND_HALF_EVEN'
    ROUND_HALF_ODD = 'ROUND_HALF_ODD'


def round_number(
        number_str: str,
        places: int = 2,
        precision: int = 8,
        round_type: RoundType = RoundType.ROUND_HALF_EVEN
) -> str:
    """
        Round a number to a given number of decimals.
    """
    places_str = f"1.{'0' * places}"
    decimal.getcontext().prec = precision
    if round_type == RoundType.ROUND_HALF_UP:
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
    elif round_type == RoundType.ROUND_HALF_DOWN:
        decimal.getcontext().rounding = decimal.ROUND_HALF_DOWN
    elif round_type == RoundType.ROUND_HALF_EVEN:
        decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
    else:
        decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN

    rounded_decimal_number = decimal.Decimal(number_str).quantize(decimal.Decimal(places_str))

    return str(rounded_decimal_number)


def to_cents(number_str: str, must_round: bool = True) -> str:
    """
        Convert a number to cents.
    """
    cents = 0
    if must_round:
        rounded_number = round_number(number_str, 2)
        cents = int(decimal.Decimal(rounded_number) * decimal.Decimal('100'))
    else:
        cents = int(decimal.Decimal(number_str) * decimal.Decimal('100'))

    return str(cents)


def to_decimals(number_str: str) -> str:
    if number_str == '0':
        return '0.00'
    cents = decimal.Decimal(number_str) / decimal.Decimal('100')

    return str(cents)
