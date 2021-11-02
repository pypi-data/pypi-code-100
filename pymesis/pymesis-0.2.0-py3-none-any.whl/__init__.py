"""Memoization for Python, with optional TTL (measured in time or function call count)."""


__author__ = "Daniel Hjertholm"
__version__ = "0.2.0"


from .pymesis import TTLUnit, _cache, memoize  # noqa: F401

__all__ = (memoize, TTLUnit)
