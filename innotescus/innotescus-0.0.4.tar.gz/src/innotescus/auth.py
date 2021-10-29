from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc6749 import OAuth2Token

from innotescus.helpers import ttl_cache_from_dict_result


class InnoAuthClient:
    """ Exchanges a client_id and client_secret for an `OAuth2Token`.
    """
    def __init__(self, client_id: str, client_secret: str, scope: str, audience: str, auth_domain: str):
        """
        :param `str` client_id: Client-specific identifier generated from Innotescus admin.
        :param `str` client_secret: Client-specific secret key generated from Innotescus admin.
        :param `str` scope: OAuth2 scope parameter.
        :param `str` audience: OAuth2 audience parameter.
        :param `str` auth_domain: Domain used to fetch token.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.token_endpoint = f'https://{auth_domain}/oauth/token'
        self.audience = audience

    @ttl_cache_from_dict_result
    def fetch_access_token(self) -> OAuth2Token:
        """ Authorizes an oauth session and returns the access
        data.  **Note** if successful, the token will be cached until
        the expiry time of the token -- you should call this method
        whenever needed, instead of saving the result elsewhere.

        :rtype: `OAuth2Token`
        :return: A dictionary containing authorization info.
        """
        client = OAuth2Session(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            audience=self.audience
        )

        return client.fetch_token(
            self.token_endpoint,
            grant_type='client_credentials',
            audience=self.audience
        )
