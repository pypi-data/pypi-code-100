from whizbang.data.az_cli_context import AzCliContext
from whizbang.domain.repository.az.az_repository_base import AzRepositoryBase


class AzDatafactoryRepository(AzRepositoryBase):
    def __init__(self, context: AzCliContext):
        AzRepositoryBase.__init__(self, context)

    @property
    def _resource_provider(self) -> str:
        return "datafactory"

    def get_integration_runtime_key(self,
                                    datafactory_name: str,
                                    resource_group: str,
                                    integration_runtime_name: str) -> str:
        auth_keys: dict = self._execute(f'integration-runtime list-auth-key'
                                        f' --factory-name {datafactory_name}'
                                        f' --resource-group {resource_group}'
                                        f' --integration-runtime-name {integration_runtime_name}')
        if auth_keys is not None:
            return auth_keys["authKey1"]

    def get_datafactory_json(self,
                             factory_name: str,
                             resource_group: str):
        return self._execute(f'show'
                             f' --factory-name {factory_name}'
                             f' --resource-group {resource_group}')
