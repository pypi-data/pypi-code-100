"""The endpoints for comment objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.any_error import AnyError
    from ..models.comment_reply_edit import CommentReplyEdit

_ClientT = t.TypeVar("_ClientT", bound="_BaseClient")


class CommentService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all_reply_edits(
        self: "CommentService[AuthenticatedClient]",
        *,
        comment_base_id: "int",
        reply_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Sequence[CommentReplyEdit]":
        """Get the edits of a reply.

        :param comment_base_id: The base of the given reply.
        :param reply_id: The id of the reply for which you want to get the
            replies.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A list of edits, sorted from newest to oldest.
        """

        url = (
            "/api/v1/comments/{commentBaseId}/replies/{replyId}/edits/".format(
                commentBaseId=comment_base_id, replyId=reply_id
            )
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.comment_reply_edit import CommentReplyEdit

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(CommentReplyEdit))
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
