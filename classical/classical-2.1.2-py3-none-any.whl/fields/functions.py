from typing import AbstractSet, Any, Dict, List, Optional, Set, Tuple, Type, Union

from classical.fields.base import ClassField
from classical.fields.generic import GenericFieldInspector


# typing.Collection is not supported by Python 3.5
StrCollection = Union[AbstractSet[str], List[str], Tuple[str, ...]]


def get_fields(cls_or_obj: Any) -> List[ClassField]:
    """
    Alias for :func:`~classical.fields.generic.GenericFieldInspector.get_fields`
    """
    return GenericFieldInspector.get_fields(cls_or_obj)


def get_field_dict(obj: Any) -> Dict[ClassField, Any]:
    """
    Alias for :func:`~classical.fields.generic.GenericFieldInspector.get_field_dict`
    """
    return GenericFieldInspector.get_field_dict(obj)


def get_name_dict(
        obj: Any, attr_mode: bool = False, init_mode: bool = False,
) -> Dict[str, Any]:
    """
    Alias for :func:`~classical.fields.generic.GenericFieldInspector.get_name_dict`
    """
    return GenericFieldInspector.get_name_dict(
        obj, attr_mode=attr_mode, init_mode=init_mode
    )


def get_name_list(
        obj: Any, attr_mode: bool = False, init_mode: bool = False,
) -> List[str]:
    """
    Alias for :func:`~classical.fields.generic.GenericFieldInspector.get_name_list`
    """
    return GenericFieldInspector.get_name_list(
        obj, attr_mode=attr_mode, init_mode=init_mode
    )


def _strip_excludes(
        _fields: List[ClassField],
        exclude_names: StrCollection = ()
) -> Set[ClassField]:
    return {f for f in _fields if f.name not in exclude_names}


def are_analogous(*objs: Any, exclude_names: StrCollection = ()) -> bool:
    """
    Compare field structure of two or more objects
    :param objs: fielded objects
    :param exclude_names: field names to omit from the comparison
    :return: ``True`` if fields are the same for all objects, ``False`` otherwise
    """
    if not objs:
        return True

    exclude_names = set(exclude_names)

    standard_fields = _strip_excludes(
        get_fields(objs[0]), exclude_names=exclude_names)
    for other_obj in objs[1:]:
        other_fields = _strip_excludes(
            get_fields(other_obj), exclude_names=exclude_names)
        if other_fields != standard_fields:
            return False

    return True


def copy_to_class(
        src: Any, dst_cls: Type,
        exclude_names: StrCollection = (),
        ignore_extra: bool = False,
        ignore_missing: bool = False,
        defaults: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Create instance of fielded class ``dst_cls``
    by copying values from fielded instance ``src``
    :param src: source object
    :param dst_cls: destination class
    :param exclude_names: field names to omit from the copy procedure
    :param ignore_extra: ignore extra fields in source; default is ``False``
    :param ignore_missing: ignore fields missing in source; default is ``False``
    :param defaults: default values for missing fields
    """
    exclude_names = set(exclude_names)

    src_fields = _strip_excludes(get_fields(src), exclude_names=exclude_names)
    dst_fields = _strip_excludes(get_fields(dst_cls), exclude_names=exclude_names)
    init_dict = {**(defaults or {})}  # type: Dict[str, Any]
    missing_field_names = []  # type: List[str]
    for field in dst_fields:
        if field in src_fields:
            init_dict[field.init_name] = field[src]
            src_fields.remove(field)
        else:
            if not ignore_missing and field.name not in init_dict:
                missing_field_names.append(field.name)

    if missing_field_names:
        raise ValueError('Missing field: {}'.format(missing_field_names))

    if src_fields and not ignore_extra:
        raise ValueError('Extra fields {}'.format([field.name for field in src_fields]))

    return dst_cls(**init_dict)
