"""Bruker ParaVision file format - read only (subject/acqp/method files)."""
import re
import typing as t
from datetime import datetime

from fw_utils import get_datetime

from .base import AnyFile, FieldsMixin, File, ReadOnly, filter_meta

ARRAY_RE = re.compile(r"\( \d+(, \d+)* \)")
VERSION_RE = re.compile(r"(PV|ParaVision) ?(?P<ver>\d+(\.\d+)+)")


class ParaVision(ReadOnly, FieldsMixin, File):
    """Bruker ParaVision file class."""

    def __init__(self, file: AnyFile) -> None:
        """Read and parse a Bruker ParaVision file.

        Args:
            file (str|Path|file): Filepath (str|Path) or open file to read from.
        """
        super().__init__(file)
        with self.file as rfile:
            object.__setattr__(self, "fields", load_paravision(rfile))

    @property
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata of ParaVision file."""
        session_ts = get_timestamp(self.get("subject_abs_date", ""))
        acq_ts = get_timestamp(self.get("acq_abs_time", ""))
        session_label = [self.get("subject_study_name")]
        if session_ts:
            session_label.append(session_ts.strftime("%Y%m%d%H%M%S"))
        meta = {
            "subject.label": self.get("subject_id"),
            "subject.sex": self.get("subject_sex"),
            "session.uid": self.get("subject_study_instance_uid"),
            "session.label": " - ".join([p for p in session_label if p]),
            "session.timestamp": session_ts,
            "acquisition.label": self.get("acq_protocol_name"),
            "acquisition.timestamp": acq_ts,
            "file.type": "ParaVision",
        }
        return filter_meta(meta)


def load_paravision(file: t.BinaryIO) -> t.Dict[str, t.Any]:
    """Parse ParaVision parameters file as a dictionary."""
    fields: t.Dict[str, t.Any] = {}
    key = None
    for line_bytes in file:
        line = line_bytes.decode()
        if not fields.get("version") and (match := VERSION_RE.search(line)):
            fields["version"] = match.group("ver")
        if line.startswith("$$"):
            continue
        if line.startswith("##"):
            key, _, value = line.partition("=")
            key = key.lstrip("##$").lower()
            if ARRAY_RE.match(value):
                value = ""
        else:
            value = line
        if key:
            value = value.strip(" <>\n")
            fields[key] = fields.get(key, "") + value
    return fields


def get_timestamp(value: str) -> t.Optional[datetime]:
    """Return iso timestamp from bruker epoch value."""
    abs_time, *_ = value.strip("()").partition(",")
    if not abs_time:
        return None
    return get_datetime(int(abs_time))
