from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join

from huscy.subjects import models, services


class AddressAdmin(admin.ModelAdmin):
    list_display = 'id', 'country', 'city', 'zip_code', 'street'
    search_fields = 'city', 'zip_code', 'street'


class ContactAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_of_birth'
    list_display = ('display_name', 'last_name', 'first_name', 'gender', 'date_of_birth',
                    'address', 'email')
    list_filter = 'gender', 'address__city'
    readonly_fields = 'address',
    search_fields = ('last_name', 'first_name', 'display_name', 'address__city',
                     'address__zip_code', 'address__street', 'email')


class SubjectAdmin(admin.ModelAdmin):
    fields = 'contact', 'guardians'
    list_display = ('id', '_display_name', '_date_of_birth', 'age_in_years',
                    'is_child', 'is_patient', '_guardians')
    readonly_fields = 'contact',
    search_fields = 'contact__display_name',

    def _display_name(self, subject):
        return subject.contact.display_name
    _display_name.admin_order_field = 'contact__display_name'

    def _date_of_birth(self, subject):
        return subject.contact.date_of_birth
    _date_of_birth.admin_order_field = 'contact__date_of_birth'

    def _guardians(self, subject):
        return format_html_join(', ', '<a href="{}">{}</a>', [
            (reverse('admin:subjects_contact_change', args=[guardian.id]), guardian.display_name)
            for guardian in subject.guardians.all()
        ])


class ChildAdmin(admin.ModelAdmin):
    search_fields = 'subject__contact__display_name', 'subject__id'

    def has_change_permission(self, request, obj=None):
        return False


class PatientAdmin(admin.ModelAdmin):
    search_fields = 'subject__contact__display_name', 'subject__id'

    def has_change_permission(self, request, obj=None):
        return False


class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    fields = 'subject', 'option', 'text', 'creator', 'created_at'
    list_display = 'subject', 'option', 'text', 'creator', 'created_at'
    list_filter = 'option',
    readonly_fields = 'creator', 'created_at'
    search_fields = 'subject__contact__display_name', 'subject__id'

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, note, form, change):
        services.create_note(note.subject, request.user, note.option, note.text)


class InactivityAdmin(admin.ModelAdmin):
    list_display = 'subject', 'until'
    search_fields = 'subject__contact__display_name', 'subject__id'

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, inactivity, form, change):
        services.set_inactivity(inactivity.subject, inactivity.until)


admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Child, ChildAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Inactivity, InactivityAdmin)
admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Subject, SubjectAdmin)
