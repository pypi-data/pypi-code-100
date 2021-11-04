from logging import Logger

from paretos.app.run import run
from paretos.socrates.socrates_api_http_session import SocratesApiHttpSession


class ShowDashboardHandler:
    def __init__(
        self,
        logger: Logger,
        dashboard_host: str,
        dashboard_port: str,
        api_session: SocratesApiHttpSession,
    ):
        self.__logger = logger
        self.__dashboard_host = dashboard_host
        self.__dashboard_port = dashboard_port
        self.__api_session = api_session

    def show(self) -> None:
        run(
            api_session=self.__api_session,
            logger=self.__logger,
            dashboard_host=self.__dashboard_host,
            dashboard_port=self.__dashboard_port,
        )
