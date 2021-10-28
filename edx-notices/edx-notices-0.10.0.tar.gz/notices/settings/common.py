"""Common settings for notices app"""


def plugin_settings(settings):
    """Settings for the notices app"""
    settings.FEATURES["NOTICES_REDIRECT_ALLOWLIST"] = []
    settings.FEATURES["NOTICES_DEFAULT_REDIRECT_URL"] = "http://www.example.com"
    settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"] = "en"
    settings.FEATURES["NOTICES_SEGMENT_KEY"] = None
    settings.FEATURES["NOTICES_SNOOZE_HOURS"] = None
    settings.FEATURES["NOTICES_SNOOZE_COUNT_LIMIT"] = None
