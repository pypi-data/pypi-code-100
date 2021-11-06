from django import template
from django.template.base import token_kwargs
from django.template.loader import render_to_string


register = template.Library()


def _parse_tag_args(parser, token):
    """
    Парсинг тегов
    """
    return token_kwargs(token.split_contents()[1:], parser, support_legacy=True)


class BaseTemplateBlock(template.Node):
    """
    Базовый блок для вывода в шаблоне
    """

    template_name = None
    context_prefix = ''

    def __init__(self, nodelist, extra_context=None):
        self.nodelist = nodelist
        self.extra_context = extra_context or {}

    def get_template_name(self):
        return self.template_name

    def render(self, context):
        values = {
            '_'.join([self.context_prefix, key]): val.resolve(context)
            for key, val in self.extra_context.items()
        }
        return render_to_string(self.template_name, {'content': self.nodelist.render(context), **values})


class PanelNode(BaseTemplateBlock):
    """
    Блок для вывода в шаблоне
    """

    template_name = 'report_designer/core/blocks/panel.html'
    context_prefix = 'panel'


class PanelHeaderNode(BaseTemplateBlock):
    """
    Блок для вывода в шаблоне
    """

    template_name = 'report_designer/core/blocks/panel_header.html'
    context_prefix = 'panel_header'


def _panel_node(parser, token, name, node):
    """
    Блок для вывода в шаблоне
    """
    extra_context = _parse_tag_args(parser, token)
    nodelist = parser.parse((f'end{name}',))
    parser.delete_first_token()
    return node(nodelist, extra_context)


@register.tag(name='panel')
def panel(parser, token):
    """
    Блок для вывода в шаблоне
    """
    return _panel_node(parser, token, 'panel', PanelNode)


@register.tag(name='panelheader')
def panelheader(parser, token):
    """
    Блок для вывода в шаблоне (шапка страницы)
    """
    return _panel_node(parser, token, 'panelheader', PanelHeaderNode)
