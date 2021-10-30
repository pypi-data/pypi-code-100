from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...permissions import init_groups

User = get_user_model()


class Command(BaseCommand):
    help = "Init Groups"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        init_groups()
