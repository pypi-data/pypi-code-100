from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, DivisionByZero


def _proportion(base: float, target: float, round_number: str) -> Decimal:
    """baseとtargetの比率
    計算式: (target - base) / abs(base)
    """
    numerator = Decimal(str(target)) - Decimal(str(base))
    denominator = Decimal(str(base)).copy_abs()
    # return float((numerator / denominator * 100).quantize(Decimal(round_number), ROUND_HALF_UP))
    return numerator / denominator


def _to_float(d: Decimal, round_number: str) -> float:
    return float(d.quantize(Decimal(round_number), ROUND_HALF_UP))


def proportion(base: float, target: float, round_number: str = '0.01') -> float:
    """baseに対してtargetの比率
    前日終値100円に対し今日の終値99円だと-1%
    Example:
        >>> proportion(100, 99)
        -1.0
        >>> proportion(203, 7)
        -96.55
    """
    try:
        p = _proportion(base, target, round_number)
        return _to_float(p * 100, round_number)
    except (InvalidOperation, ZeroDivisionError):
        return float('nan')


def progress_rate(goal: float, progress: float, round_number: str = '0.01') -> float:
    """goalに対して現在(progress)の達成率
    Example:
        >>> progress_rate(50, 40)
        80.0
        >>> progress_rate(50, 12.031454, '0.00001')
        24.06291
    """
    if goal == 0:
        return float('nan')
    try:
        p = _proportion(goal, progress, round_number)
        return _to_float((Decimal('1') + p) * 100, round_number)
    except (InvalidOperation, ZeroDivisionError):
        return float('nan')
