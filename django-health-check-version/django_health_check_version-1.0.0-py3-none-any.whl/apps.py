from django.apps import AppConfig
from health_check.plugins import plugin_dir


class DjangoHealthCheckVersionConfig(AppConfig):
    name = 'django_health_check_version'

    def ready(self):
        from .backends import VersionBackend
        plugin_dir.register(VersionBackend)
