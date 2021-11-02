"""
Python SDK for accessing Skytap APIs
"""
from restfly.session import APISession

from .users import Users


class Skytap(APISession):
    """
    A controller to access Endpoints in the Skytap API.

    KWARG Options:
        username (str): Skytap Username
        password (str): Skytap password
        token (str): API Token from Skytap.
        api_version (int): Default to 1 but can be 2.
    """

    _url = "https://cloud.skytap.com"

    def _authenticate(self, **kwargs) -> None:
        """Create a session to Skytap API."""
        api_version = kwargs.pop("api_version", 1)
        username = kwargs.pop("username", None)
        password = kwargs.pop("password", None)
        token = kwargs.pop("token", None)

        if username:
            if token:
                self._session.auth = (username, token)
            elif password:
                self._session.auth = (username, password)
            else:
                self._log.warn(
                    "Token or Password is required for authentication.  Starting unauthenticated session."
                )
        else:
            self._log.warn(
                "Username is required for authentication.  Starting unauthenticated session."
            )
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        if api_version == 2:
            self._session.headers.update(
                {"Accept": "application/vnd.skytap.api.v2+json"}
            )

    def _deauthenticate(self):
        """Ends the authentication session."""
        self._session.auth = None

    @property
    def users(self):
        """Call Users Class"""
        return Users(self)
