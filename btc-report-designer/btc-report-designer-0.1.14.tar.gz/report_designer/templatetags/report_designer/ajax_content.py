from django.template.loader import render_to_string
from django import template


register = template.Library()


def ajax_content_kwargs(
    base_class,
    context,
    name,
    url=None,
    auto_start=True,
    enable_preloader=True,
    preloader_class='rd-preloader',
    additional_css_classes=None,
    included_template=None,
    **data_attrs,
):
    """
    Контекст ajax-контента

    :param base_class: Базовый класс элемента
    :param context: Контекст шаблона
    :param name: Наименование динамического контента
    :param url: URL адрес загружаемого контента
    :param auto_start: Автоматическая загрузка после инициализации
    :param enable_preloader: Показывать ли прелоадер перед загрузкой
    :param preloader_class: Показывать ли прелоадер перед загрузкой
    :param additional_css_classes: Дополнительные css-классы
    :param included_template: Включаемый шаблон
    :param data_attrs: data-аттрибуты
    """
    # Идентификатор динамического контента для JS
    js_name = f'{base_class}-{name}' if not name.startswith('js') else name
    if included_template:
        included_template = render_to_string(included_template, context.flatten())

    # Подговка data-аттрибутов
    data_attrs = {
        name.replace('data_').replace("_", "-")
        for name, value in data_attrs
        if name.startswith('data_')
    }
    return {
        'base_class': base_class,
        'js_name': js_name,
        'name': name,
        'url': url,
        'auto_start': auto_start,
        'enable_preloader': enable_preloader,
        'preloader_class': preloader_class,
        'additional_css_classes': additional_css_classes,
        'included_template': included_template,
        'data_attrs': data_attrs,
    }


@register.inclusion_tag('report_designer/core/blocks/ajax_content.html', takes_context=True)
def dynamic_content(context, *args, **kwargs):
    """
    Динамический контент
    """
    return ajax_content_kwargs('js-rd-dynamic-content', context, *args, **kwargs)


@register.inclusion_tag('report_designer/core/blocks/ajax_content.html', takes_context=True)
def ajax_content(context, *args, **kwargs):
    """
    Ajax-content
    """
    is_filterable = kwargs.pop('is_filterable', False)
    content_kwargs = ajax_content_kwargs('js-rd-ajax-content', context, *args, **kwargs)
    if is_filterable:
        content_kwargs.update({'auto_start': False})
    return content_kwargs
