from abc import ABCMeta

from colassigner.util import camel_to_snake

from .constants import DEFAULT_PP, FORBIDDEN_NAMES, PREFIX_SEP


class ColMeta(ABCMeta):
    def __new__(cls, name, bases, local):
        for attr in local:
            if (attr in FORBIDDEN_NAMES) or (
                PREFIX_SEP in attr and not attr.startswith("_")
            ):
                raise ValueError(
                    f"Column name can't be either {FORBIDDEN_NAMES}. "
                    f"And can't contain the string {PREFIX_SEP}. "
                    f"{attr} is given"
                )
        return super().__new__(cls, name, bases, local)

    def __init__(self, name: str, bases, namespace) -> None:
        super().__init__(name, bases, namespace)
        self._parent_prefixes = namespace.get("_parent_prefixes", DEFAULT_PP)

    def __getattribute__(cls, attid):
        "so that Cls.xy returns a string for column access"

        att_value = super().__getattribute__(attid)

        if attid.startswith("_") or (attid in FORBIDDEN_NAMES):
            return att_value

        new_pref_arr = (*cls._parent_prefixes, camel_to_snake(attid))

        if isinstance(att_value, ColMeta):

            class _C(att_value):
                _parent_prefixes = new_pref_arr

            return _C

        return PREFIX_SEP.join(filter(None, new_pref_arr))

    def __getcoltype__(cls, attid):
        colval = super().__getattribute__(attid.split(PREFIX_SEP)[-1])
        return colval
