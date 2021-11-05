"""Skaha Client."""
from os import environ
from pathlib import Path
from platform import machine, platform, python_version, release, system
from time import asctime, gmtime

from attr import attrib, attrs
from requests import Session
from validators import url

from skaha import __version__
from skaha.exceptions import InvalidCertificateError, InvalidServerURL


@attrs
class SkahaClient(Session):
    """SkahaClient is the base class for all other API clients.

    Args:
        Session (requests.Session): Requests Session Object.

    Raises:
        InvalidServerURL: If the server URL is invalid.
        InvalidCertificateError: If the client is given an invalid certificate.

    Examples:
        >>> from skaha.client import SkahaClient
            class MyClient(SkahaClient):
                pass

    """

    server = attrib(default="https://ws-uv.canfar.net/skaha")
    certificate = attrib(
        default="{HOME}/.ssl/cadcproxy.pem".format(HOME=environ["HOME"]), type=str
    )
    timeout = attrib(default=15, type=int)

    def __attrs_pre_init__(self):
        """Intialize Session Object."""
        super().__init__()

    @server.validator
    def _check_server(self, attribute, value):
        """Check if server is a valid url."""
        if not url(value):
            raise InvalidServerURL("Server must be a valid URL.")
        self.headers.update({"X-Skaha-Server": value})

    @certificate.validator
    def _check_certificate(self, attribute, value):
        """Check the certificate."""
        if not Path(value).is_absolute():
            raise InvalidCertificateError("certificate must be an absolute path.")
        if not Path(value).is_file():
            raise InvalidCertificateError(f"{value} does not exist.")
        self.headers.update({"X-Skaha-Authentication-Type": "certificate"})
        self.cert = value
        self.verify = True

    def __attrs_post_init__(self):
        """Post Intialization Attributes."""
        self.headers.update({"Content-Type": "application/json"})
        self.headers.update({"Accept": "*/*"})
        self.headers.update({"User-Agent": "skaha-client"})
        self.headers.update({"Date": asctime(gmtime())})
        self.headers.update({"X-Skaha-Version": __version__})
        self.headers.update({"X-Skaha-Client-Python-Version": python_version()})
        self.headers.update({"X-Skaha-Client-Arch": machine()})
        self.headers.update({"X-Skaha-Client-OS": system()})
        self.headers.update({"X-Skaha-Client-OS-Version": release()})
        self.headers.update({"X-Skaha-Client-Platform": platform()})
