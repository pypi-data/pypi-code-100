from django import template


register = template.Library()


@register.inclusion_tag('report_designer/scripts.html')
def report_designer_scripts(is_all=False):
    """
    Скрипты конструктора отчетов
    :param is_all: Загрузка всех требуюущихся скриптов
    """
    return {'is_all': is_all}


@register.inclusion_tag('report_designer/styles.html')
def report_designer_styles(is_all=False):
    """
    Стили конструктора отчетов
    :param is_all: Загрузка всех требуюущихся стилей
    """
    return {'is_all': is_all}
