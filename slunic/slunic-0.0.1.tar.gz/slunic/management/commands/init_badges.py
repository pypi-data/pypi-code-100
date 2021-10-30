from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...awards import init_badges

User = get_user_model()


class Command(BaseCommand):
    help = "Init Badges"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        init_badges()
