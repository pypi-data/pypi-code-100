
class ConnectionError(Exception):
    """Raised when connceting to jarvis for the first time fails."""


class APIRequestFailed(Exception):
    """Raised when trying to call an api endpoint fails."""


class InvalidMethod(Exception):
    """Rasied when you're attempting to send an API request with an invalid method."""


class UnknownServerError(Exception):
    """Raised when an error gets thrown in the server side but it's unknown. Highly unlikely to get raised."""


class APIKeyError(Exception):
    """Raised when the API key provided is not valid or there's no API key at all."""
