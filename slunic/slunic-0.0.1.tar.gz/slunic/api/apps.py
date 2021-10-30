from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
    name = "slunic.api"
    label = "slunic_api"
    verbose_name = _("Slunic API")
