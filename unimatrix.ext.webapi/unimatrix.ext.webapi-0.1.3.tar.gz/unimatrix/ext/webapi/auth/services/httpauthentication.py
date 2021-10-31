"""Declares :class:`HTTPAuthenticationService`."""
from unimatrix.ext import jose

from ..ihttpauthenticationservice import IHTTPAuthenticationService


class HTTPAuthenticationService(IHTTPAuthenticationService):

    async def resolve(self, bearer: bytes):
        """Decode JWT `bearer` and return the principal described by the
        claimset.
        """
        jws = await jose.payload(bearer)
        jws.verify()
        return jws.claims

