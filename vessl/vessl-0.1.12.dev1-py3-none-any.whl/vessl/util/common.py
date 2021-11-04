from datetime import datetime, timezone

import timeago


def parse_time_to_ago(dt: datetime):
    if not dt:
        return "N/A"
    return timeago.format(dt, datetime.now(timezone.utc))


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
