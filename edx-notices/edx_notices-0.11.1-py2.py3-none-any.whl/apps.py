"""
notices Django application initialization.
"""

from django.apps import AppConfig


class NoticesConfig(AppConfig):
    """
    Configuration for the notices Django application.
    """

    name = "notices"

    plugin_app = {
        "url_config": {
            "lms.djangoapp": {
                "namespace": "notices",
                "regex": "^notices/",
                "relative_path": "urls",
            }
        },
        "settings_config": {
            "lms.djangoapp": {
                "production": {"relative_path": "settings.production"},
                "common": {"relative_path": "settings.common"},
            }
        },
        "view_context_config": {"lms.djangoapp": {"course_dashboard": "notices.context_api.get_dashboard_context"}},
    }
