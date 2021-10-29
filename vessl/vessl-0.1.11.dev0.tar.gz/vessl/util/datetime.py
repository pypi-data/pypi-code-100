from datetime import datetime, timezone

import timeago


def parse_time_to_ago(dt: datetime):
    if not dt:
        return "N/A"
    return timeago.format(dt, datetime.now(timezone.utc))
