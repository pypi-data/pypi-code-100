import json
import warnings

from django import forms
from django.conf import settings
from django.contrib import admin
from django.db import OperationalError
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from front_data.models import FrontData, FAQ


class JSONEditorWidget(forms.Widget):
    template_name = 'site_data/editorJson.html'

    def __init__(self, templates=None):
        super().__init__()
        if templates is None:
            templates = []
        self.templates = templates

    def render(self, name, value, attrs=None, renderer=None):
        editor_options = {}
        context = {
            'name': name,
            'value': value,
            'templates': json.dumps(self.templates),
            'editor_options': json.dumps(editor_options),
        }
        return mark_safe(render_to_string(self.template_name, context))

    @property
    def media(self):
        css = {
            'all': [
                'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.0.0/jsoneditor.css',
            ]
        }
        js = ['https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/9.0.0/jsoneditor.js']
        return forms.Media(css=css, js=js)


class DataEditorWidget(JSONEditorWidget):
    def render(self, name, value, attrs=None, renderer=None):
        templates = self.get_context(name, value, attrs)['widget']['attrs'].get('templates')
        if not isinstance(templates, list):
            templates = []
        editor_options = {}
        context = {
            'name': name,
            'value': value,
            'templates': json.dumps(templates),
            'editor_options': json.dumps(editor_options),
        }
        return mark_safe(render_to_string(self.template_name, context))


class JSONModelAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(kwargs.get('instance'), FrontData):
            self.fields['data'].widget.attrs.update({'templates': kwargs.get('instance').templates})

    class Meta:
        model = FrontData
        fields = '__all__'
        widgets = {
            'data': DataEditorWidget,
            'templates': JSONEditorWidget(templates=[
                {
                    "text": "Template",
                    "title": "Add new template",
                    "className": "jsoneditor-type-object",
                    "field": "NewTemplate",
                    "value": {
                        "text": "",
                        "title": "",
                        "className": "jsoneditor-type-object",
                        "field": "",
                        "value": {
                            "field": "Value"
                        }
                    }
                }
            ]),
        }


@admin.register(FrontData)
class SiteDataAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            default_data = settings.DEFAULT_SITE_DATA
            if isinstance(default_data, list):
                for site_data in default_data:
                    if  site_data.get('name') and site_data.get('templates') and \
                            list(sorted(site_data.keys())) == ["data", "name", "templates"]:
                        name = site_data.get('name')
                        templates = site_data.get('templates')
                        if isinstance(name, str) and isinstance(templates, list):
                            if not FrontData.objects.filter(name=name).exists():
                                FrontData.objects.create(**site_data)
                        else:
                            print("*****name is not string or templates is not list in settings DEFAULT_SITE_DATA")
                    else:
                        print("*******Doesn't have required attributes or has extra "
                              "attributes in settings DEFAULT_SITE_DATA ********")
            else:
                print("*******Data is not list********")
        except (AttributeError, OperationalError):
            pass

    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ['name', 'data']
        }),
        ('Optionals', {
            'classes': ('collapse', 'low-z'),
            'fields': ('templates', 'user', 'created_at')
        })
    )
    list_display = ('name', 'created_at')
    form = JSONModelAdminForm
    search_fields = ['name', 'data']
    list_per_page = 20
    autocomplete_fields = ['user']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at']
    search_fields = ['question', 'answer']
    list_filter = ['created_at']
    list_per_page = 20
