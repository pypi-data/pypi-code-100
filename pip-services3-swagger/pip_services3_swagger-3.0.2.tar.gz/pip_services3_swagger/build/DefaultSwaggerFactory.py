# -*- coding: utf-8 -*-

from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory

from pip_services3_swagger.services.SwaggerService import SwaggerService


class DefaultSwaggerFactory(Factory):
    """
    Creates Swagger components by their descriptors.

    See :class:`Factory <pip_services3_components.build.Factory.Factory>`
    :class:`HttpEndpoint <pip_services3_rpc.services.HttpEndpoint.HttpEndpoint>`
    :class:`HeartbeatRestService <pip_services3_rpc.services.HeartbeatRestService.HeartbeatRestService>`
    :class:`StatusRestService <pip_services3_rpc.services.StatusRestService.StatusRestService>`
    """
    descriptor = Descriptor("pip-services", "factory", "swagger", "default", "1.0")
    swagger_service_descriptor = Descriptor("pip-services", "swagger-service", "*", "*", "1.0")

    def __init__(self):
        super(DefaultSwaggerFactory, self).__init__()
        self.register_as_type(DefaultSwaggerFactory.swagger_service_descriptor, SwaggerService)
