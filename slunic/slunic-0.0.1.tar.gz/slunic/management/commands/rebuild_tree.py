from django.core.management.base import BaseCommand
from ...models import Page


class Command(BaseCommand):
    help = "Rebuild mptt tree structure"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Page.objects.rebuild()
