"""
    This module provides the `settings` object, that is used to access
    app settings, checking for user settings first, then falling
    back to the defaults. 'Inpired By DRF Settings'
"""
import os
from typing import Any, Dict
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string

from django.test.signals import setting_changed

SETTINGS_NAME = "SLUNIC"
SETTINGS_DOC = "https://github/realnoobs/slunic/"


SLUNIC_DEFAULTS: Dict[str, Any] = {
    "STATS_DIR": os.path.join(settings.BASE_DIR, "export", "stats"),
    "APP_NAME": "slunic",
    "THEME_NAME": "default",
    "LOGGER_NAME": "slunic",
    "GOOGLE_TRACKER": "",
    # Used for send notification
    "BOT_NAME": "slunicbot",
    "BOT_USERNAME": "slunicbot",
    "BOT_EMAIL": "slunicbot@example.com",
    "BOT_PASSWORD": "slunicbot_pwd",
    "USER_PROFILE_MODEL": getattr(settings, "SLUNIC_PROFILE_MODEL", "slunic.Profile"),
    "USER_GRAVATAR_PROVIDER_URL": "//www.gravatar.com/avatar",
    "USER_LOGIN_URL": getattr(settings, "LOGIN_URL", "login"),
    "USER_LOGOUT_URL": getattr(settings, "LOGIN_OUT", "logout"),
    "USER_SIGNUP_URL": getattr(settings, "SIGNUP_URL", "/signup/"),
    "USER_STATS_SESSION_KEY": "counts",
    "USER_MAX_AWARDS_PER_SESSION": 2,
    "USER_RECENTLY_JOINED_DAYS": 7,
    "IMAGE_UPLOAD_ENABLED": False,
    "IMAGE_UPLOAD_PATH": "content_images",
    # Used for profile score
    "LOW_REP_THRESHOLD": 0,
    "ADMIN_UPLOAD_SIZE": 1000,
    "TRUSTED_UPLOAD_SIZE": 100,
    # default upload limit
    "MAX_UPLOAD_SIZE": 10,

    "COMMENT_MIN_LENGTH": 5,
    "COMMENT_MAX_LENGTH": 1000,
    "COMMENT_MAX_LEVEL": 3,
    "COMMENTS_TIMEOUT": (60 * 60 * 2),
    ######################################################
    # CACHE
    ######################################################
    "CACHE_APP_STATS_KEY": "Slunic:App:States:%(timestamp)s",
    "CACHE_APP_STATS_TIMEOUT": 60 * 1,
    "CACHE_USER_STATS_KEY": "Slunic:User:States:%(user_id)s",
    "CACHE_USER_STATS_TIMEOUT": 60 * 1,
    "CACHE_USER_BOOKMARKS_KEY": "Slunic:User:Bookmarks",
    "CACHE_USER_BOOKMARKS_TIMEOUT": 60 * 1,
    "CACHE_PAGE_VIEW_KEY": "PageView:%(page_id)s:%(ip)s",
    "CACHE_PAGE_VIEW_TIMEOUT": 60 * 1,

    "CACHE_OBJECT_SEARCH_TIMEOUT": 60 * 1,
    "CACHE_OBJECT_LIST_TIMEOUT": 60 * 1,
    "CACHE_OBJECT_DETAIL_TIMEOUT": 60 * 1,

    ######################################################
    # HOOK NAMES
    ######################################################
    "API_VIEWS_HOOK_V1": "v1_views_hook",
    "API_VIEWSETS_HOOK_V1": "v1_viewsets_hook",
    ######################################################
    # COMPONENTS
    ######################################################
    "MODELS_FOR_LIST": ["tutorial", "question", "help", "tag", "badge", "category", "profile"],
    "MODELS_FOR_COMMENT": ["tutorial", "question", "comment"],
    "PAGE_MENU_ITEMS": [
        {"name": "tutorial", "label": _("Tutorials")},
        {"name": "question", "label": _("Questions")},
        {"name": "badge", "label": _("Badges")},
        {"name": "tag", "label": _("Tags")},
        {"name": "profile", "label": _("Users")},
        {"name": "help", "label": _("Help")},
    ],
    "EASY_MDE": {
        "autofocus": True,
        "toolbarTips": True,
        "maxHeight": "200px",
        "toolbar": [
            "heading",
            "bold",
            "italic",
            "quote",
            "link",
            "|",
            "code",
            "ordered-list",
            "unordered-list",
            "table",
            "image",
            "|",
            "preview",
            "guide",
        ],
        "placeholder": _("Type something here .."),
        "uploadImage": False,
        "sideBySideFullscreen": False,
    },
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = ["SLUNIC_PROFILE"]

# List of settings that have been removed
REMOVED_SETTINGS = []


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for SLUNIC setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg)


class AppSettings:
    """
    Settings object, that is used to access app settings, checking for user settings first,
    then falling back to the defaults.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or SLUNIC_DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "SLUNIC", {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid SLUNIC setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for setting in REMOVED_SETTINGS:
            if setting in user_settings:
                raise RuntimeError(
                    "The '%s' setting has been removed. Please refer to "
                    " '%s' for available settings." % (setting, SETTINGS_DOC)
                )
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


app_configs = AppSettings(None, SLUNIC_DEFAULTS, IMPORT_STRINGS)


def reload_slunic_configs(*args, **kwargs):
    setting = kwargs["setting"]
    if setting == "SLUNIC":
        app_configs.reload()


setting_changed.connect(reload_slunic_configs)
