from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...configs import app_configs

User = get_user_model()


class Command(BaseCommand):
    help = "Init Bot User"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            bot_user = User.objects.get(username=app_configs.BOT_USERNAME)
        except User.DoesNotExist:
            bot_user = User.objects.create_user(
                username=app_configs.BOT_USERNAME,
                password=str(app_configs.BOT_PASSWORD),
                email=app_configs.BOT_EMAIL,
                first_name=app_configs.BOT_NAME,
                is_staff=True,
                is_superuser=True,
            )
        bot_user.save()
