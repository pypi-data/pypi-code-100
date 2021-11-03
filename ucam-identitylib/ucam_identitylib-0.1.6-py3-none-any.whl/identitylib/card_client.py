from typing import Any, Dict, Iterable, Mapping, Optional
from logging import getLogger

from identitylib.utils import chunks
from identitylib.api_client import IdentityAPIClient
from identitylib.identifiers import IdentifierScheme


LOG = getLogger(__name__)


class CardClient(IdentityAPIClient):
    """
    A client providing methods to efficiently query the Card API

    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = 'https://api.apps.cam.ac.uk/card/v1beta1/',
        token_url: str = 'https://api.apps.cam.ac.uk/oauth/client_credential/accesstoken',
        config: Optional[Mapping] = {},
    ):

        super(CardClient, self).__init__(
            client_id, client_secret, base_url, token_url, config
        )

    @staticmethod
    def get_identifier_by_scheme(card: Mapping, scheme: IdentifierScheme) -> Optional[str]:
        """
        Finds an identifier on the given card by the identifier scheme provided.
        Returns the identifier in full string form, i.e. `<value>@<scheme>`

        """

        return next(
            (
                f"{id['value']}@{str(scheme)}"
                for id in card['identifiers'] if id['scheme'] == str(scheme)
            ),
            None
        )

    def cards_for_identifiers(
        self, identifiers: Iterable[str], *,
        chunk_size: Optional[int] = 50, params: Optional[Dict[str, Any]] = {}
    ) -> Iterable[Mapping]:
        """
        Queries the Card API for the given list of identifiers. The query is made
        in batches in order to reduce load and therefore this method returns an
        iterator which will emit results as they are received.

        """

        for chunk in chunks(list(identifiers), chunk_size):
            yield from self._yield_paged_request(
                f'{self.base_url}/cards/filter/',
                self.session.post,
                json={'identifiers': chunk},
                params={'page_size': self.page_size, **params}
            )

    def all_cards(self, params: Optional[Dict[str, Any]] = {}) -> Iterable[Mapping]:
        """
        Queries the Card API for all cards, using the given params. Returns an iterator
        which will emit results as each page of cards is received.

        """
        return self._yield_paged_request(
            f'{self.base_url}/cards/',
            params={'page_size': self.page_size, **params}
        )

    def get_card_detail(self, card_uuid: str) -> Mapping:
        """
        Queries for the detail of a single card by UUID

        """
        request = self.session.get(f'{self.base_url}/cards/{card_uuid}/')
        request.raise_for_status()
        return request.json()
