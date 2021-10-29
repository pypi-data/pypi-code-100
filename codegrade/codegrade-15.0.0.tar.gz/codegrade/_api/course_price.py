"""The endpoints for course_price objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.any_error import AnyError
    from ..models.start_payment_course_price_data import (
        StartPaymentCoursePriceData,
    )
    from ..models.started_transaction import StartedTransaction

_ClientT = t.TypeVar("_ClientT", bound="_BaseClient")


class CoursePriceService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def start_payment(
        self: "CoursePriceService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "StartPaymentCoursePriceData"],
        *,
        price_id: "str",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "StartedTransaction":
        """Create a new payment for the current user.

        :param json_body: The body of the request. See
            :model:`.StartPaymentCoursePriceData` for information about the
            possible fields. You can provide this data as a
            :model:`.StartPaymentCoursePriceData` or as a dictionary.
        :param price_id: The price you want to pay for.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A transaction for this course price with a `stripe_url` key
                  that can be used to pay. Be careful to check the state of the
                  transaction, as a payment might already be in progress.
        """

        url = "/api/v1/course_prices/{priceId}/pay".format(priceId=price_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.started_transaction import StartedTransaction

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(StartedTransaction)
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
