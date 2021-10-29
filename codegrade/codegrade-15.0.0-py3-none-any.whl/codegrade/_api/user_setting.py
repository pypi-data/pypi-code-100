"""The endpoints for user_setting objects.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""
import typing as t

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from .. import parsers, utils

if t.TYPE_CHECKING:
    from ..client import AuthenticatedClient, _BaseClient
    from ..models.any_error import AnyError
    from ..models.notification_setting import NotificationSetting
    from ..models.patch_notification_setting_user_setting_data import (
        PatchNotificationSettingUserSettingData,
    )
    from ..models.patch_ui_preference_user_setting_data import (
        PatchUiPreferenceUserSettingData,
    )
    from ..models.result_data_get_user_setting_get_all_ui_preferences import (
        ResultDataGetUserSettingGetAllUiPreferences,
    )

_ClientT = t.TypeVar("_ClientT", bound="_BaseClient")


class UserSettingService(t.Generic[_ClientT]):
    __slots__ = ("__client",)

    def __init__(self, client: "_BaseClient") -> None:
        self.__client = client

    def get_all_notification_settings(
        self,
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "NotificationSetting":
        """Update preferences for notifications.

        :param token: The token with which you want to get the preferences, if
            not given the preferences are retrieved for the currently logged in
            user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """

        url = "/api/v1/settings/notification_settings/"
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(t.cast(t.Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.notification_setting import NotificationSetting

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(NotificationSetting)
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

    def patch_notification_setting(
        self,
        json_body: t.Union[
            dict, list, "PatchNotificationSettingUserSettingData"
        ],
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Update preferences for notifications.

        :param json_body: The body of the request. See
            :model:`.PatchNotificationSettingUserSettingData` for information
            about the possible fields. You can provide this data as a
            :model:`.PatchNotificationSettingUserSettingData` or as a
            dictionary.
        :param token: The token with which you want to update the preferences,
            if not given the preferences are updated for the currently logged
            in user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """

        url = "/api/v1/settings/notification_settings/"
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(t.cast(t.Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

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

    def get_ui_preference(
        self,
        *,
        name: "str",
        token: Maybe["str"] = Nothing,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "t.Optional[bool]":
        """Get a single UI preferences.

        :param name: The preference name you want to get.
        :param token: The token with which you want to get the preferences, if
            not given the preferences are retrieved for the currently logged in
            user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """

        url = "/api/v1/settings/ui_preferences/{name}".format(name=name)
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(t.cast(t.Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            # fmt: on
            return parsers.JsonResponseParser(
                rqa.Nullable(rqa.SimpleValue.bool)
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

    def get_all_ui_preferences(
        self,
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "ResultDataGetUserSettingGetAllUiPreferences":
        """Get ui preferences.

        :param token: The token with which you want to get the preferences, if
            not given the preferences are retrieved for the currently logged in
            user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: The preferences for the user as described by the `token`.
        """

        url = "/api/v1/settings/ui_preferences/"
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(t.cast(t.Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

        with self.__client as client:
            resp = client.http.get(url=url, params=params)
        utils.log_warnings(resp)

        if utils.response_code_matches(resp.status_code, 200):
            # fmt: off
            from ..models.result_data_get_user_setting_get_all_ui_preferences import (
                ResultDataGetUserSettingGetAllUiPreferences,
            )

            # fmt: on
            return parsers.JsonResponseParser(
                parsers.ParserFor.make(
                    ResultDataGetUserSettingGetAllUiPreferences
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

    def patch_ui_preference(
        self,
        json_body: t.Union[dict, list, "PatchUiPreferenceUserSettingData"],
        *,
        token: Maybe["str"] = Nothing,
        extra_parameters: t.Mapping[
            str, t.Union[str, bool, int, float]
        ] = None,
    ) -> "None":
        """Update ui preferences.

        :param json_body: The body of the request. See
            :model:`.PatchUiPreferenceUserSettingData` for information about
            the possible fields. You can provide this data as a
            :model:`.PatchUiPreferenceUserSettingData` or as a dictionary.
        :param token: The token with which you want to update the preferences,
            if not given the preferences are updated for the currently logged
            in user.
        :param extra_parameters: The extra query parameters you might want to
            add. By default no extra query parameters are added.

        :returns: Nothing.
        """

        url = "/api/v1/settings/ui_preferences/"
        params: t.Dict[str, t.Any] = {
            **(extra_parameters or {}),
        }
        maybe_from_nullable(t.cast(t.Any, token)).if_just(
            lambda val: params.__setitem__("token", val)
        )

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
