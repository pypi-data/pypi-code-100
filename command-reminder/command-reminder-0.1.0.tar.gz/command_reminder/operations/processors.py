import os
import typing
import subprocess

from command_reminder.common import InvalidArgumentException
from command_reminder.operations.dto import OperationData, InitOperationDataDto


class Processor:
    def process(self, operation: OperationData) -> None:
        pass


class InitRepositoryProcessor(Processor):
    def process(self, data: OperationData) -> None:
        if not isinstance(data, InitOperationDataDto):
            return
        self._validate(data)
        self._create_dir(data.directory)
        self._init_git_repo(data.directory, data.repo)

    @staticmethod
    def _validate(data: InitOperationDataDto) -> None:
        if not data.directory:
            raise InvalidArgumentException("Config directory must be configured.")

    @staticmethod
    def _create_dir(path) -> None:
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def _init_git_repo(directory, repo):
        if repo:
            subprocess.run([f'cd {directory} && git init && git remote add origin {repo}'],
                           shell=True, check=True)


class CompoundProcessor:
    def __init__(self, processors: typing.List[Processor]):
        self.processors = processors

    def process(self, operation: OperationData) -> None:
        for p in self.processors:
            p.process(operation)
