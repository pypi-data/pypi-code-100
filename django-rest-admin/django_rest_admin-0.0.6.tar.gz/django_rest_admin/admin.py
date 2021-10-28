from django.contrib import admin
from .models import RouteExec,ComputedField
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, include
from django.http import HttpResponse,HttpResponseRedirect

from .update_models import update_models
from .json_widget import JsonEditorWidget, CodeEditorWidget
from .model_field import JSONField, CodeField
from .update_rest import update_rest
from .get_app_url_base import get_app_url_base

# Register your models here.



class ComputedFieldAdmin(admin.TabularInline):
    model = ComputedField

class RouteExecAdmin(admin.ModelAdmin):
    inlines = [ComputedFieldAdmin, ]
    change_list_template = "html/auto_refresh_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_rest/', self.update_rest_action),
        ]
        return my_urls + urls
    def update_rest_action(self, request):
        update_rest(request)
        return HttpResponseRedirect("../")



    def button_link(self, obj):
        app_base = get_app_url_base()
        button_html = """<a class="changelink" href=""" + app_base+ """/api%s/>OpenApi</a>"""%(obj.route)
        return format_html(button_html)

    button_link.short_description = "打开"

    list_display = ['id', 'route', 'button_link']
    formfield_overrides = {
            JSONField: {'widget': JsonEditorWidget},
            CodeField: {'widget': CodeEditorWidget},
        }

    class Media:
        css = {
            'all': ( 'django_rest_admin/jsoneditor.css',)
        }
        js = ('django_rest_admin/jsoneditor.js', 'django_rest_admin/jquery-3.6.0.min.js')


admin.site.register(RouteExec, RouteExecAdmin)


