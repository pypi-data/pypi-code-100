from django.apps import AppConfig


class SlunicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "slunic"

    def ready(self):
        from slunic import signals  # NOQA
        from slunic.permissions import init_groups # NOQA
        # init_groups()
        return super().ready()
