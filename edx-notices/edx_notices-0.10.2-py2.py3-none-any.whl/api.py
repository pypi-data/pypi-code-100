"""
Python API for Notice data.
"""
from django.conf import settings
from rest_framework.reverse import reverse

from notices.models import AcknowledgedNotice
from notices.selectors import get_visible_notices


def get_unacknowledged_notices_for_user(user, in_app=False, request=None):
    """
    Retrieve a list of all unacknowledged (active) Notices for a given user.

    Returns:
        (list): A (text) list of URLs to the unack'd Notices.
    """
    unacknowledged_active_notices = get_visible_notices(user)

    urls = []
    if unacknowledged_active_notices:
        urls = [
            reverse("notices:notice-detail", kwargs={"pk": notice.id}, request=request)
            + ("?mobile=true" if in_app else "")
            for notice in unacknowledged_active_notices
        ]

    return urls


def can_dismiss(user, notice):
    """
    Determine whether or not the dismiss should be visible.
    """
    try:
        acknowledged_notice = AcknowledgedNotice.objects.get(user=user, notice=notice)
    except AcknowledgedNotice.DoesNotExist:
        return True

    snooze_limit = settings.FEATURES.get("NOTICES_SNOOZE_COUNT_LIMIT")
    if snooze_limit is not None and acknowledged_notice.snooze_count < snooze_limit:
        return True
    return False
