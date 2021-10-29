"""
Functions to add context to LMS pages via the plugins context feature.
"""
from notices.api import get_unacknowledged_notices_for_user
from notices.toggles import ENABLE_NOTICES


def get_dashboard_context(existing_context):
    """
    Return additional context for the course dashboard.
    """
    user = existing_context.get("user")

    data = None
    if ENABLE_NOTICES.is_enabled() and user:
        data = get_unacknowledged_notices_for_user(user)

    return {
        "unacknowledged_notices": data,
    }
