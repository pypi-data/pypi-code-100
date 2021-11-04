import logging
import os
from pathlib import Path
from typing import Callable

from dependency_injector import containers, providers
from flask import Flask

from paretos.socrates.project_api_client import ProjectApiClient

from ...version import VERSION
from .request_handler.jsend import JSend
from .request_handler.request_handler import RequestHandler
from .routes.get_project_meta import GetProjectMeta
from .routes.get_projects import GetProjects
from .routes.get_solutions import GetSolutions
from .service.error_handler import ErrorHandler
from .service.logger import Logger
from .service.request_id_provider import RequestIdProvider


class Container(containers.DeclarativeContainer):
    config: providers.Configuration = providers.Configuration()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    App: Callable[[], Flask] = providers.Singleton(
        Flask, "Data API", template_folder=Path(dir_path).parent / "templates"
    )

    Request_Id_Provider: Callable[[], RequestIdProvider] = providers.Singleton(
        RequestIdProvider
    )

    Version_Obj: Callable[[], str] = providers.Object(VERSION)

    Logger_Obj: Callable[[], logging.Logger] = providers.Singleton(
        Logger, request_id_provider=Request_Id_Provider, api_version=Version_Obj
    )

    JSend = providers.Singleton(
        JSend, request_id_provider=Request_Id_Provider, api_version=Version_Obj
    )

    ErrorHandler = providers.Singleton(
        ErrorHandler, application_protocol=JSend, logger=Logger_Obj
    )

    RequestHandler = providers.Singleton(
        RequestHandler,
        application_protocol=JSend,
        logger=Logger_Obj,
    )

    project_api_client = providers.Factory(
        ProjectApiClient, session=config.api_session.required()
    )

    Route_GetProjects: Callable[[], GetProjects] = providers.Factory(
        GetProjects, logger=Logger_Obj, api_client=project_api_client
    )

    Route_GetProjectMeta: Callable[[], GetProjectMeta] = providers.Factory(
        GetProjectMeta, logger=Logger_Obj, api_client=project_api_client
    )

    Route_GetSolutions: Callable[[], GetSolutions] = providers.Factory(
        GetSolutions, logger=Logger_Obj, api_client=project_api_client
    )
