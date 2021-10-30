"""Configuration package."""

from os.path import dirname, join
from notelist.config.settings import SettingsManager


# File paths
_dir = dirname(__file__)
_settings_path = join(_dir, "settings.json")


def get_sm() -> SettingsManager:
    """Return the settings manager.

    :returns: Settings manager.
    """
    return SettingsManager(_settings_path)
