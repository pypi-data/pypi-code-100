from typing import List

from drone_api_client.service import get_date_from_timestamp


class Build:
    def __init__(self, data: dict):
        if data is not None:
            self.id: int = data.get('id')
            self.repo_id: int = data.get('repo_id')
            self.trigger: str = data.get('trigger')
            self.number: int = data.get('number')
            self.status: str = data.get('status')
            self.event: str = data.get('event')
            self.action: str = data.get('action')
            self.link: str = data.get('link')
            self.timestamp: int = get_date_from_timestamp(data.get('timestamp'))
            self.message: str = data.get('message')
            self.before: str = data.get('before')
            self.after: str = data.get('after')
            self.ref: str = data.get('ref')
            self.source_repo: str = data.get('source_repo')
            self.source: str = data.get('source')
            self.target: str = data.get('target')
            self.author_login: str = data.get('author_login')
            self.author_name: str = data.get('author_name')
            self.author_email: str = data.get('author_email')
            self.author_avatar: str = data.get('author_avatar')
            self.sender: str = data.get('sender')
            self.cron: str = data.get('cron')
            self.started: int = get_date_from_timestamp(data.get('started'))
            self.finished: int = get_date_from_timestamp(data.get('finished'))
            self.created: int = get_date_from_timestamp(data.get('created'))
            self.updated: int = get_date_from_timestamp(data.get('updated'))
            self.version: int = data.get('version')
            if data.get('stages') is not None:
                self.stages = tuple(Stages(stage) for stage in data.get('stages'))

    def __str__(self):
        return f'{self.message}, {self.status}'


class Stages:
    def __init__(self, data: dict):
        if data is not None:
            self.id: int = data.get('id')
            self.repo_id: int = data.get('repo_id')
            self.build_id: int = data.get('build_id')
            self.number: int = data.get('number')
            self.name: str = data.get('name')
            self.kind: str = data.get('kind')
            self.type: str = data.get('type')
            self.status: str = data.get('status')
            self.errignore: bool = data.get('errignore')
            self.exit_code: int = data.get('exit_code')
            self.machine: str = data.get('machine')
            self.os: str = data.get('os')
            self.arch: str = data.get('arch')
            self.started: int = get_date_from_timestamp(data.get('started'))
            self.stopped: int = get_date_from_timestamp(data.get('stopped'))
            self.created: int = get_date_from_timestamp(data.get('created'))
            self.updated: int = get_date_from_timestamp(data.get('updated'))
            self.version: int = data.get('version')
            self.on_success: bool = data.get('on_success')
            self.on_failure: bool = data.get('on_failure')
            if data.get('steps') is not None:
                self.steps: List[Steps] = tuple(Steps(step) for step in data.get('steps'))

    def __str__(self):
        return self.name


class Steps:
    def __init__(self, data: dict):
        if data is not None:
            self.id: int = data.get('id')
            self.step_id: int = data.get('step_id')
            self.number: int = data.get('number')
            self.name: str = data.get('name')
            self.status: str = data.get('status')
            self.exit_code: int = data.get('exit_code')
            self.started: int = get_date_from_timestamp(data.get('started'))
            self.stopped: int = get_date_from_timestamp(data.get('stopped'))
            self.version: int = data.get('version')

    def __str__(self):
        return self.name
