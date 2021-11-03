from whizbang.config.app_config import AppConfig
from whizbang.domain.handler.handler_base import HandlerBase
from whizbang.domain.manager.az.az_datafactory_manager import AzDatafactoryManager


class DatafactoryHandler(HandlerBase):
    def __init__(self,
                 app_config: AppConfig,
                 manager: AzDatafactoryManager):
        HandlerBase.__init__(self, app_config=app_config)
        self.manager = manager

    def get_integration_runtime_key(self,
                                    datafactory_name: str,
                                    resource_group: str,
                                    integration_runtime_name: str) -> str:
        return self.manager.get_integration_runtime_key(datafactory_name=datafactory_name,
                                                        resource_group=resource_group,
                                                        integration_runtime_name=integration_runtime_name)

    def get_object_id(self,
                      factory_name: str,
                      resource_group: str):
        datafactory_json = self.manager.get_datafactory_json(factory_name=factory_name,
                                                             resource_group=resource_group)
        if datafactory_json is not None:
            return datafactory_json["identity"]["principalId"]
