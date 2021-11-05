from whizbang.domain.manager.az.az_manager_base import AzManagerBase
from whizbang.domain.repository.az.az_datafactory_repository import AzDatafactoryRepository


class AzDatafactoryManager(AzManagerBase):
    def __init__(self, repository: AzDatafactoryRepository):
        AzManagerBase.__init__(self, repository=repository)
        self._repository: AzDatafactoryRepository = self._repository

    def get_integration_runtime_key(self,
                                    datafactory_name: str,
                                    resource_group: str,
                                    integration_runtime_name: str) -> str:
        return self._repository.get_integration_runtime_key(datafactory_name=datafactory_name,
                                                            resource_group=resource_group,
                                                            integration_runtime_name=integration_runtime_name)

    def get_datafactory_json(self,
                             factory_name: str,
                             resource_group: str):
        return self._repository.get_datafactory_json(factory_name=factory_name,
                                                     resource_group=resource_group)
