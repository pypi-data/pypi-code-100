import logging

from importlib import import_module

from alira.instance import Instance


class Map(object):
    def __init__(
        self,
        function: str = None,
        **kwargs,
    ):
        self._pipeline_module_name = function
        self.function = self._load_function(function)

    def run(self, instance: Instance, **kwargs):
        if self.function:
            result = self.function(instance=instance, **kwargs)

            if not isinstance(result, dict):
                raise RuntimeError(
                    "The result of the map operation must be a dictionary"
                )

            return result

        return None

    def _load_function(self, function_name: str):
        try:
            module_path, _, fn_name = function_name.rpartition(".")
            function = getattr(import_module(module_path), fn_name)
            logging.info(f"Loaded function {function_name}")

            return function
        except Exception as e:
            logging.exception(e)
            raise RuntimeError(f"Unable to load function {function_name}") from e
