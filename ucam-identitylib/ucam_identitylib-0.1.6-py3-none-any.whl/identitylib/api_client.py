from typing import Callable, Optional, Mapping
from functools import lru_cache
from logging import getLogger
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests import auth


LOG = getLogger(__name__)


class IdentityAPIClient:
    """
    A client providing methods to query identity related APIs

    """

    def __init__(
        self, client_id, client_secret, base_url, token_url,
        config: Optional[Mapping] = {},
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url.rstrip('/')
        self.token_url = token_url
        self.page_size = int(config.get('page_size', 200))

    @property
    @lru_cache()
    def session(self):
        """
        Lazy-init a OAuth2-wrapped session and fetch a token before it's used.

        """

        client = BackendApplicationClient(client_id=self.client_id)
        session = OAuth2Session(client=client)

        session.fetch_token(
            token_url=self.token_url,
            auth=auth.HTTPBasicAuth(self.client_id, self.client_secret)
        )
        return session

    def _yield_paged_request(
        self,
        url: str,
        request_method: Optional[Callable] = None,
        **kwargs
    ):
        """
        Utility method allowing DRF pages to be walked through with results being emitted
        through the returned iterator.

        """
        request_method = self.session.get if not request_method else request_method

        def make_request(target_url: str, **request_kwargs):
            request = request_method(target_url, timeout=(2, 20), **request_kwargs)
            request.raise_for_status()

            data = request.json()
            return data.get('results', []), data.get('next')

        results, next_url = make_request(url, **kwargs)
        yield from results

        while next_url:
            results, next_url = make_request(next_url)
            yield from results
