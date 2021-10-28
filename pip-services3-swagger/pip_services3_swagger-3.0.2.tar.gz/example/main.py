# -*- coding: utf-8 -*-

import sys
import os

import keyboard
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import References, Descriptor, Referencer
from pip_services3_commons.run import Opener, Closer
from pip_services3_components.count import LogCounters
from pip_services3_components.log import ConsoleLogger
from pip_services3_rpc.services import HttpEndpoint, StatusRestService, HeartbeatRestService

from logic.DummyController import DummyController
from services.DummyCommandableHttpService import DummyCommandableHttpService
from services.DummyRestService import DummyRestService
from pip_services3_swagger.services.SwaggerService import SwaggerService

# add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Create components
logger = ConsoleLogger()
controller = DummyController()
http_endpoint = HttpEndpoint()
rest_service = DummyRestService()
http_service = DummyCommandableHttpService()
status_service = StatusRestService()
heartbeat_service = HeartbeatRestService()
swagger_service = SwaggerService()

components = [
    controller,
    http_endpoint,
    rest_service,
    http_service,
    status_service,
    heartbeat_service,
    swagger_service
]

try:
    # Configure components
    logger.configure(ConfigParams.from_tuples('level', 'trace'))
    http_endpoint.configure(ConfigParams.from_tuples(
        'connection.protocol', 'http',
        'connection.host', 'localhost',
        'connection.port', 8080
    ))
    rest_service.configure(ConfigParams.from_tuples('swagger.enable', True))
    http_service.configure(ConfigParams.from_tuples(
        'base_route', 'dummies2',
        'swagger.enable', True
    ))

    # Set references
    references = References.from_tuples(
        Descriptor('pip-services', 'logger', 'console', 'default', '1.0'), logger,
        Descriptor('pip-services', 'counters', 'log', 'default', '1.0'), LogCounters(),
        Descriptor('pip-services', 'endpoint', 'http', 'default', '1.0'), http_endpoint,
        Descriptor('pip-services-dummies', 'controller', 'default', 'default', '1.0'), controller,
        Descriptor('pip-services-dummies', 'service', 'rest', 'default', '1.0'), rest_service,
        Descriptor('pip-services-dummies', 'service', 'commandable-http', 'default', '1.0'), http_service,
        Descriptor('pip-services', 'status-service', 'rest', 'default', '1.0'), status_service,
        Descriptor('pip-services', 'heartbeat-service', 'rest', 'default', '1.0'), heartbeat_service,
        Descriptor('pip-services', 'swagger-service', 'http', 'default', '1.0'), swagger_service
    )

    Referencer.set_references(references, components)

    # Open components
    Opener.open(None, components)

except Exception as ex:
    logger.error(None, ex, 'Failed to execute the microservice')
    sys.exit(1)


def terminate():
    Closer.close(None, components)
    sys.exit(0)


# Wait until user presses ENTER or ctrl+c
keyboard.add_hotkey('ctrl+c', terminate)
keyboard.add_hotkey('enter', terminate)
