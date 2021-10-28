from django.contrib import admin
from quartet_templates import models

@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description'
    )

def register_to_site(admin_site):
    admin_site.register(models.Template, TemplateAdmin)
