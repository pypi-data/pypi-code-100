from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

import uuid


# Create your models here.

class ConnectedAccountBacklog(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_("User"), on_delete=models.CASCADE)
    token = models.CharField(max_length=200, verbose_name=_("Token"), blank=True, null=True, default=str(uuid.uuid4())[:15])
    summary = models.TextField(verbose_name=_("Summary"), blank=True, null=True)

    def __str__(self) -> str:
        return str(self.token+"--"+self.user.username)