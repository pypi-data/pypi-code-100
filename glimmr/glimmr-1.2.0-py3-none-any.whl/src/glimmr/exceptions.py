"""Exceptions for GLIMMR."""


class GlimmrError(Exception):
    """Generic GLIMMR exception."""


class GlimmrEmptyResponseError(Exception):
    """GLIMMR empty API response exception."""


class GlimmrConnectionError(GlimmrError):
    """GLIMMR connection exception."""


class GlimmrRConnectionTimeoutError(GlimmrConnectionError):
    """GLIMMR connection Timeout exception."""


class GlimmrRConnectionClosed(GlimmrConnectionError):
    """GLIMMR WebSocket connection has been closed."""
