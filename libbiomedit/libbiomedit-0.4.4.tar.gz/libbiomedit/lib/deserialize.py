from typing import (
    Union,
    Tuple,
    Any,
    Dict,
    Optional,
    Sequence,
    cast,
    Callable,
    Type,
    get_type_hints,
)
import collections.abc
import warnings
from enum import Enum

import dataclasses

from .classify import (
    classify,
    __origin_attr__,
    AbstractType,
    IsDataclass,
    IsTypingType,
    is_secret,
)
from .secret import Secret


def deserialize(T: AbstractType) -> Callable[[Any], Any]:
    """Creates a deserializer for the type :T:. It handles dataclasses,
    sequences, typing.Optional, Enum and primitive types.

    :returns: A deserializer, converting a dict, list or primitive to :T:
    """
    return _deserializers.get(classify(T), lambda x: x)(T)


def serialize(T: AbstractType) -> Callable[[Any], Any]:
    """Creates a serializer for the type :T:. It handles dataclasses,
    sequences, typing.Optional, Enum and primitive types.

    :returns: A serializer, converting an instance of :T: to dict, list or primitive
    """
    return _serializers.get(classify(T), lambda x: x)(T)


_deserializers = {}
_serializers = {}


def _deserializer(T: Any):
    def decorator(f):
        _deserializers[T] = f
        return f

    return decorator


def _serializer(T: Any):
    def decorator(f):
        _serializers[T] = f
        return f

    return decorator


def _serializer_deserializer(T: Any):
    def decorator(f):
        _deserializers[T] = f(deserialize)
        _serializers[T] = f(serialize)
        return f

    return decorator


@_deserializer(Any)
def deserialize_any(_: AbstractType):
    return lambda x: x


@_serializer(Any)
def serialize_any(_: AbstractType):
    def _serialize(x: Any):
        if isinstance(x, Secret):
            raise RuntimeError(
                "Trying to implicitly serialize a Secret. Try using Optional[Secret]."
            )

        return x

    return _serialize


@_deserializer(Secret)
def deserialize_secret(T: Type[Secret]):
    inner_deserialize = deserialize(getattr(T, "__args__", (Any,))[0])
    return lambda val: Secret(inner_deserialize(val))


@_serializer(Secret)
def serialize_secret(_: AbstractType):
    def _serialize(_: Secret):
        raise RuntimeError(
            "Trying to explicitly serialize a Secret. This should not happen."
        )

    return _serialize


@_serializer_deserializer(Tuple)
def transform_tuple(transform):
    def _transform_tuple(T: IsTypingType):
        item_types = cast(Tuple[AbstractType, ...], T.__args__)
        if transform is serialize and any(
            is_secret(item_type) for item_type in item_types
        ):
            raise ValueError(
                "Serializing tuples containing Secret is not supported. Try using Optional[Secret]"
            )

        if len(item_types) == 2 and item_types[1] is ...:
            inner_transform = transform(item_types[0])

            def _transform_ellipsis(data: tuple):
                return tuple(inner_transform(item) for item in data)

            return _transform_ellipsis

        inner_transforms = [transform(T) for T in item_types]

        def _transform(data: tuple):
            if len(item_types) != len(data):
                raise ValueError(f"Wrong number ({len(data)}) of items for {repr(T)}")
            return tuple(
                inner_transform(item)
                for inner_transform, item in zip(inner_transforms, data)
            )

        return _transform

    return _transform_tuple


@_serializer_deserializer(Sequence)
def transform_seq(transform):
    def _transform_seq(T: IsTypingType):
        seq_type = getattr(T, __origin_attr__, None)
        try:
            item_type = T.__args__[0]
        except AttributeError as e:
            raise ValueError(
                f"Sequence of type {seq_type.__name__} without item type"
            ) from e
        if transform is serialize and is_secret(item_type):
            raise ValueError(
                "Serializing sequences of Secret is not supported. try using Optional[Secret]"
            )
        if seq_type is collections.abc.Sequence:
            seq_type = list

        def _transform(data):
            return seq_type(map(transform(item_type), data))

        return _transform

    return _transform_seq


@_deserializer(IsDataclass)
def deserialize_dataclass(T):
    deserializers_by_name = prepare_serializers(T, deserialize)

    def _deserialize(data: dict):
        unexpected_keys = set(data) - set(n for n, _ in deserializers_by_name)
        if unexpected_keys:
            warnings.warn(
                f"{T.__name__}: Unexpected keys: " + ", ".join(unexpected_keys)
            )
        converted_data = {
            f_name: deserializer(data[f_name])
            for f_name, deserializer in deserializers_by_name
            if f_name in data
        }
        return T(**converted_data)

    return _deserialize


@_serializer(IsDataclass)
def serialize_dataclass(T):
    serializers_by_name = prepare_serializers(T, serialize)
    if any(is_secret(f.type) for f in dataclasses.fields(T)):
        raise ValueError(
            "Serializing dataclasses with Secret values are not supported. Try using Optional[Secret]."
        )

    def _serialize(obj):
        converted_data = {
            f_name: serializer(getattr(obj, f_name))
            for f_name, serializer in serializers_by_name
        }
        return converted_data

    return _serialize


def prepare_serializers(
    T: IsDataclass, method: Callable
) -> Sequence[Tuple[str, Callable]]:
    fields = dataclasses.fields(T)
    type_hints = get_type_hints(T)
    return [
        (f.name, method(f.metadata.get(method.__name__, type_hints[f.name])))
        for f in fields
    ]


@_serializer_deserializer(Optional)
def transform_optional(transform):
    def _transform_optional(T: IsTypingType):
        opt_type = optional_type(T)

        if is_secret(opt_type) and transform is serialize:
            return lambda _: None

        inner_transform = transform(opt_type)

        def _transform(data):
            if data is None:
                return None
            return inner_transform(data)

        return _transform

    return _transform_optional


def optional_type(T: IsTypingType) -> type:
    return next(
        t for t in T.__args__ if not (isinstance(t, type) and isinstance(None, t))
    )


@_deserializer(Union)
def deserialize_union(T: IsTypingType):
    """Deserializes Unions of dataclasses.
    The variants are assumed to be adjacently tagged by its type ("type" and "value")."""
    types = T.__args__
    if not all(dataclasses.is_dataclass(t) for t in types):
        raise ValueError("Currently, only Unions of dataclasses are supported")
    transform_by_name = {t.__name__: deserialize(t) for t in types}

    def _deserialize(data):
        type_name = data.get("type")
        if type_name is None:
            raise ValueError(
                f"Union[{', '.join(transform_by_name)}]: missing `type` item"
            )
        inner_transform = transform_by_name.get(type_name)
        if inner_transform is None:
            raise ValueError(
                f"Union[{', '.join(transform_by_name)}]: "
                f"unexpected type `{type_name}`"
            )
        return inner_transform(data["value"])

    return _deserialize


@_serializer(Union)
def serialize_union(T: IsTypingType):
    """Serializes Unions of dataclasses.
    The variants are adjacently tagged by its type ("type" and "value")."""
    types = T.__args__
    if not all(dataclasses.is_dataclass(t) for t in types):
        raise ValueError("Currently, only Unions of dataclasses are supported")
    transform_by_type = {t: serialize(t) for t in types}

    def _serialize(data):
        inner_type = type(data)
        inner_serialize = transform_by_type.get(inner_type)
        if inner_serialize is None:
            variants = ", ".join(t.__name__ for t in transform_by_type)
            raise ValueError(
                f"{data}: Could associate {inner_type.__name__} to one of the variants {variants}"
            )
        return {"type": inner_type.__name__, "value": inner_serialize(data)}

    return _serialize


def transform_dict(transform):
    def _transform_dict(T: IsTypingType):
        key_type, val_type = T.__args__

        if transform is serialize and is_secret(val_type):
            raise ValueError(
                "Serializing dicts with Secret values is not supported. Use Optional[Secret]."
            )

        key_transform = transform(key_type)
        val_transform = transform(val_type)

        def _transform(data):
            return {key_transform(key): val_transform(val) for key, val in data.items()}

        return _transform

    return _transform_dict


@_serializer(Dict)
def serialize_dict(T: Type[dict]):
    """Special serializer to support dict[str, Any] holding Secret values.
    In this case Secret is interpreted as Optional[Secret] and serialized to None."""
    raw_serialize = transform_dict(serialize)(T)

    def _serialize(obj: dict):
        return raw_serialize(
            {
                key: val if not isinstance(val, Secret) else None
                for key, val in obj.items()
            }
        )

    return _serialize


@_deserializer(Dict)
def deserialize_dict(T: Type[dict]):
    return transform_dict(deserialize)(T)


@_serializer(Enum)
def serialize_enum(_T: Type[Enum]):
    def _serialize(obj: Enum):
        return obj.value

    return _serialize
