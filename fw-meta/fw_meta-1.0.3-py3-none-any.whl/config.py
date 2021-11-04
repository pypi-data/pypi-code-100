"""Metadata configuration."""
import functools

try:
    import zoneinfo
except ImportError:  # pragma: no cover
    from backports import zoneinfo  # type: ignore

import tzlocal


@functools.lru_cache()
def tz() -> zoneinfo.ZoneInfo:
    """Return timezone to parse naive timestamps with."""
    return tzlocal.reload_localzone()  # type: ignore
