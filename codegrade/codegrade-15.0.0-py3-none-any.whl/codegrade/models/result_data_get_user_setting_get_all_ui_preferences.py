"""The module that defines the ``ResultDataGetUserSettingGetAllUiPreferences`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class ResultDataGetUserSettingGetAllUiPreferences:
    """ """

    rubric_editor_v2: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_mosaic_1: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_mosaic_2: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_mosaic_3: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_nobel: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_nobel_1: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_nobel_2: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_orchid: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_orchid_1: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_orchid_2: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_orchid_3: Maybe["t.Optional[bool]"] = Nothing
    no_msg_for_perfectly_normal: Maybe["t.Optional[bool]"] = Nothing

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "rubric_editor_v2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_mosaic_1",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_mosaic_2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_mosaic_3",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_nobel",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_nobel_1",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_nobel_2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_orchid",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_orchid_1",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_orchid_2",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_orchid_3",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
            rqa.OptionalArgument(
                "no_msg_for_perfectly_normal",
                rqa.Nullable(rqa.SimpleValue.bool),
                doc="",
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.rubric_editor_v2 = maybe_from_nullable(self.rubric_editor_v2)
        self.no_msg_for_mosaic_1 = maybe_from_nullable(
            self.no_msg_for_mosaic_1
        )
        self.no_msg_for_mosaic_2 = maybe_from_nullable(
            self.no_msg_for_mosaic_2
        )
        self.no_msg_for_mosaic_3 = maybe_from_nullable(
            self.no_msg_for_mosaic_3
        )
        self.no_msg_for_nobel = maybe_from_nullable(self.no_msg_for_nobel)
        self.no_msg_for_nobel_1 = maybe_from_nullable(self.no_msg_for_nobel_1)
        self.no_msg_for_nobel_2 = maybe_from_nullable(self.no_msg_for_nobel_2)
        self.no_msg_for_orchid = maybe_from_nullable(self.no_msg_for_orchid)
        self.no_msg_for_orchid_1 = maybe_from_nullable(
            self.no_msg_for_orchid_1
        )
        self.no_msg_for_orchid_2 = maybe_from_nullable(
            self.no_msg_for_orchid_2
        )
        self.no_msg_for_orchid_3 = maybe_from_nullable(
            self.no_msg_for_orchid_3
        )
        self.no_msg_for_perfectly_normal = maybe_from_nullable(
            self.no_msg_for_perfectly_normal
        )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {}
        if self.rubric_editor_v2.is_just:
            res["rubric_editor_v2"] = to_dict(self.rubric_editor_v2.value)
        if self.no_msg_for_mosaic_1.is_just:
            res["no_msg_for_mosaic_1"] = to_dict(
                self.no_msg_for_mosaic_1.value
            )
        if self.no_msg_for_mosaic_2.is_just:
            res["no_msg_for_mosaic_2"] = to_dict(
                self.no_msg_for_mosaic_2.value
            )
        if self.no_msg_for_mosaic_3.is_just:
            res["no_msg_for_mosaic_3"] = to_dict(
                self.no_msg_for_mosaic_3.value
            )
        if self.no_msg_for_nobel.is_just:
            res["no_msg_for_nobel"] = to_dict(self.no_msg_for_nobel.value)
        if self.no_msg_for_nobel_1.is_just:
            res["no_msg_for_nobel_1"] = to_dict(self.no_msg_for_nobel_1.value)
        if self.no_msg_for_nobel_2.is_just:
            res["no_msg_for_nobel_2"] = to_dict(self.no_msg_for_nobel_2.value)
        if self.no_msg_for_orchid.is_just:
            res["no_msg_for_orchid"] = to_dict(self.no_msg_for_orchid.value)
        if self.no_msg_for_orchid_1.is_just:
            res["no_msg_for_orchid_1"] = to_dict(
                self.no_msg_for_orchid_1.value
            )
        if self.no_msg_for_orchid_2.is_just:
            res["no_msg_for_orchid_2"] = to_dict(
                self.no_msg_for_orchid_2.value
            )
        if self.no_msg_for_orchid_3.is_just:
            res["no_msg_for_orchid_3"] = to_dict(
                self.no_msg_for_orchid_3.value
            )
        if self.no_msg_for_perfectly_normal.is_just:
            res["no_msg_for_perfectly_normal"] = to_dict(
                self.no_msg_for_perfectly_normal.value
            )
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ResultDataGetUserSettingGetAllUiPreferences"],
        d: t.Dict[str, t.Any],
    ) -> "ResultDataGetUserSettingGetAllUiPreferences":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            rubric_editor_v2=parsed.rubric_editor_v2,
            no_msg_for_mosaic_1=parsed.no_msg_for_mosaic_1,
            no_msg_for_mosaic_2=parsed.no_msg_for_mosaic_2,
            no_msg_for_mosaic_3=parsed.no_msg_for_mosaic_3,
            no_msg_for_nobel=parsed.no_msg_for_nobel,
            no_msg_for_nobel_1=parsed.no_msg_for_nobel_1,
            no_msg_for_nobel_2=parsed.no_msg_for_nobel_2,
            no_msg_for_orchid=parsed.no_msg_for_orchid,
            no_msg_for_orchid_1=parsed.no_msg_for_orchid_1,
            no_msg_for_orchid_2=parsed.no_msg_for_orchid_2,
            no_msg_for_orchid_3=parsed.no_msg_for_orchid_3,
            no_msg_for_perfectly_normal=parsed.no_msg_for_perfectly_normal,
        )
        res.raw_data = d
        return res
