from typing import List
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.container.ContainerInterface import ContainerInterface
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias


class Bundle:
    def get_config_files(self):
        return ["config.yaml"]

    def get_compiler_passes(self) -> List[CompilerPassInterface]:
        return []

    def modify_raw_config(self, raw_config: dict) -> dict:
        return raw_config

    def modify_services(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box):
        return services, aliases

    def modify_parameters(self, parameters: Box) -> Box:
        return parameters

    def boot(self, container: ContainerInterface):
        pass
