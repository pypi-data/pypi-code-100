import os
from logging import Logger
from penvy.setup.SetupStepInterface import SetupStepInterface


class AppEnvSetter(SetupStepInterface):
    def __init__(
        self,
        logger: Logger,
    ):
        self._logger = logger

    def run(self):
        self._logger.info("Setting APP_ENV environment variable to 'dev'")
        os.environ["APP_ENV"] = "dev"

    def get_description(self):
        return "Set APP_ENV environment variable"

    def should_be_run(self) -> bool:
        return "APP_ENV" not in os.environ
