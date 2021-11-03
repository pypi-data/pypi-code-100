
from datetime import datetime


def tab_to_comma(contents):
    return ",".join(contents.split("\t"))


def combine_date_time_fields(row, delete=False):
    row["datetime"] = datetime.combine(row["date"], row["time"])
    if delete:
        del(row["date"], row["time"])
    return row
