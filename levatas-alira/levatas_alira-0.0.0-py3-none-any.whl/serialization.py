import logging
import json
import sys
import traceback

from importlib import import_module


logger = logging.getLogger(__name__)


class FunctionWrapper(object):
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

    def process(self, *args, **kwargs):
        return self.function(*args, **dict(self.arguments, **kwargs))


class Deserializer:
    @staticmethod
    def package_from_str(full_package_name):
        module_path, _, package_name = full_package_name.rpartition(".")
        module = import_module(module_path)

        return getattr(module, package_name), package_name

    @staticmethod
    def _create_instance_from_class(reference: str, **kwargs):
        try:
            module, package_name = Deserializer.package_from_str(reference)

            return module(**kwargs), package_name
        except (Exception):
            _, _, exc_tb = sys.exc_info()

            logger.error(traceback.print_tb(exc_tb))

            raise ValueError(
                f"There was an error trying to instantiate the "
                f'reference "{reference}"'
            )

    @staticmethod
    def instantiate(key, reference, model_base_directory):
        if reference is None:
            return None

        if isinstance(reference, str) and (
            key.startswith("fn_") or key.endswith("_fn")
        ):
            function, _ = Deserializer.package_from_str(reference)
            return function

        if isinstance(reference, list):
            instances = []

            for item in reference:
                instances.append(Deserializer.instantiate(key, item, model_base_directory))

            return instances

        if isinstance(reference, dict):
            arguments = {
                "model_base_directory": model_base_directory
            }
            for key, value in reference.items():
                if key != "class" and key != "function":
                    arguments[key] = Deserializer.instantiate(key, value, model_base_directory)

            if "class" in reference:
                module, pkg_name = Deserializer._create_instance_from_class(
                    reference["class"], **arguments
                )
                return module

            if "function" in reference:
                function, pkg_name = Deserializer.package_from_str(
                    reference["function"]
                )

                wrapper_object = FunctionWrapper(function, arguments)
                return wrapper_object.process

            return arguments

        return reference
