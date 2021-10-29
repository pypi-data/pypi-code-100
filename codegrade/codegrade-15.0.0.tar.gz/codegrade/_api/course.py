"""The endpoints for course objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing

from .. import parsers, utils

if t.TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.any_error import AnyError
    from ..models.assignment import Assignment
    from ..models.change_user_role_course_data import ChangeUserRoleCourseData
    from ..models.course_perm_map import CoursePermMap
    from ..models.course_price import CoursePrice
    from ..models.course_registration_link import CourseRegistrationLink
    from ..models.course_snippet import CourseSnippet
    from ..models.create_assignment_course_data import (
        CreateAssignmentCourseData,
    )
    from ..models.create_course_data import CreateCourseData
    from ..models.create_group_set_course_data import CreateGroupSetCourseData
    from ..models.create_snippet_course_data import CreateSnippetCourseData
    from ..models.email_users_course_data import EmailUsersCourseData
    from ..models.extended_course import ExtendedCourse
    from ..models.extended_work import ExtendedWork
    from ..models.group_set import GroupSet
    from ..models.import_into_course_data import ImportIntoCourseData
    from ..models.job import Job
    from ..models.patch_course_data import PatchCourseData
    from ..models.patch_snippet_course_data import PatchSnippetCourseData
    from ..models.put_enroll_link_course_data import PutEnrollLinkCourseData
    from ..models.put_price_course_data import PutPriceCourseData
    from ..models.user import User
    from ..models.user_course import UserCourse

_ClientT = t.TypeVar("_ClientT", bound="_BaseClient")


class CourseService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all(
        self: "CourseService[AuthenticatedClient]",
        *,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Sequence[ExtendedCourse]":
        """Return all Course objects the current user is a member of.

        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized courses
        """

        url = "/api/v1/courses/"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course import ExtendedCourse

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(ExtendedCourse))
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

    def create(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateCourseData"],
        *,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ExtendedCourse":
        """Create a new course.

        :param json_body: The body of the request. See
            :model:`.CreateCourseData` for information about the possible
            fields. You can provide this data as a :model:`.CreateCourseData`
            or as a dictionary.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialization of the new
                  course
        """

        url = "/api/v1/courses/"
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course import ExtendedCourse

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourse)
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

    def create_snippet(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateSnippetCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "CourseSnippet":
        """Add or modify a <span
        data-role=\"class\">.models.CourseSnippet</span> by key.

        :param json_body: The body of the request. See
            :model:`.CreateSnippetCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.CreateSnippetCourseData` or as a dictionary.
        :param course_id: The id of the course in which you want to create a
            new snippet.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized snippet and return
                  code 201.
        """

        url = "/api/v1/courses/{courseId}/snippet".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 201):
            # fmt: off
            from ..models.course_snippet import CourseSnippet

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(CourseSnippet)
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

    def get_group_sets(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Sequence[GroupSet]":
        """Get the all the group sets of a given course.

        :param course_id: The id of the course of which the group sets should
            be retrieved.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A list of group sets.
        """

        url = "/api/v1/courses/{courseId}/group_sets/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.group_set import GroupSet

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(GroupSet))
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

    def create_group_set(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateGroupSetCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "GroupSet":
        """Create or update a GroupSet in the given course id.

        :param json_body: The body of the request. See
            :model:`.CreateGroupSetCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.CreateGroupSetCourseData` or as a dictionary.
        :param course_id: The id of the course in which the group set should be
            created or updated. The course id of a group set cannot change.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The created or updated group.
        """

        url = "/api/v1/courses/{courseId}/group_sets/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.group_set import GroupSet

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(GroupSet)
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

    def create_assignment(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "CreateAssignmentCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "Assignment":
        """Create a new course for the given assignment.

        :param json_body: The body of the request. See
            :model:`.CreateAssignmentCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.CreateAssignmentCourseData` or as a dictionary.
        :param course_id: The course to create an assignment in.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The newly created assignment.
        """

        url = "/api/v1/courses/{courseId}/assignments/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.assignment import Assignment

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(Assignment)
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

    def put_enroll_link(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "PutEnrollLinkCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "CourseRegistrationLink":
        """Create or edit an enroll link.

        :param json_body: The body of the request. See
            :model:`.PutEnrollLinkCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.PutEnrollLinkCourseData` or as a dictionary.
        :param course_id: The id of the course in which this link should enroll
            users.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The created or edited link.
        """

        url = "/api/v1/courses/{courseId}/registration_links/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.course_registration_link import CourseRegistrationLink

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(CourseRegistrationLink)
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

    def put_price(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "PutPriceCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "CoursePrice":
        """Update the price of the given course.

        :param json_body: The body of the request. See
            :model:`.PutPriceCourseData` for information about the possible
            fields. You can provide this data as a :model:`.PutPriceCourseData`
            or as a dictionary.
        :param course_id: The id of the course for which you want to update the
            price.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The created or updated price.
        """

        url = "/api/v1/courses/{courseId}/price".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.course_price import CoursePrice

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(CoursePrice)
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

    def delete_price(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Update the price of the given course.

        :param course_id: The id of the course for which you want to update the
            price.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The created or updated price.
        """

        url = "/api/v1/courses/{courseId}/price".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.delete(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

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

    def delete_snippet(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        snippet_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Delete the <span data-role=\"class\">.models.CourseSnippet</span>
        with the given id.

        :param course_id: The id of the course in which the snippet is located.
        :param snippet_id: The id of the snippet
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204
        """

        url = "/api/v1/courses/{courseId}/snippets/{snippetId}".format(
            courseId=course_id, snippetId=snippet_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.delete(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

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

    def patch_snippet(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "PatchSnippetCourseData"],
        *,
        course_id: "int",
        snippet_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Modify the <span data-role=\"class\">.models.CourseSnippet</span>
        with the given id.

        :param json_body: The body of the request. See
            :model:`.PatchSnippetCourseData` for information about the possible
            fields. You can provide this data as a
            :model:`.PatchSnippetCourseData` or as a dictionary.
        :param course_id: The id of the course in which the course snippet is
            saved.
        :param snippet_id: The id of the snippet to change.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204.
        """

        url = "/api/v1/courses/{courseId}/snippets/{snippetId}".format(
            courseId=course_id, snippetId=snippet_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.patch(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

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

    def delete_role(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        role_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Remove a CourseRole from the given Course.

        :param course_id: The id of the course
        :param role_id: The id of the role you want to delete
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An empty response with return code 204
        """

        url = "/api/v1/courses/{courseId}/roles/{roleId}".format(
            courseId=course_id, roleId=role_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.delete(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

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

    def get_all_users(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Union[t.Sequence[User], t.Sequence[UserCourse]]":
        """Return a list of all <span data-role=\"class\">.models.User</span>
        objects and their

        :param course_id: The id of the course
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized users and course
                  roles
        """

        url = "/api/v1/courses/{courseId}/users/".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.user import User
            from ..models.user_course import UserCourse

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.make_union(
                    rqa.List(parsers.ParserFor.make(User)),
                    rqa.List(parsers.ParserFor.make(UserCourse)),
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

    def change_user_role(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "ChangeUserRoleCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> t.Union["UserCourse", "None"]:
        """Set the `CourseRole` of a user in the given course.

        :param json_body: The body of the request. See
            :model:`.ChangeUserRoleCourseData` for information about the
            possible fields. You can provide this data as a
            :model:`.ChangeUserRoleCourseData` or as a dictionary.
        :param course_id: The id of the course in which you want to enroll a
            new user, or change the role of an existing user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: If the user\_id parameter is set in the request the response
                  will be empty with return code 204. Otherwise the response
                  will contain the JSON serialized user and course role with
                  return code 201
        """

        url = "/api/v1/courses/{courseId}/users/".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.put(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.user_course import UserCourse

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(UserCourse)
            ).try_parse(resp)
        if utils.response_code_matches(resp.status_code, 204):
            # fmt: off
            # fmt: on
            return parsers.ConstantlyParser(None).try_parse(resp)

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
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ExtendedCourse":
        """Get a course by id.

        :param course_id: The id of the course
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A response containing the JSON serialized course
        """

        url = "/api/v1/courses/{courseId}".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course import ExtendedCourse

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourse)
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

    def patch(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "PatchCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ExtendedCourse":
        """Update the given course with new values.

        :param json_body: The body of the request. See
            :model:`.PatchCourseData` for information about the possible
            fields. You can provide this data as a :model:`.PatchCourseData` or
            as a dictionary.
        :param course_id: The id of the course you want to update.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated course, in extended format.
        """

        url = "/api/v1/courses/{courseId}".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.patch(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course import ExtendedCourse

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourse)
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

    def get_snippets(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Sequence[CourseSnippet]":
        """Get all snippets of the given course.

        :param course_id: The id of the course from which you want to get the
            snippets.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: An array containing all snippets for the given course.
        """

        url = "/api/v1/courses/{courseId}/snippets/".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.course_snippet import CourseSnippet

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.List(parsers.ParserFor.make(CourseSnippet))
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

    def get_permissions(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "CoursePermMap":
        """Get all the permissions of the currently logged in user in this
        course.

        This will return the permission as if you have already paid, even if
        this is not the case.

        :param course_id: The id of the course of which the permissions should
            be retrieved.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A mapping between the permission name and a boolean
                  indicating if the currently logged in user has this
                  permission.
        """

        url = "/api/v1/courses/{courseId}/permissions/".format(
            courseId=course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.course_perm_map import CoursePermMap

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(CoursePermMap)
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

    def get_submissions_by_user(
        self: "CourseService[AuthenticatedClient]",
        *,
        course_id: "int",
        user_id: "int",
        latest_only: "bool" = False,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Mapping[str, t.Sequence[ExtendedWork]]":
        """Get all submissions by the given user in this course.

        :param course_id: The id of the course from which you want to get the
            submissions.
        :param user_id: The id of the user of which you want to get the
            submissions.
        :param latest_only: Only get the latest submission of a user. Please
            use this option if at all possible, as students have a tendency to
            submit many attempts and that can make this route quite slow.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A mapping between assignment id and the submissions done in
                  that assignment by the given user. If the `latest_only` query
                  parameter was used the value will still be an array of
                  submissions, but the length will always be one. If the user
                  didn't submit for an assignment the value might be empty or
                  the id of the assignment will be missing from the returned
                  object.
        """

        url = "/api/v1/courses/{courseId}/users/{userId}/submissions/".format(
            courseId=course_id, userId=user_id
        )
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
            "latest_only": utils.to_dict(latest_only),
        }

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_work import ExtendedWork

            # fmt: on
            return parsers.JsonResponseParser(
                rqa.LookupMapping(
                    rqa.List(parsers.ParserFor.make(ExtendedWork))
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

    def import_into(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "ImportIntoCourseData"],
        *,
        into_course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ExtendedCourse":
        """Copy a course into another course.

        :param json_body: The body of the request. See
            :model:`.ImportIntoCourseData` for information about the possible
            fields. You can provide this data as a
            :model:`.ImportIntoCourseData` or as a dictionary.
        :param into_course_id: The course you want to import into.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The updated course, so the course of which the id was passed
                  in the url.
        """

        url = "/api/v1/courses/{intoCourseId}/copy".format(
            intoCourseId=into_course_id
        )
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.extended_course import ExtendedCourse

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(ExtendedCourse)
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

    def email_users(
        self: "CourseService[AuthenticatedClient]",
        json_body: t.Union[dict, list, "EmailUsersCourseData"],
        *,
        course_id: "int",
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "Job":
        """Sent the authors in this course an email.

        :param json_body: The body of the request. See
            :model:`.EmailUsersCourseData` for information about the possible
            fields. You can provide this data as a
            :model:`.EmailUsersCourseData` or as a dictionary.
        :param course_id: The id of the course in which you want to send the
            emails.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: A task result that will send these emails.
        """

        url = "/api/v1/courses/{courseId}/email".format(courseId=course_id)
        params = extra_parameters or {}

        with self.__client as client:
            resp = client.http.post(
                url=url, json=utils.to_dict(json_body), params=params
            )
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.job import Job

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(Job)
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
