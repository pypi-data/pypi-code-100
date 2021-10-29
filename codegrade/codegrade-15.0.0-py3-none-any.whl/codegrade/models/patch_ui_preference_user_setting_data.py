"""The module that defines the ``PatchUiPreferenceUserSettingData`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..utils import to_dict
from .ui_preference_name import UIPreferenceName


@dataclass
class PatchUiPreferenceUserSettingData:
    """Input data required for the `User Setting::PatchUiPreference` operation."""

    #: The ui preference you want to change.
    name: "UIPreferenceName"
    #: The new value of the preference.
    value: "bool"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "name",
                rqa.EnumValue(UIPreferenceName),
                doc="The ui preference you want to change.",
            ),
            rqa.RequiredArgument(
                "value",
                rqa.SimpleValue.bool,
                doc="The new value of the preference.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "name": to_dict(self.name),
            "value": to_dict(self.value),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["PatchUiPreferenceUserSettingData"], d: t.Dict[str, t.Any]
    ) -> "PatchUiPreferenceUserSettingData":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            name=parsed.name,
            value=parsed.value,
        )
        res.raw_data = d
        return res
