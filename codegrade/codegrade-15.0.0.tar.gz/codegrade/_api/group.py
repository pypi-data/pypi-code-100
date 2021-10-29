"""The endpoints for group objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.any_error import AnyError
    from ..models.extended_group import ExtendedGroup
    from ..models.user_input import UserInput

_ClientT = t.TypeVar("_ClientT", bound="_BaseClient")


class GroupService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def add_member(
        self: "GroupService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "UserInput"],
        *,
        group_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ExtendedGroup":
        """Add a user (member) to a group.

        :param json_body: The body of the request. See :model:`.UserInput` for
            information about the possible fields. You can provide this data as
            a :model:`.UserInput` or as a dictionary.
        :param group_id: The id of the group the user should be added to.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The group with the newly added user.
        """

        url = "/api/v1/groups/{groupId}/member".format(groupId=group_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_group import ExtendedGroup

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedGroup)
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

    def get(
        self: "GroupService[AuthenticatedClient]",
        *,
        group_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ExtendedGroup":
        """Get a group by id.

        :param group_id: The id of the group to get.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The requested group.
        """

        url = "/api/v1/groups/{groupId}".format(groupId=group_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_group import ExtendedGroup

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedGroup)
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
