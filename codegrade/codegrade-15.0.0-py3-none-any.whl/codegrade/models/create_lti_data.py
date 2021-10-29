"""The module that defines the ``CreateLTIData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict


@dataclass
class CreateLTIData_1:
    """ """

    #: The id of the tenant that will use this LMS
    tenant_id: "str"
    #: The LMS that will be used for this connection
    lms: "t.Literal['Canvas', 'Blackboard', 'Sakai', 'Open edX', 'Moodle', 'BrightSpace', 'Populi']"
    #: Use LTI 1.1
    lti_version: "t.Literal['lti1.1']"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc="The id of the tenant that will use this LMS",
            ),
            rqa.RequiredArgument(
                "lms",
                rqa.StringEnum(
                    "Canvas",
                    "Blackboard",
                    "Sakai",
                    "Open edX",
                    "Moodle",
                    "BrightSpace",
                    "Populi",
                ),
                doc="The LMS that will be used for this connection",
            ),
            rqa.RequiredArgument(
                "lti_version",
                rqa.StringEnum("lti1.1"),
                doc="Use LTI 1.1",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "tenant_id": to_dict(self.tenant_id),
            "lms": to_dict(self.lms),
            "lti_version": to_dict(self.lti_version),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["CreateLTIData_1"], d: t.Dict[str, t.Any]
    ) -> "CreateLTIData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            tenant_id=parsed.tenant_id,
            lms=parsed.lms,
            lti_version=parsed.lti_version,
        )
        res.raw_data = d
        return res


@dataclass
class CreateLTIData_1_2:
    """ """

    #: The id of the tenant that will use this LMS
    tenant_id: "str"
    #: The iss of the new provider
    iss: "str"
    #: The LMS that will be used for this connection
    lms: "t.Literal['Canvas', 'Blackboard', 'Moodle', 'Brightspace']"
    #: Use LTI 1.3
    lti_version: "t.Literal['lti1.3']" = "lti1.3"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "tenant_id",
                rqa.SimpleValue.str,
                doc="The id of the tenant that will use this LMS",
            ),
            rqa.RequiredArgument(
                "iss",
                rqa.SimpleValue.str,
                doc="The iss of the new provider",
            ),
            rqa.RequiredArgument(
                "lms",
                rqa.StringEnum(
                    "Canvas", "Blackboard", "Moodle", "Brightspace"
                ),
                doc="The LMS that will be used for this connection",
            ),
            rqa.DefaultArgument(
                "lti_version",
                rqa.StringEnum("lti1.3"),
                doc="Use LTI 1.3",
                default=lambda: "'lti1.3'",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "tenant_id": to_dict(self.tenant_id),
            "iss": to_dict(self.iss),
            "lms": to_dict(self.lms),
            "lti_version": to_dict(self.lti_version),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["CreateLTIData_1_2"], d: t.Dict[str, t.Any]
    ) -> "CreateLTIData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            tenant_id=parsed.tenant_id,
            iss=parsed.iss,
            lms=parsed.lms,
            lti_version=parsed.lti_version,
        )
        res.raw_data = d
        return res


CreateLTIData = t.Union[
    CreateLTIData_1,
    CreateLTIData_1_2,
]
CreateLTIDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(CreateLTIData_1),
        ParserFor.make(CreateLTIData_1_2),
    ),
)
