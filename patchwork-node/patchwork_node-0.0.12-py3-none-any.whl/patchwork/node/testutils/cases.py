# -*- coding: utf-8 -*-

from contextlib import asynccontextmanager

from typing import Type, Mapping

from patchwork.core.testutils.cases import AsyncioTestCase
from patchwork.node.core import Module
from patchwork.node.testutils.mocks import WorkerMock


class ModuleTestCase(AsyncioTestCase):

    module_class: Type[Module]
    worker: WorkerMock

    def get_module_settings(self) -> Mapping:
        return {}

    def setUp(self) -> None:
        super().setUp()
        self._worker = WorkerMock()

        self.module = self.module_class(self._worker, **self.get_module_settings())

    def tearDown(self) -> None:
        del self.module
        del self._worker

    async def _test_module_run(self):

        self.assertTrue(await self.module.run(), msg="Module run() method should return True "
                                                     "when successfully started")

        self.assertTrue(self.module.is_running, msg="Module should have is_running property set to True after run(). "
                                                    "Is run()/start() methods return when module is really started?")

        self.assertTrue(await self.module.terminate(), msg="Module terminate() should return True "
                                                           "when successfully stopped")
        self.assertFalse(self.module.is_running, msg="Module should have is_running property set to False after"
                                                     "terminate(). Is terminate()/stop() methods return when module"
                                                     "is really stopped?")

    def test_00_module_lifetime(self):
        # name is prefixed with '00' to run it as the first one (in most cases) so you can run test with failfast
        # and if module startup and shutdown is not passing then running all other tests make no sense and won't
        # be executed
        self.loop.run_until_complete(self._test_module_run())

    @asynccontextmanager
    async def running_module(self):
        if not await self.module.run():
            raise RuntimeError("Module didn't start, can't run test")

        try:
            yield self.module
        finally:
            await self.module.terminate()
