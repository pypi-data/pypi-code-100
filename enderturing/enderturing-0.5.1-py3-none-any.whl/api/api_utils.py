from datetime import date, datetime
from typing import Union


def _to_date_range(from_date: Union[str, datetime, date], to_date: Union[str, datetime, date]) -> Union[str, None]:
    if not from_date and not to_date:
        return None
    start = from_date
    end = to_date
    if isinstance(start, datetime) or isinstance(start, date):
        start = start.isoformat()
    if isinstance(end, datetime) or isinstance(end, date):
        end = end.isoformat()
    res = start
    if end:
        res += ";" + end
    return res
