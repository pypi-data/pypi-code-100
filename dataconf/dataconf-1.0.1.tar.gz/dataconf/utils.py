from dataclasses import _MISSING_TYPE
from dataclasses import asdict
from dataclasses import fields
from dataclasses import is_dataclass
from typing import get_args
from typing import get_origin
from typing import Union

from dataconf.exceptions import EnvListOrderException
from dataconf.exceptions import MalformedConfigException
from dataconf.exceptions import MissingTypeException
from dataconf.exceptions import TypeConfigException
from dataconf.exceptions import UnexpectedKeysException
from dateutil.relativedelta import relativedelta
from pyhocon import ConfigFactory
from pyhocon.config_tree import ConfigList
from pyhocon.config_tree import ConfigTree
import pyparsing


NoneType = type(None)


def __parse_type(value, clazz, path, check):
    try:
        if check:
            return value
    except TypeError:
        pass

    raise TypeConfigException(f"expected type {clazz} at {path}, got {type(value)}")


def is_optional(type):
    # Optional = Union[T, NoneType]
    return get_origin(type) is Union and NoneType in get_args(type)


def __parse(value: any, clazz, path):

    if is_dataclass(clazz):

        if not isinstance(value, ConfigTree):
            raise TypeConfigException(
                f"expected type {clazz} at {path}, got {type(value)}"
            )

        fs = {}
        renamings = dict()

        for f in fields(clazz):

            if f.name in value:
                val = value[f.name]
            elif f.name.replace("_", "-") in value:
                renamings[f.name] = f.name.replace("_", "-")
                val = value[f.name.replace("_", "-")]
            else:
                if callable(f.default_factory):
                    val = f.default_factory()
                else:
                    val = f.default

            if not isinstance(val, _MISSING_TYPE):
                fs[f.name] = __parse(val, f.type, f"{path}.{f.name}")

            elif is_optional(f.type):
                # Optional not found
                fs[f.name] = None

            else:
                raise MalformedConfigException(
                    f"expected type {clazz} at {path}, no {f.name} found in dataclass"
                )

        unexpected_keys = value.keys() - {renamings.get(k, k) for k in fs.keys()}
        if len(unexpected_keys) > 0:
            raise UnexpectedKeysException(
                f"unexpected key(s) \"{', '.join(unexpected_keys)}\" detected for type {clazz} at {path}"
            )

        return clazz(**fs)

    origin = get_origin(clazz)
    args = get_args(clazz)

    if origin is list:
        if len(args) != 1:
            raise MissingTypeException("expected list with type information: List[?]")
        if value is not None:
            return [__parse(v, args[0], f"{path}[]") for v in value]
        return None

    if origin is dict:
        if len(args) != 2:
            raise MissingTypeException(
                "expected dict with type information: Dict[?, ?]"
            )
        if value is not None:
            return {k: __parse(v, args[1], f"{path}.{k}") for k, v in value.items()}
        return None

    if is_optional(clazz):
        left, right = args
        try:
            return __parse(value, left if right is NoneType else right, path)
        except TypeConfigException:
            # cannot parse Optional
            return None

    if origin is Union:
        left, right = args

        try:
            return __parse(value, left, path)
        except TypeConfigException as left_failure:
            try:
                return __parse(value, right, path)
            except TypeConfigException as right_failure:
                raise TypeConfigException(
                    f"expected type {clazz} at {path}, failed both:\n- {left_failure}\n- {right_failure}"
                )

    if clazz is bool:
        return __parse_type(value, clazz, path, isinstance(value, bool))

    if clazz is int:
        return __parse_type(value, clazz, path, isinstance(value, int))

    if clazz is float:
        return __parse_type(
            value, clazz, path, isinstance(value, float) or isinstance(value, int)
        )

    if clazz is str:
        return __parse_type(value, clazz, path, isinstance(value, str))

    if clazz is relativedelta:
        return __parse_type(value, clazz, path, isinstance(value, relativedelta))

    if clazz is ConfigTree:
        return __parse_type(value, clazz, path, isinstance(value, ConfigTree))

    child_failures = []
    for child_clazz in sorted(clazz.__subclasses__(), key=lambda c: c.__name__):
        if is_dataclass(child_clazz):
            try:
                return __parse(value, child_clazz, path)
            except (
                TypeConfigException,
                MalformedConfigException,
                UnexpectedKeysException,
            ) as e:
                child_failures.append(e)

    # no need to check length; false if empty
    if child_failures:
        failures = "\n- ".join([str(c) for c in child_failures])
        raise TypeConfigException(
            f"expected type {clazz} at {path}, failed subclasses:\n- {failures}"
        )

    raise TypeConfigException(f"expected type {clazz} at {path}, got {type(value)}")


def __generate(value: object, path):

    if is_dataclass(value):
        tree = {k: __generate(v, f"{path}.{k}") for k, v in asdict(value).items()}
        return ConfigTree(tree)

    if isinstance(value, dict):
        tree = {k: __generate(v, f"{path}.{k}") for k, v in value.items()}
        return ConfigTree(tree)

    if isinstance(value, list):
        tree = [__generate(e, f"{path}[]") for e in value]
        return ConfigList(tree)

    # needs a better impl.
    # if isinstance(value, timedelta):
    # if isinstance(value, relativedelta):

    return value


def __dict_list_parsing(prefix: str, obj):
    ret = {}

    def set_lens(p, focus, v):

        # value
        if len(p) == 1:
            # []x
            if isinstance(focus, list):
                if p[0] != len(focus):
                    raise EnvListOrderException
                focus.append(v)
            # {}x
            else:
                focus[p[0]] = v
            return

        # dict
        if p[1] == "":

            if p[0] not in focus:
                # []{x}
                if isinstance(focus, list):
                    if p[0] != len(focus):
                        raise EnvListOrderException
                    focus.append({})
                # {}{x}
                else:
                    focus[p[0]] = {}

            return set_lens(p[2:], focus[p[0]], v)

        # list
        if isinstance(p[1], int):

            if p[0] not in focus:
                # [][x]
                if isinstance(focus, list):
                    if p[1] != len(focus):
                        raise EnvListOrderException
                    focus.append([])
                # {}[x]
                else:
                    focus[p[0]] = []

            return set_lens(p[1:], focus[p[0]], v)

        # compose path
        return set_lens([f"{p[0]}_{p[1]}"] + p[2:], focus, v)

    def int_or_string(v):
        try:
            return int(v)
        except ValueError:
            return v

    if not prefix.endswith("_"):
        prefix = f"{prefix}_"

    for k, v in sorted(obj.items(), key=lambda x: x[0]):
        if k.startswith(prefix):

            path = [int_or_string(e) for e in k[len(prefix) :].lower().split("_")]
            try:
                value = ConfigFactory.parse_string(v)
            except pyparsing.ParseSyntaxException:
                value = v

            set_lens(path, ret, value)

    return ret
