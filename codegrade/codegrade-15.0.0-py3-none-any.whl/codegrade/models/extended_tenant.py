"""The module that defines the ``ExtendedTenant`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..utils import to_dict
from .tenant import Tenant
from .tenant_price import TenantPrice


@dataclass
class ExtendedTenant(Tenant):
    """The extended JSON representation of a tenant."""

    #: A url where you can download the default logo for this tenant. You don't
    #: need to be logged in to use this url.
    logo_default_url: "str"
    #: A url where you can download the dark logo for this tenant. You don't
    #: need to be logged in to use this url.
    logo_dark_url: "str"
    #: The price of a tenant.
    price: "t.Optional[TenantPrice]"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: Tenant.data_parser.parser.combine(
            rqa.FixedMapping(
                rqa.RequiredArgument(
                    "logo_default_url",
                    rqa.SimpleValue.str,
                    doc=(
                        "A url where you can download the default logo for"
                        " this tenant. You don't need to be logged in to use"
                        " this url."
                    ),
                ),
                rqa.RequiredArgument(
                    "logo_dark_url",
                    rqa.SimpleValue.str,
                    doc=(
                        "A url where you can download the dark logo for this"
                        " tenant. You don't need to be logged in to use this"
                        " url."
                    ),
                ),
                rqa.RequiredArgument(
                    "price",
                    rqa.Nullable(parsers.ParserFor.make(TenantPrice)),
                    doc="The price of a tenant.",
                ),
            )
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "logo_default_url": to_dict(self.logo_default_url),
            "logo_dark_url": to_dict(self.logo_dark_url),
            "price": to_dict(self.price),
            "id": to_dict(self.id),
            "name": to_dict(self.name),
            "sso_provider_id": to_dict(self.sso_provider_id),
            "statistics": to_dict(self.statistics),
            "abbreviated_name": to_dict(self.abbreviated_name),
            "order_category": to_dict(self.order_category),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["ExtendedTenant"], d: t.Dict[str, t.Any]
    ) -> "ExtendedTenant":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            logo_default_url=parsed.logo_default_url,
            logo_dark_url=parsed.logo_dark_url,
            price=parsed.price,
            id=parsed.id,
            name=parsed.name,
            sso_provider_id=parsed.sso_provider_id,
            statistics=parsed.statistics,
            abbreviated_name=parsed.abbreviated_name,
            order_category=parsed.order_category,
        )
        res.raw_data = d
        return res
