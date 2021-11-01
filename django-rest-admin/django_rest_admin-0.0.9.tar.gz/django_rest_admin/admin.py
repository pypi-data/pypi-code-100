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
from .set_table_default_value import set_table_default_value
# Register your models here.



class ComputedFieldAdmin(admin.TabularInline):
    model = ComputedField

class RouteExecAdmin(admin.ModelAdmin):
    inlines = [ComputedFieldAdmin, ]
    change_list_template = "html/auto_refresh_list.html"

    def update_rest_action(self, request):
        message_to_show = update_rest(request)
        self.message_user(request, message_to_show)
        return HttpResponseRedirect("../")

    def set_table_default(self, request, id):
        #message_to_show = update_rest(request)
        message_to_show = set_table_default_value(RouteExec.objects.get(id=id))
        self.message_user(request, message_to_show)
        return HttpResponseRedirect("../../")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_rest/', self.update_rest_action),
            path('set_table_default/<int:id>/', self.set_table_default),
        ]
        return my_urls + urls

    def button_link(self, obj):
        app_base = get_app_url_base()
        button_html = """<a class="changelink" href=""" + app_base+ """%s/>OpenApi</a>"""%(obj.route)
        return format_html(button_html)

    button_link.short_description = "打开"

    def button2_link(self, obj):
        app_base = get_app_url_base('django_rest_admin_self_default_list')
        button_html = """<a class="changelink" href=set_table_default/%d/>填充</a>""" % (obj.id)
        return format_html(button_html)

    button2_link.short_description = "自动填充空项"

    list_display = ['id', 'route','button2_link',  'button_link']
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


