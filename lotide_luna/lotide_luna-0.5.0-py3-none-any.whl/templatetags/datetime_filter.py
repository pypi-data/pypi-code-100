from datetime import datetime

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def to_datetime(value):
    """Convert ISO 8601 string to datetime."""
    return datetime.fromisoformat(value)
