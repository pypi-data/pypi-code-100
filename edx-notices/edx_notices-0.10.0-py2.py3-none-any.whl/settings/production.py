"""Production settings for notices app"""


def plugin_settings(settings):
    """Settings for the notices app"""
    settings.FEATURES["NOTICES_REDIRECT_ALLOWLIST"] = settings.ENV_TOKENS.get(
        "NOTICES_REDIRECT_ALLOWLIST", settings.FEATURES["NOTICES_REDIRECT_ALLOWLIST"]
    )
    settings.FEATURES["NOTICES_DEFAULT_REDIRECT_URL"] = settings.ENV_TOKENS.get(
        "NOTICES_DEFAULT_REDIRECT_URL", settings.FEATURES["NOTICES_DEFAULT_REDIRECT_URL"]
    )
    settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"] = settings.ENV_TOKENS.get(
        "NOTICES_FALLBACK_LANGUAGE", settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"]
    )
    settings.FEATURES["NOTICES_SNOOZE_HOURS"] = settings.ENV_TOKENS.get(
        "NOTICES_SNOOZE_HOURS", settings.FEATURES["NOTICES_SNOOZE_HOURS"]
    )
    settings.FEATURES["NOTICES_SNOOZE_COUNT_LIMIT"] = settings.ENV_TOKENS.get(
        "NOTICES_SNOOZE_COUNT_LIMIT", settings.FEATURES["NOTICES_SNOOZE_COUNT_LIMIT"]
    )
    settings.FEATURES["NOTICES_SEGMENT_KEY"] = settings.AUTH_TOKENS.get(
        "NOTICES_SEGMENT_KEY", settings.FEATURES["NOTICES_SEGMENT_KEY"]
    )
