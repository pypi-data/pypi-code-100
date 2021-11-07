import typing

import aiohttp

from . import models
from .core.api import ApiClient
from .core.auth import AuthManager
from .core.exceptions import ApiException
from .crud_objects import Branch, Customer, Location, StudyStatus, Subject, LeadStatus, LeadSource


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
        self.branch = Branch(self.api_client, model_class=models.Branch)
        self.location = Location(self.api_client, models.Location)
        self.customer = Customer(self.api_client, models.Customer)
        self.study_status = StudyStatus(self.api_client, models.StudyStatus)
        self.subject = Subject(self.api_client, models.Subject)
        self.lead_status = LeadStatus(self.api_client, models.LeadStatus)
        self.lead_source = LeadSource(self.api_client, models.LeadSource)

    @classmethod
    def _create_session(cls) -> aiohttp.ClientSession:
        """
        Create session
        :return: session
        """
        return aiohttp.ClientSession()

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
