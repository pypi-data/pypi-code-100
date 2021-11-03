from django import template
from django.conf import settings
from django.contrib.admin.models import LogEntry

register = template.Library()

@register.simple_tag
def site_name():
    return settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'FrontAdmin'

@register.inclusion_tag('elements/logo.html')
def logo(defaut=True):
    return {
        'site_name': settings.SITE_NAME if hasattr(settings, 'SITE_NAME') else 'FrontAdmin',
        'default': defaut
    }

@register.inclusion_tag('elements/sidebar.html')
def sidebar():
    pass

@register.inclusion_tag('elements/warnings_recent_content.html')
def warnings_recent_content():
    entries = LogEntry.objects.all().order_by('-id')[:10]
    return {
        'log_entries': entries
    }