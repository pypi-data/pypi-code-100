"""
Utility functions for pulling Notice data.
"""
import datetime

from django.conf import settings

from notices.data import AcknowledgmentResponseTypes
from notices.models import AcknowledgedNotice, Notice


def get_active_notices():
    """
    Return a QuerySet of all active Notices.
    """
    return Notice.objects.filter(active=True)


def get_acknowledged_notices_for_user(user):
    """
    Return a QuerySet of all acknowledged Notices for a given user.
    """
    return AcknowledgedNotice.objects.filter(user=user)


def get_visible_notices(user):
    """
    Return a QuerySet of all active and unacknowledged Notices for a given user.
    """
    active_notices = get_active_notices()
    acknowledged_notices = get_acknowledged_notices_for_user(user)

    snooze_hours = settings.FEATURES.get("NOTICES_SNOOZE_HOURS")
    if snooze_hours is not None:
        last_valid_datetime = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=snooze_hours)
        acknowledged_notices = acknowledged_notices.exclude(
            response_type=AcknowledgmentResponseTypes.DISMISSED, modified__lte=last_valid_datetime
        )

    snooze_limit = settings.FEATURES.get("NOTICES_SNOOZE_COUNT_LIMIT")
    if snooze_limit is not None:
        acknowledged_notices = acknowledged_notices.exclude(
            response_type=AcknowledgmentResponseTypes.DISMISSED, snooze_count__gt=snooze_limit
        )

    excluded_notices = active_notices.exclude(id__in=[acked.notice.id for acked in acknowledged_notices])

    return excluded_notices
