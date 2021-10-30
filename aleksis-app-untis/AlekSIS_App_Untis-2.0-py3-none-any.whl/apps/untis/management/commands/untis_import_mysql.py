from django.core.management.base import BaseCommand

from ...commands import COMMANDS_BY_NAME


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "command", nargs="?", default="all", type=str, choices=list(COMMANDS_BY_NAME.keys())
        )
        parser.add_argument(
            "--background", action="store_true", help="Run import job in background using Celery",
        )

    def handle(self, *args, **options):
        command = COMMANDS_BY_NAME[options["command"]]
        background = options["background"]
        command.run(background=background)
