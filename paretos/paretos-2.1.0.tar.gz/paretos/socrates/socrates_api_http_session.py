from logging import Logger, LoggerAdapter
from typing import Union

from ..authentication.access_token_provider import AccessTokenProvider
from ..service.api_http_session import ApiHttpSession


class SocratesApiHttpSession(ApiHttpSession):
    def __init__(
        self,
        api_url: str,
        access_token_provider: AccessTokenProvider,
        logger: Union[Logger, LoggerAdapter],
    ):
        super(SocratesApiHttpSession, self).__init__(
            api_url=api_url,
            api_name='Socrates Api',
            access_token_provider=access_token_provider,
            logger=logger
        )
