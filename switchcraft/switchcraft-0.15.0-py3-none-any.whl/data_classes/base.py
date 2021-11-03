from typing import Any, Dict, Optional


class DictWrapper:
    """Provides a single read only access to a wrapper dict.

    It's important that all data classes in this module inherit from
    this class.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)
