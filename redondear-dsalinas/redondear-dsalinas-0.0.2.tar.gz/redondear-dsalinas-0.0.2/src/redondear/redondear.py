import decimal
from enum import Enum


class RoundType(Enum):
    ROUND_HALF_UP = 'ROUND_HALF_UP'
    ROUND_HALF_DOWN = 'ROUND_HALF_DOWN'
    ROUND_HALF_EVEN = 'ROUND_HALF_EVEN'


def round_number(
        number_str: str,
        places: int = 2,
        precision: int = 8,
        round_type: RoundType = RoundType.ROUND_HALF_EVEN
) -> str:
    """
        Round a number specifying the number of places and the type of rounding.
    :param number_str: Number to be rounded
    :param places: Number of digits after the decimal point
    :param precision: Calculation precision
    :param round_type: Type of rounding
    :return: Rounded number in string format
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
    :param number_str: number to be converted
    :param must_round: boolean field to indicate if the number must be rounded
    :return: Converted number in string format
    """
    cents = 0
    if must_round:
        rounded_number = round_number(number_str, 2)
        cents = int(decimal.Decimal(rounded_number) * decimal.Decimal('100'))
    else:
        cents = int(decimal.Decimal(number_str) * decimal.Decimal('100'))

    return str(cents)


def to_decimals(number_str: str) -> str:
    """
        Convert a number to decimals.
    :param number_str: Number to be converted
    :return: Converted number in string format
    """
    if number_str == '0':
        return '0.00'
    cents = decimal.Decimal(number_str) / decimal.Decimal('100')

    return str(cents)
