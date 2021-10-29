"""The module that defines the ``StartPaymentCoursePriceData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict


@dataclass
class StartPaymentCoursePriceData_1:
    """ """

    #: We should redirect the user after the payment has completed
    mode: "t.Literal['redirect']"
    #: The location that the user should be redirected to after the transaction
    #: has been processed. This should be a valid URL that has the same origin
    #: as origin of the API.
    next_route: "str"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "mode",
                rqa.StringEnum("redirect"),
                doc=(
                    "We should redirect the user after the payment has"
                    " completed"
                ),
            ),
            rqa.RequiredArgument(
                "next_route",
                rqa.SimpleValue.str,
                doc=(
                    "The location that the user should be redirected to after"
                    " the transaction has been processed. This should be a"
                    " valid URL that has the same origin as origin of the API."
                ),
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "mode": to_dict(self.mode),
            "next_route": to_dict(self.next_route),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["StartPaymentCoursePriceData_1"], d: t.Dict[str, t.Any]
    ) -> "StartPaymentCoursePriceData_1":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            mode=parsed.mode,
            next_route=parsed.next_route,
        )
        res.raw_data = d
        return res


@dataclass
class StartPaymentCoursePriceData_1_2:
    """ """

    #: We should close the tab after the payment has completed
    mode: "t.Literal['close_tab']"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "mode",
                rqa.StringEnum("close_tab"),
                doc="We should close the tab after the payment has completed",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "mode": to_dict(self.mode),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["StartPaymentCoursePriceData_1_2"], d: t.Dict[str, t.Any]
    ) -> "StartPaymentCoursePriceData_1_2":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            mode=parsed.mode,
        )
        res.raw_data = d
        return res


StartPaymentCoursePriceData = t.Union[
    StartPaymentCoursePriceData_1,
    StartPaymentCoursePriceData_1_2,
]
StartPaymentCoursePriceDataParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(StartPaymentCoursePriceData_1),
        ParserFor.make(StartPaymentCoursePriceData_1_2),
    ),
)
