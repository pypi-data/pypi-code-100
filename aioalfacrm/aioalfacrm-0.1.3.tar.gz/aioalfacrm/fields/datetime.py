import datetime
import typing

from ..core import BaseField

DATE_FORMAT = '%d.%m.%Y'
ISO_DATE_FORMAT = '%Y-%m-%d'

ISO_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

DATE_FORMATS = [DATE_FORMAT, ISO_DATE_FORMAT]
DATETIME_FORMATS = [ISO_DATETIME_FORMAT]


class DateField(BaseField):
    def serialize(self, value: datetime.date) -> typing.Any:
        return value.isoformat()

    def deserialzie(self, value: typing.Any) -> typing.Optional[datetime.date]:
        if not value:
            return None
        if isinstance(value, str):
            return parse_date(value, DATE_FORMATS).date()
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value


class DateTimeField(BaseField):
    def serialize(self, value: typing.Any) -> typing.Any:
        return value.isoformat()

    def deserialzie(self, value: typing.Any) -> typing.Optional[datetime.datetime]:
        if value is None:
            return None
        if isinstance(value, str):
            return parse_date(value, DATETIME_FORMATS)
        if isinstance(value, datetime.datetime):
            return value


def parse_date(date_string: str, formats: typing.List[str]) -> datetime.datetime:
    for format_ in formats:
        try:
            date = datetime.datetime.strptime(date_string, format_)
            return date
        except:  # noqa
            pass
    raise ValueError(f'{date_string} is not date')
