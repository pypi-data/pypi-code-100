import datetime

from django.db.models import Case, When
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.html import escape
from django.utils.safestring import mark_safe


class RenderMixin:
    """
    Миксин, добалвяющий возможность рендера шаблона
    """

    template_name = None
    context_object_name = None

    def __str__(self):
        if self.template_name:
            return self.render()
        return super().__str__()

    def render(self):
        """
        Рендер шаблона
        """
        return mark_safe(render_to_string(self.get_template_name(), self.get_context_data()))

    def get_template_name(self):
        """
        Шаблон
        """
        return self.template_name

    def get_context_data(self):
        """
        Контекст шаблона
        """
        return {
            self.context_object_name: self,
        }


def format_date(date, format='d.m.Y', default=''):
    """
    Возвращает отформатированную дату
    :param date: Дата
    :param format: смотри https://docs.djangoproject.com/en/2.2/ref/templates/builtins/#date
    :param default: вернётся, если нет date
    :return:
    """

    if date is not None:
        if isinstance(date, datetime.datetime) and timezone.is_aware(date):
            date = timezone.localtime(date)
        return date_format(date, format)
    return default


def prepare_attrs(attrs, prefix='') -> str:
    """
    Подготовка атрибутов для вывода в шаблоне
    :param attrs: {'attribute': 'value'}
    :param prefix: 'data'
    :return: ' data-attribute="value"'
    """
    prefix = prefix and f'{prefix}-' or ''
    return ' '.join(f'{prefix}{key.replace("_", "-")}="{escape(value)}"' for key, value in attrs.items())


def order_by_list(queryset, key, values_list):
    """
    Упорядочивание объектов queryset в порядке, определенном в списке
    :param queryset: Queryset для упорядочивания
    :param key: поле, по которому необходимо упорядочить
    :param values_list: список значений, по которым необходимо упорядочить
    :return: Упорядоченный queryset
    """
    order = Case(*[When(**{key: value, 'then': position}) for position, value in enumerate(values_list)])
    return queryset.order_by(order)

