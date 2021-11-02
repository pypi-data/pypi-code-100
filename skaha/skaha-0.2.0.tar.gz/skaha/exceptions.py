"""Skaha Exceptions."""


# API Errors from HTTP Status Codes
class APIError(Exception):
    """Errors raised as a result of HTTP Status Codes."""

    pass


class NotAuthenticated(APIError):
    """Not Authenticated."""

    pass


class PermissionDeniedError(APIError):
    """Permission Denied."""

    pass


class InternalError(APIError):
    """Internal Server Error."""

    pass


class ServiceBusyError(APIError):
    """Service Busy."""

    pass


class ConnectionError(APIError):
    """Connection Error."""

    pass


# Client Errors


class ClientError(Exception):
    """Skaha Client Errors."""

    pass


class InvalidServerURL(ClientError):
    """Invalid Server URL."""

    pass


class InvalidCertificateError(ClientError):
    """Invalid Certificate."""

    pass


class ParameterError(ClientError):
    """Invalid Parameters."""

    pass


class UnknownError(ClientError):
    """Unknown Error."""

    pass
