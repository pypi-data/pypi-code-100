# -*- coding: utf-8 -*-

import asyncio
from typing import Mapping

from asyncmock import AsyncMock

from patchwork.core.testutils.mocks import ConfigMock


class ProcessingUnitMock:
    pass


class ExecutorMock:
    pass


class WorkerMock:

    settings: ConfigMock

    def __init__(self, settings: Mapping = None):
        if settings is None:
            settings = {
                'debug': False,
                'processors': []
            }

        self.settings = ConfigMock(settings)

    @property
    def event_loop(self):
        return asyncio.get_event_loop()
