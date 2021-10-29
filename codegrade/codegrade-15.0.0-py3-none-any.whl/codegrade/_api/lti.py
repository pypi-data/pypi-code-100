"""The endpoints for lti objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.any_error import AnyError
    from ..models.create_lti_data import CreateLTIData
    from ..models.finalized_lti1p1_provider import FinalizedLTI1p1Provider
    from ..models.finalized_lti1p3_provider import FinalizedLTI1p3Provider
    from ..models.non_finalized_lti1p1_provider import (
        NonFinalizedLTI1p1Provider,
    )
    from ..models.non_finalized_lti1p3_provider import (
        NonFinalizedLTI1p3Provider,
    )

_ClientT = t.TypeVar("_ClientT", bound="_BaseClient")


class LTIService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def create(
        self: "LTIService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateLTIData"],
        *,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Union[NonFinalizedLTI1p3Provider, NonFinalizedLTI1p1Provider, FinalizedLTI1p3Provider, FinalizedLTI1p1Provider]":
        """Create a new LTI 1.1 or 1.3 provider.

        This route is part of the public API.

        :param json_body: The body of the request. See :model:`.CreateLTIData`
            for information about the possible fields. You can provide this
            data as a :model:`.CreateLTIData` or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The just created provider.
        """

        url = "/api/v1/lti1.3/providers/"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.finalized_lti1p1_provider import (
                FinalizedLTI1p1Provider,
            )
            from ..models.finalized_lti1p3_provider import (
                FinalizedLTI1p3Provider,
            )
            from ..models.non_finalized_lti1p1_provider import (
                NonFinalizedLTI1p1Provider,
            )
            from ..models.non_finalized_lti1p3_provider import (
                NonFinalizedLTI1p3Provider,
            )

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.make_union(
                    parsers.ParserFor.make(NonFinalizedLTI1p3Provider),
                    parsers.ParserFor.make(NonFinalizedLTI1p1Provider),
                    parsers.ParserFor.make(FinalizedLTI1p3Provider),
                    parsers.ParserFor.make(FinalizedLTI1p1Provider),
                )
            ).try_parse(resp)

        from ..models.any_error import AnyError

        raise utils.get_error(
            resp,
            (
                (
                    (400, 409, 401, 403, 404, "5XX"),
                    utils.unpack_union(AnyError),
                ),
            ),
        )
