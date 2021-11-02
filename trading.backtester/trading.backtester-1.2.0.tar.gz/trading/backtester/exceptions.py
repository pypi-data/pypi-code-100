"""Module containing custom errors for the backtester."""


__all__ = [
    # Class exports
    "BacktesterException",
    "InsufficientBalanceError",
    "InsufficientPositionAmountError",
]


class BacktesterException(Exception):
    """Base exception for any backtester-related issues."""


class InsufficientBalanceError(BacktesterException):
    """Raised when there's not enough balance in the exchange."""
