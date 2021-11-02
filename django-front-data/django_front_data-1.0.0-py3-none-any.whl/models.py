from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class FrontData(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    templates = models.JSONField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Website data'
        verbose_name_plural = 'Website data'


class FAQ(models.Model):
    question = models.CharField(max_length=1023)
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'Frequently Asked Question'
        verbose_name_plural = 'Frequently Asked Questions'
