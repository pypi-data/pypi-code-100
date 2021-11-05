import datetime
from functools import wraps

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


def functions_attrs_map(key, map_name='FUNCTIONS_MAP', function_by_key_name='function_by_key'):
    """
    Декоратор. Собирает словарь наименований функций по ключам.
    Функции должны быть декорированы functions_attrs с таким же ключом
    """
    def decorator(cls_obj):
        def __function_by_key(_cls, _key):
            """
            Функция по ключу
            """
            _functions_map = getattr(_cls, map_name, {})
            return _functions_map.get(_key)

        setattr(cls_obj, function_by_key_name, classmethod(__function_by_key))
        # Сбор функций
        functions_map = {}
        for func_name in dir(cls_obj):
            func = getattr(cls_obj, func_name, None)
            if func_name.startswith('__') or not func:
                continue
            if hasattr(func, '__call__'):
                map_key = getattr(func, key, None)
                if map_key:
                    functions_map[map_key] = func
        setattr(cls_obj, map_name, functions_map)
        return cls_obj
    return decorator


def functions_attrs(**attrs):
    """
    Установка аттрибутов функции
    """
    def decorator(function):
        for key, value in attrs.items():
            setattr(function, key, value)

        @wraps(function)
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs)
        return wrapper
    return decorator
