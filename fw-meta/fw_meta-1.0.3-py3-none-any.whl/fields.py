"""Flywheel meta field definitions and utility functions."""
import datetime as dt
import pathlib
import re
import typing as t

import pathvalidate
from fw_utils import format_datetime, get_datetime

from .config import tz

# list of allowed fw metadata field names
# session and acquisition timezone fields are set automatically
FIELD_LIST: t.List[str] = [
    "group._id",
    "group.label",
    "project._id",
    "project.label",
    "subject._id",
    "subject.label",
    "subject.firstname",
    "subject.lastname",
    "subject.mlset",
    "subject.sex",
    "session._id",
    "session.uid",
    "session.label",
    "session.age",
    "session.weight",
    "session.operator",
    "session.timestamp",
    "acquisition._id",
    "acquisition.uid",
    "acquisition.label",
    "acquisition.timestamp",
    "file.name",
    "file.type",
    "file.modality",
]
FIELDS: t.Set[str] = set(FIELD_LIST)  # use set for efficient "is in" checks

# file.info meta field name regex (eg. file.info.custom matches/is allowed)
FILEINFO_RE = re.compile(r"file\.info(\.[0-9A-Za-z_]+)+")

# temporary meta field name regex
TMP_FIELD_RE = re.compile(r"T\d")

# map of meta field name shorthands to full names (allows simple patterns)
ALIASES: t.Dict[str, str] = {
    "group": "group._id",
    "group.id": "group._id",
    "project": "project.label",
    "project.id": "project._id",
    "subject": "subject.label",
    "subject.id": "subject._id",
    "session": "session.label",
    "session.id": "session._id",
    "acquisition": "acquisition.label",
    "acquisition.id": "acquisition._id",
    "timestamp": "acquisition.timestamp",
}

# field value validators
GROUP_ID_RE = r"^[0-9a-z][0-9a-z.@_-]{0,30}[0-9a-z]$"
OBJECT_ID_RE = r"^[0-9a-f]{24}$"
MLSET_RE = r"^Training|Testing|Validation$"


def validate_group_id(value: str) -> str:
    """Normalize and validate group id."""
    value = value.lower()
    match = re.match(GROUP_ID_RE, value)
    if not match:
        raise ValueError(f"Invalid group id: {value} (expected {GROUP_ID_RE!r})")
    return value


def validate_container_id(value: str) -> str:
    """Normalize and validate object id."""
    value = value.lower()
    match = re.match(OBJECT_ID_RE, value)
    if not match:
        raise ValueError(f"Invalid container id: {value} (expected {OBJECT_ID_RE!r})")
    return value


def validate_timestamp(value: t.Union[str, dt.datetime]) -> str:
    """Parse timestamp and return in isoformat."""
    value = get_datetime(value, tz=tz())
    return format_datetime(value)


def validate_mlset(value: str) -> str:
    """Ensure that mlset is one of Training|Testing|Validation."""
    value = value.title()
    match = re.match(MLSET_RE, value)
    if not match:  # pragma: no cover
        raise ValueError(f"Invalid ML-Set: {value} (expected {MLSET_RE!r})")
    return value


def validate_subject_sex(value: str) -> str:
    """Normalize subject.sex meta field.

    m, male   -> male
    f, female -> female
    o, other  -> other
    *         -> unknown
    """
    value = value.lower()
    if value in ("m", "male"):
        return "male"
    if value in ("f", "female"):
        return "female"
    if value in ("o", "other"):
        return "other"
    return "unknown"


def validate_filename(value: str) -> str:
    """Return cross-platform valid filename.

    Replace special characters with `_`.
    "*" character replaced with "star".
    """
    if isinstance(value, pathlib.Path):
        value = value.as_posix()
    value = value.replace("*", "star")
    value = pathvalidate.sanitize_filename(value, replacement_text="_")  # type: ignore
    return value


# map of meta field names to value validator regexes
VALIDATORS: t.Dict[str, t.Callable] = {
    "group._id": validate_group_id,
    "project._id": validate_container_id,
    "project.label": validate_filename,
    "subject._id": validate_container_id,
    "subject.sex": validate_subject_sex,
    "subject.label": validate_filename,
    "subject.mlset": validate_mlset,
    "session._id": validate_container_id,
    "session.label": validate_filename,
    "session.timestamp": validate_timestamp,
    "acquisition._id": validate_container_id,
    "acquisition.label": validate_filename,
    "acquisition.timestamp": validate_timestamp,
    "file.name": validate_filename,
}


def validate_field(field: str) -> str:
    """Return validated full meta field name (resolve aliases)."""
    if is_tmp_field(field):
        return field
    field = ALIASES.get(field, field)
    if field in FIELDS or FILEINFO_RE.match(field):
        return field
    raise ValueError(f"Invalid metadata field {field}")


def validate_field_value(field: str, value: str) -> t.Tuple[str, str]:
    """Return validated field name and value."""
    field = validate_field(field)
    value = VALIDATORS.get(field, lambda v: v)(value)
    return field, value


def is_tmp_field(field: str) -> bool:
    """Return True if the field is a tmp field otherwise False."""
    return bool(TMP_FIELD_RE.match(field))
