from typing import Dict, Any


def _dict_update_when_missing(map: Dict = None, key: Any = None, value: Any = None):
    if key not in map:
        map.update({key: value})
