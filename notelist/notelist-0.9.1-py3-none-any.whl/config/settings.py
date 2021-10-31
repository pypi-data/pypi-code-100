"""Settings module."""

from os import environ
import json
from typing import Any


class SettingsManager:
    """Key-value settings manager.

    Each setting is stored as an environment variable where the key and value
    of the setting are the key and value of the environment variable.
    """

    def __init__(self, schema_path: str):
        """Initialize the instance loading the setting schema.

        :param schema_path: Setting schema file path.
        """
        with open(schema_path) as f:
            self._schema = json.load(f)

    @property
    def schema(self) -> dict:
        """Return the setting schema.

        :return: Schema.
        """
        return self._schema.copy()

    def get(self, key: str) -> Any:
        """Return the value of a setting.

        An exception is raised if the setting is not found or not set.

        :param key: Setting key.
        :return: Setting value.
        """
        # Schema
        s = self._schema.get(key)

        if s is None:
            return s

        _typ = s.get("type", "string")
        _def = s.get("default")

        # Environment variable
        val = environ.get(key, _def)

        try:
            if val is not None:
                if _typ == "integer":
                    val = int(val)
                elif _typ != "string":
                    raise Exception(f"'{_typ}' type not supported")
        except Exception as e:
            raise Exception(f"'{key}' setting error: {e}")

        return val
