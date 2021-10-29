"""The main client used by the CodeGrade API.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import abc
import getpass
import os
import sys
import typing as t
import uuid
from types import TracebackType

import httpx

from .utils import maybe_input, select_from_list

_DEFAULT_HOST = os.getenv("CG_HOST", "https://app.codegra.de")

_BaseClientT = t.TypeVar("_BaseClientT", bound="_BaseClient")

if t.TYPE_CHECKING:
    from codegrade._api.about import AboutService as _AboutService
    from codegrade._api.assignment import (
        AssignmentService as _AssignmentService,
    )
    from codegrade._api.auto_test import AutoTestService as _AutoTestService
    from codegrade._api.comment import CommentService as _CommentService
    from codegrade._api.course import CourseService as _CourseService
    from codegrade._api.course_price import (
        CoursePriceService as _CoursePriceService,
    )
    from codegrade._api.file import FileService as _FileService
    from codegrade._api.git_provider import (
        GitProviderService as _GitProviderService,
    )
    from codegrade._api.group import GroupService as _GroupService
    from codegrade._api.login_link import LoginLinkService as _LoginLinkService
    from codegrade._api.lti import LTIService as _LTIService
    from codegrade._api.oauth_provider import (
        OAuthProviderService as _OAuthProviderService,
    )
    from codegrade._api.permission import (
        PermissionService as _PermissionService,
    )
    from codegrade._api.site_settings import (
        SiteSettingsService as _SiteSettingsService,
    )
    from codegrade._api.snippet import SnippetService as _SnippetService
    from codegrade._api.submission import (
        SubmissionService as _SubmissionService,
    )
    from codegrade._api.task_result import (
        TaskResultService as _TaskResultService,
    )
    from codegrade._api.tenant import TenantService as _TenantService
    from codegrade._api.transaction import (
        TransactionService as _TransactionService,
    )
    from codegrade._api.user import UserService as _UserService
    from codegrade._api.user_setting import (
        UserSettingService as _UserSettingService,
    )


class _BaseClient:
    """A base class for keeping track of data related to the API."""

    __slots__ = (
        "__about",
        "__assignment",
        "__course",
        "__group",
        "__user",
        "__git_provider",
        "__auto_test",
        "__lti",
        "__tenant",
        "__submission",
        "__oauth_provider",
        "__permission",
        "__file",
        "__login_link",
        "__user_setting",
        "__comment",
        "__site_settings",
        "__snippet",
        "__task_result",
        "__transaction",
        "__course_price",
        "__open_level",
        "__http",
        "base_url",
    )

    def __init__(self: "_BaseClientT", base_url: str) -> None:
        # Open level makes it possible to efficiently nest the context manager.
        self.__open_level = 0
        self.base_url = base_url

        self.__about: t.Optional["_AboutService[_BaseClientT]"] = None
        self.__assignment: t.Optional[
            "_AssignmentService[_BaseClientT]"
        ] = None
        self.__course: t.Optional["_CourseService[_BaseClientT]"] = None
        self.__group: t.Optional["_GroupService[_BaseClientT]"] = None
        self.__user: t.Optional["_UserService[_BaseClientT]"] = None
        self.__git_provider: t.Optional[
            "_GitProviderService[_BaseClientT]"
        ] = None
        self.__auto_test: t.Optional["_AutoTestService[_BaseClientT]"] = None
        self.__lti: t.Optional["_LTIService[_BaseClientT]"] = None
        self.__tenant: t.Optional["_TenantService[_BaseClientT]"] = None
        self.__submission: t.Optional[
            "_SubmissionService[_BaseClientT]"
        ] = None
        self.__oauth_provider: t.Optional[
            "_OAuthProviderService[_BaseClientT]"
        ] = None
        self.__permission: t.Optional[
            "_PermissionService[_BaseClientT]"
        ] = None
        self.__file: t.Optional["_FileService[_BaseClientT]"] = None
        self.__login_link: t.Optional["_LoginLinkService[_BaseClientT]"] = None
        self.__user_setting: t.Optional[
            "_UserSettingService[_BaseClientT]"
        ] = None
        self.__comment: t.Optional["_CommentService[_BaseClientT]"] = None
        self.__site_settings: t.Optional[
            "_SiteSettingsService[_BaseClientT]"
        ] = None
        self.__snippet: t.Optional["_SnippetService[_BaseClientT]"] = None
        self.__task_result: t.Optional[
            "_TaskResultService[_BaseClientT]"
        ] = None
        self.__transaction: t.Optional[
            "_TransactionService[_BaseClientT]"
        ] = None
        self.__course_price: t.Optional[
            "_CoursePriceService[_BaseClientT]"
        ] = None
        self.__http: t.Optional[httpx.Client] = None

    def _get_headers(self) -> t.Mapping[str, str]:
        """Get headers to be used in all endpoints"""
        return {}

    @abc.abstractmethod
    def _make_http(self) -> httpx.Client:
        raise NotImplementedError

    @property
    def http(self) -> httpx.Client:
        if self.__http is None:
            self.__http = self._make_http()
        return self.__http

    def __enter__(self: _BaseClientT) -> _BaseClientT:
        if self.__open_level == 0:
            self.http.__enter__()
        self.__open_level += 1
        return self

    def __exit__(
        self,
        exc_type: t.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        self.__open_level -= 1
        if self.__open_level == 0:
            self.http.__exit__(exc_type, exc_value, traceback)
            self.__http = None

    @property
    def about(self: _BaseClientT) -> "_AboutService[_BaseClientT]":
        if self.__about is None:
            import codegrade._api.about as m

            self.__about = m.AboutService(self)
        return self.__about

    @property
    def assignment(self: _BaseClientT) -> "_AssignmentService[_BaseClientT]":
        if self.__assignment is None:
            import codegrade._api.assignment as m

            self.__assignment = m.AssignmentService(self)
        return self.__assignment

    @property
    def course(self: _BaseClientT) -> "_CourseService[_BaseClientT]":
        if self.__course is None:
            import codegrade._api.course as m

            self.__course = m.CourseService(self)
        return self.__course

    @property
    def group(self: _BaseClientT) -> "_GroupService[_BaseClientT]":
        if self.__group is None:
            import codegrade._api.group as m

            self.__group = m.GroupService(self)
        return self.__group

    @property
    def user(self: _BaseClientT) -> "_UserService[_BaseClientT]":
        if self.__user is None:
            import codegrade._api.user as m

            self.__user = m.UserService(self)
        return self.__user

    @property
    def git_provider(
        self: _BaseClientT,
    ) -> "_GitProviderService[_BaseClientT]":
        if self.__git_provider is None:
            import codegrade._api.git_provider as m

            self.__git_provider = m.GitProviderService(self)
        return self.__git_provider

    @property
    def auto_test(self: _BaseClientT) -> "_AutoTestService[_BaseClientT]":
        if self.__auto_test is None:
            import codegrade._api.auto_test as m

            self.__auto_test = m.AutoTestService(self)
        return self.__auto_test

    @property
    def lti(self: _BaseClientT) -> "_LTIService[_BaseClientT]":
        if self.__lti is None:
            import codegrade._api.lti as m

            self.__lti = m.LTIService(self)
        return self.__lti

    @property
    def tenant(self: _BaseClientT) -> "_TenantService[_BaseClientT]":
        if self.__tenant is None:
            import codegrade._api.tenant as m

            self.__tenant = m.TenantService(self)
        return self.__tenant

    @property
    def submission(self: _BaseClientT) -> "_SubmissionService[_BaseClientT]":
        if self.__submission is None:
            import codegrade._api.submission as m

            self.__submission = m.SubmissionService(self)
        return self.__submission

    @property
    def oauth_provider(
        self: _BaseClientT,
    ) -> "_OAuthProviderService[_BaseClientT]":
        if self.__oauth_provider is None:
            import codegrade._api.oauth_provider as m

            self.__oauth_provider = m.OAuthProviderService(self)
        return self.__oauth_provider

    @property
    def permission(self: _BaseClientT) -> "_PermissionService[_BaseClientT]":
        if self.__permission is None:
            import codegrade._api.permission as m

            self.__permission = m.PermissionService(self)
        return self.__permission

    @property
    def file(self: _BaseClientT) -> "_FileService[_BaseClientT]":
        if self.__file is None:
            import codegrade._api.file as m

            self.__file = m.FileService(self)
        return self.__file

    @property
    def login_link(self: _BaseClientT) -> "_LoginLinkService[_BaseClientT]":
        if self.__login_link is None:
            import codegrade._api.login_link as m

            self.__login_link = m.LoginLinkService(self)
        return self.__login_link

    @property
    def user_setting(
        self: _BaseClientT,
    ) -> "_UserSettingService[_BaseClientT]":
        if self.__user_setting is None:
            import codegrade._api.user_setting as m

            self.__user_setting = m.UserSettingService(self)
        return self.__user_setting

    @property
    def comment(self: _BaseClientT) -> "_CommentService[_BaseClientT]":
        if self.__comment is None:
            import codegrade._api.comment as m

            self.__comment = m.CommentService(self)
        return self.__comment

    @property
    def site_settings(
        self: _BaseClientT,
    ) -> "_SiteSettingsService[_BaseClientT]":
        if self.__site_settings is None:
            import codegrade._api.site_settings as m

            self.__site_settings = m.SiteSettingsService(self)
        return self.__site_settings

    @property
    def snippet(self: _BaseClientT) -> "_SnippetService[_BaseClientT]":
        if self.__snippet is None:
            import codegrade._api.snippet as m

            self.__snippet = m.SnippetService(self)
        return self.__snippet

    @property
    def task_result(self: _BaseClientT) -> "_TaskResultService[_BaseClientT]":
        if self.__task_result is None:
            import codegrade._api.task_result as m

            self.__task_result = m.TaskResultService(self)
        return self.__task_result

    @property
    def transaction(self: _BaseClientT) -> "_TransactionService[_BaseClientT]":
        if self.__transaction is None:
            import codegrade._api.transaction as m

            self.__transaction = m.TransactionService(self)
        return self.__transaction

    @property
    def course_price(
        self: _BaseClientT,
    ) -> "_CoursePriceService[_BaseClientT]":
        if self.__course_price is None:
            import codegrade._api.course_price as m

            self.__course_price = m.CoursePriceService(self)
        return self.__course_price


class Client(_BaseClient):
    """A class used to do unauthenticated requests to CodeGrade"""

    __slots__ = ()

    def _make_http(self) -> httpx.Client:
        return httpx.Client(base_url=self.base_url)


class AuthenticatedClient(_BaseClient):
    """A Client which has been authenticated for use on secured endpoints"""

    __slots__ = ("token",)

    def __init__(self, base_url: str, token: str):
        super().__init__(base_url)
        self.token = token

    def _make_http(self) -> httpx.Client:
        return httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.token}"},
        )

    @staticmethod
    def _prepare_host(host: str) -> str:
        if not host.startswith("http"):
            return "https://{}".format(host)
        elif host.startswith("http://"):
            raise ValueError("Non https:// schemes are not supported")
        else:
            return host

    @classmethod
    def get(
        cls,
        username: str,
        password: str,
        tenant: str = None,
        host: str = _DEFAULT_HOST,
    ) -> "AuthenticatedClient":
        """Get an :model:`.AuthenticatedClient` by logging in with your
        username and password.

        .. code-block:: python

        with AuthenticatedClient.get( username='my-username',
        password=os.getenv('CG_PASS'), tenant='My University', ) as client:
        print('Hi I am {}'.format(client.user.get().name)

        :param username: Your CodeGrade username.
        :param password: Your CodeGrade password, if you do not know your
            password you can set it by following `these steps.
            <https://help.codegrade.com/for-teachers/setting-up-a-password-for-my-account>`_
        :param tenant: The id or name of your tenant in CodeGrade. This is the
            name you click on the login screen.
        :param host: The CodeGrade instance you want to use.

        :returns: A client that you can use to do authenticated requests to
                  CodeGrade. We advise you to use it in combination with a
                  ``with`` block (i.e. as a contextmanager) for the highest
                  efficiency.
        """
        host = cls._prepare_host(host)

        with Client(host) as client:
            try:
                tenant_id: t.Union[str, uuid.UUID] = uuid.UUID(tenant)
            except ValueError:
                # Given tenant is not an id, find it by name
                all_tenants = client.tenant.get_all()
                if tenant is None and len(all_tenants) == 1:
                    tenant_id = all_tenants[0].id
                elif tenant is not None:
                    tenants = {t.name: t for t in all_tenants}
                    if tenant not in tenants:
                        raise KeyError(
                            'Could not find tenant "{}", known tenants are: {}'
                            .format(
                                tenant,
                                ", ".join(t.name for t in all_tenants),
                            )
                        )
                    tenant_id = tenants[tenant].id
                else:
                    raise ValueError(
                        "No tenant specified and found more than 1 tenant on"
                        " the instance. Found tenants are: {}".format(
                            ", ".join(t.name for t in all_tenants),
                        )
                    )

            res = client.user.login(
                json_body={
                    "username": username,
                    "password": password,
                    "tenant_id": tenant_id,
                }
            )

        return cls.get_with_token(
            token=res.access_token,
            host=host,
            check=False,
        )

    @classmethod
    def get_with_token(
        cls,
        token: str,
        host: str = _DEFAULT_HOST,
        *,
        check: bool = True,
    ) -> "AuthenticatedClient":
        """Get an :model:`.AuthenticatedClient` by logging with an access
        token.

        :param token: The access token you want to use to login.
        :param host: The CodeGrade instance you want to login to.
        :param check: If ``False`` we won't check if your token actually works.

        :returns: A new ``AuthenticatedClient``.
        """
        host = cls._prepare_host(host)

        res = cls(host, token)
        if check:
            try:
                res.user.get()
            except BaseException as exc:
                raise ValueError(
                    "Failed to retrieve connected user, make sure your token"
                    " has not expired"
                ) from exc
        return res

    @classmethod
    def get_from_cli(cls) -> "AuthenticatedClient":
        host = (
            maybe_input("Your instance", _DEFAULT_HOST)
            .map(cls._prepare_host)
            .try_extract(sys.exit)
        )
        with Client(host) as client:
            tenant = select_from_list(
                "Select your tenant",
                client.tenant.get_all(),
                lambda t: t.name,
            ).try_extract(sys.exit)
        username = maybe_input("Your username").try_extract(sys.exit)
        password = getpass.getpass("Your password: ")
        if not password:
            sys.exit()

        return cls.get(
            username=username, password=password, host=host, tenant=tenant.id
        )
