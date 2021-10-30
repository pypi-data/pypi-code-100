from aleksis.core.celery import app

from .commands import ImportCommand

TASKS = {}
for import_command in ImportCommand.__subclasses__():

    @app.task(name=import_command.task_name)
    def _task():
        import_command.run()

    TASKS[import_command] = _task
