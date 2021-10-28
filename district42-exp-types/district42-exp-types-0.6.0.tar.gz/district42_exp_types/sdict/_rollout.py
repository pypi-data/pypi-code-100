from typing import Any, Dict, Union, cast

from district42 import optional

__all__ = ("rollout",)


KeysType = Dict[Union[str, optional], Any]


def rollout(keys: KeysType, separator: str = ".") -> KeysType:
    updated: KeysType = {}

    for comp_key, val in keys.items():
        assert isinstance(comp_key, (str, optional))

        is_optional = False
        if isinstance(comp_key, optional):
            comp_key = comp_key.key
            is_optional = True

        parts = cast(str, comp_key).split(separator)
        key = parts[0]
        if len(parts) == 1:
            updated[optional(key) if is_optional else key] = val
        else:
            if key not in updated:
                updated[key] = {}
            tail = separator.join(parts[1:])
            updated[key][optional(tail) if is_optional else tail] = val

    for k, v in updated.items():
        updated[k] = rollout(v) if isinstance(v, dict) else v

    return updated
