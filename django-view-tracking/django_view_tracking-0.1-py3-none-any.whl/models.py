from django.conf import settings
from django.core import validators
from django.db import models


class ViewTrack(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="view_tracks",
    )

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    request_method = models.CharField(max_length=7)
    request_url = models.TextField(validators=[validators.URLValidator()])

    response_status_code = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.user} request on {self.timestamp}"
