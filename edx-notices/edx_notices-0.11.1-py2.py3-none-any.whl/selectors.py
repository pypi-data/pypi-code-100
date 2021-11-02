"""
Utility functions for pulling Notice data.
"""
import datetime

from django.conf import settings

from notices.data import AcknowledgmentResponseTypes
from notices.models import AcknowledgedNotice, Notice


def get_active_notices(before_date=None):
    """
    Return a QuerySet of all active Notices.

    We don't want to show notices that have a launch date prior to a user creating an account,
    because they won't have a change to acknowledge.
    """
    active_notices = Notice.objects.filter(active=True)
    if before_date:
        return active_notices.exclude(launch_date__lte=before_date)
    return active_notices


def get_acknowledged_notices_for_user(user):
    """
    Return a QuerySet of all acknowledged Notices for a given user.
    """
    return AcknowledgedNotice.objects.filter(user=user)


def get_visible_notices(user):
    """
    Return a QuerySet of all active and unacknowledged Notices for a given user.
    """
    active_notices = get_active_notices(before_date=user.date_joined)
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

    max_snooze_days = settings.FEATURES.get("NOTICES_MAX_SNOOZE_DAYS")
    if max_snooze_days is not None:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        max_time_before_now = current_time - datetime.timedelta(days=max_snooze_days)
        acknowledged_notices = acknowledged_notices.exclude(
            response_type=AcknowledgmentResponseTypes.DISMISSED,
            created__lte=max_time_before_now,
        )

    excluded_notices = active_notices.exclude(id__in=[acked.notice.id for acked in acknowledged_notices])

    return excluded_notices
