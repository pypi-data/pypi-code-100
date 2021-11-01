from django import template


register = template.Library()


@register.inclusion_tag('report_designer/core/blocks/preloader.html')
def preloader(is_disable=False):
    """
    Прелоадер
    todo: удалить
    :param is_disable: абсолютное позиционирование. Родительский элемент должен иметь {style: relative}
    """
    return {'is_disable': is_disable}


@register.filter
def is_list(value):
    """
    Проверка, что тип - Список
    """
    return isinstance(value, (list, tuple,))


@register.filter
def default_if_empty(value, default):
    """
    Дефолтное значение
    """
    if not value and value != 0:
        return default
    return value


@register.simple_tag
def template_string(string, *args):
    """
    Формирование строки на основании шаблона и параметров
    """
    return string % args
