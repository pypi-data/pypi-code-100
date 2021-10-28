# -*- coding: utf-8 -*-
from pip_services3_commons.refer import Descriptor
from pip_services3_rpc.services import CommandableHttpService


class DummyCommandableHttpService(CommandableHttpService):
    def __init__(self):
        super(DummyCommandableHttpService, self).__init__('dummies2')
        self._dependency_resolver.put('controller',
                                      Descriptor('pip-services-dummies', 'controller', 'default', '*', '*'))

    def register(self):
        # if not (self._swagger_auto and self._swagger_enabled):
        #     self._register_open_api_spec('swagger yaml content')

        super().register()
