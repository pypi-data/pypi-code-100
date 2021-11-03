from django import template
from django.conf import settings
import json

register = template.Library()

@register.simple_tag
def site_name():
    return settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'AdminLTE'

@register.inclusion_tag('elements/logo.html')
def logo(defaut=True):
    return {
        'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'AdminLTE',
        'default': defaut
    }

@register.inclusion_tag('elements/navbar.html')
def navbar(navdata=False):
    return {
        'nav_data': json.loads(navdata) if navdata else []
    }

@register.inclusion_tag('elements/sidebar.html')
def sidebar():
    pass