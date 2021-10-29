"""The module that defines the ``ExportAssignmentData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .assignment_export_column import AssignmentExportColumn


@dataclass
class ExportAssignmentData_1:
    """ """

    #: Export assignment information as a CSV file.
    type: "t.Literal['info']"
    #: The columns that should be included in the report.
    columns: "t.Sequence[AssignmentExportColumn]"
    #: If not `null` only the submissions of these users will be included in
    #: the report.
    user_ids: "t.Optional[t.Sequence[int]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "type",
                rqa.StringEnum("info"),
                doc="Export assignment information as a CSV file.",
            ),
            rqa.RequiredArgument(
                "columns",
                rqa.List(rqa.EnumValue(AssignmentExportColumn)),
                doc="The columns that should be included in the report.",
            ),
            rqa.RequiredArgument(
                "user_ids",
                rqa.Nullable(rqa.List(rqa.SimpleValue.int)),
                doc=(
                    "If not `null` only the submissions of these users will be"
                    " included in the report."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "type": to_dict(self.type),
            "columns": to_dict(self.columns),
            "user_ids": to_dict(self.user_ids),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ExportAssignmentData_1"], d: t.Dict[str, t.Any]
    ) -> "ExportAssignmentData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            type=parsed.type,
            columns=parsed.columns,
            user_ids=parsed.user_ids,
        )
        res.raw_data = d
        return res


@dataclass
class ExportAssignmentData_1_2:
    """ """

    #: Export submissions as zip.
    type: "t.Literal['files']"
    #: If not `null` only the submissions of these users will be exported.
    user_ids: "t.Optional[t.Sequence[int]]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "type",
                rqa.StringEnum("files"),
                doc="Export submissions as zip.",
            ),
            rqa.RequiredArgument(
                "user_ids",
                rqa.Nullable(rqa.List(rqa.SimpleValue.int)),
                doc=(
                    "If not `null` only the submissions of these users will be"
                    " exported."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "type": to_dict(self.type),
            "user_ids": to_dict(self.user_ids),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ExportAssignmentData_1_2"], d: t.Dict[str, t.Any]
    ) -> "ExportAssignmentData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            type=parsed.type,
            user_ids=parsed.user_ids,
        )
        res.raw_data = d
        return res


ExportAssignmentData = t.Union[
    ExportAssignmentData_1,
    ExportAssignmentData_1_2,
]
ExportAssignmentDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(ExportAssignmentData_1),
        ParserFor.make(ExportAssignmentData_1_2),
    ),
)
