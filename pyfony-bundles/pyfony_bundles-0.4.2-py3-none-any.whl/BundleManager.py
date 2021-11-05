from pathlib import Path
from typing import List
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.config.ConfigLoader import ConfigLoader
from injecta.config.ConfigMerger import ConfigMerger
from injecta.service.Service import Service
from injecta.package.path_resolver import resolve_path
from injecta.service.ServiceAlias import ServiceAlias
from pyfonybundles.Bundle import Bundle


class BundleManager:
    def __init__(self, bundles: List[Bundle]):
        self.__bundles = bundles
        self.__config_loader = ConfigLoader()
        self.__config_merger = ConfigMerger()

    def get_compiler_passes(self) -> List[CompilerPassInterface]:
        compiler_passes = []

        for bundle in self.__bundles:
            compiler_passes += bundle.get_compiler_passes()

        return compiler_passes

    def get_bundles_config(self) -> dict:
        config = dict()

        for bundle in self.__bundles:
            root_module_name = bundle.__module__[: bundle.__module__.find(".")]
            config_base_path = resolve_path(root_module_name) + "/_config"

            for config_file_name in bundle.get_config_files():
                config_file_path = Path(config_base_path + "/" + config_file_name)
                new_config = self.__config_loader.load(config_file_path)

                config = self.__config_merger.merge(config, new_config, False)

        return config

    def get_project_bundles_config(self, bundles_configs_dir: str) -> dict:
        config = dict()

        for bundle in self.__bundles:
            root_package_name = bundle.__module__[: bundle.__module__.find(".")]
            project_bundle_config_path = Path(bundles_configs_dir + "/" + root_package_name + ".yaml")

            if project_bundle_config_path.exists():
                project_bundle_config = self.__config_loader.load(project_bundle_config_path)

                config = self.__config_merger.merge(config, project_bundle_config)

        return config

    def modify_raw_config(self, raw_config: dict) -> dict:
        for bundle in self.__bundles:
            raw_config = bundle.modify_raw_config(raw_config)

        return raw_config

    def modify_services(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box):
        for bundle in self.__bundles:
            services, aliases = bundle.modify_services(services, aliases, parameters)

        return services, aliases

    def modify_parameters(self, parameters: Box) -> Box:
        for bundle in self.__bundles:
            parameters = bundle.modify_parameters(parameters)

        return parameters
