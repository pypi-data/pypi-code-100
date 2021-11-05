import ssl
import typing

import aiohttp
import certifi

from .core.api import ApiClient
from .core.auth import AuthManager
from .core.exceptions import ApiException
from .objects import Branch, Customer, Location, StudyStatus, Subject, LeadStatus, LeadSource


class AlfaClient:
    """Class for work with AlfaCRM API"""

    def __init__(
            self,
            hostname: str,
            email: str,
            api_key: str,
            branch_id: int,
            connections_limit: typing.Optional[int] = None,
            session: typing.Optional[aiohttp.ClientSession] = None,
    ):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._connector_init = dict(limit=connections_limit, ssl=ssl_context)
        self._connector_class: typing.Type[aiohttp.TCPConnector] = aiohttp.TCPConnector

        if session is None:
            session = self._create_session()

        self._hostname = hostname
        self._branch_id = branch_id
        self._session = session
        self._email = email
        self._api_key = api_key
        self.auth_manager = AuthManager(
            email,
            api_key,
            hostname,
            session,
        )

        self.api_client = ApiClient(
            self._hostname,
            self._branch_id,
            self.auth_manager,
            self._session,
        )

        # Set API objects
        self.branch = Branch(self.api_client)
        self.location = Location(self.api_client)
        self.customer = Customer(self.api_client)
        self.study_status = StudyStatus(self.api_client)
        self.subject = Subject(self.api_client)
        self.lead_status = LeadStatus(self.api_client)
        self.lead_source = LeadSource(self.api_client)

    def _create_session(self) -> aiohttp.ClientSession:
        """
        Create session
        :return: session
        """
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init),
        )

    async def auth(self):
        await self.auth_manager.refresh_token()

    async def check_auth(self) -> bool:
        """Check authentification"""
        try:
            await self.auth()
            return True
        except ApiException:
            return False

    async def close(self):
        """Close connections"""
        await self._session.close()

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def email(self) -> str:
        return self._email

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def branch_id(self) -> int:
        return self._branch_id
