from mad_notifications.utils import notificaion_unique_file_path
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings



# Create your models here.


class EmailTemplate(models.Model):
    name = models.CharField(max_length=225, blank=False, null=False, help_text="Template Name")
    slug = models.SlugField(max_length=225, blank=False, null=False, unique=True, help_text="Unique Template identifer")
    content = models.TextField(blank=False, null=False, help_text='Templated content of the email. <a href="https://docs.djangoproject.com/en/dev/topics/templates/" target="_target">Refer to docs for more details.')
    from_email = models.CharField(max_length=225, blank=True, null=True, help_text='For example: No Reply <noreply@example.com>')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-id']


class Device(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    token = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=False, null=True)
    title = models.CharField(max_length=254, blank=False, null=False)
    content = models.TextField(blank=False, null=True)
    image = models.FileField(upload_to=notificaion_unique_file_path, blank=True, null=True)
    icon = models.FileField(upload_to=notificaion_unique_file_path, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    actions = models.JSONField(default=dict, blank=True, help_text="")
    data = models.JSONField(default=dict, blank=True, help_text="All keys and values in the dictionary must be strings.")
    template = models.ForeignKey(EmailTemplate, blank=True, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-id']