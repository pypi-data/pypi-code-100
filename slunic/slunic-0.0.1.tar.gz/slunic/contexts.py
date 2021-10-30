"""
Export Django settings to templates
https://github.com/jakubroztocil/django-settings-export

# How to use
# settings.py

SETTINGS_EXPORT = [
    'DEBUG',
    'GA_ID',
]

"""
import logging
from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from slunic.configs import app_configs

from slunic import __version__

# from slunic.permissions import is_moderator

logger = logging.getLogger(app_configs.LOGGER_NAME)


VARIABLE_NAME = getattr(
    django_settings,
    "SETTINGS_EXPORT_VARIABLE_NAME",
    "settings",
)


class SettingsExportError(ImproperlyConfigured):
    """Base error indicating misconfiguration."""


class UndefinedSettingError(SettingsExportError):
    """An undefined setting name included in SETTINGS_EXPORT."""


class UnexportedSettingError(SettingsExportError):
    """An unexported setting has been accessed from a template."""


class ExportedSettings(dict):
    def __getitem__(self, item):
        """Fail loudly if accessing a setting that is not exported."""
        try:
            return super(ExportedSettings, self).__getitem__(item)
        except KeyError:
            if hasattr(self, item):
                # Let the KeyError propagate so that Django templates
                # can access the existing attribute (e.g. `items()`).
                raise
            raise UnexportedSettingError(
                "The `{key}` setting key is not accessible"
                ' from templates: add "{key}" to'
                " `settings.SETTINGS_EXPORT` to change that.".format(key=item)
            )


def _get_exported_settings():
    exported_settings = ExportedSettings()
    for key in getattr(django_settings, "SETTINGS_EXPORT", []):
        try:
            value = getattr(django_settings, key)
        except AttributeError:
            raise UndefinedSettingError(
                '"settings.%s" is included in settings.SETTINGS_EXPORT ' "but it does not exist. " % key
            )
        exported_settings[key] = value
    return exported_settings


def export_settings(request):
    """
    The template context processor that adds settings defined in
    `SETTINGS_EXPORT` to the context. If SETTINGS_EXPORT_VARIABLE_NAME is not
    set, the context variable will be `settings`.
    """
    variable_name = getattr(
        django_settings,
        "SETTINGS_EXPORT_VARIABLE_NAME",
        "configs",
    )
    return {
        variable_name: _get_exported_settings(),
        "app_name": app_configs.APP_NAME,
        "top_menu_items": app_configs.PAGE_MENU_ITEMS,
        "theme_name": app_configs.THEME_NAME,
        "google_tracker": app_configs.GOOGLE_TRACKER,
        "version": __version__,
    }
