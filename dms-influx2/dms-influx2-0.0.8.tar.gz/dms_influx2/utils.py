from datetime import datetime, timedelta
from typing import Union
from dateutil.parser import parse


def timestamp_to_influx_string(timestamp: Union[str, datetime], offset: int = None) -> str:
    if type(timestamp) == str:
        timestamp = parse(timestamp)
    if offset is not None:
        timestamp = timestamp - timedelta(hours=int(offset))
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
