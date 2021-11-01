# This file is part of ts_IntegrationTests
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

import asyncio
from lsst.ts import salobj

# Create an inherited class from the controller,
# so that you can add logic when commands are received.
# You can also output events and telemetry from there.


class ScriptQueueController(salobj.Controller):
    """Define a ScriptQueue controller. This is used by the unit tests to
    mimic the functions of the real ScriptQueue. The integration test
    scripts are designed to run in a fully stood-up environment.

    """

    def __init__(self, index):
        """Initialize the ScriptQueue Controller.

        Parameters
        ----------
        index : `int`
            Defines whether this is a MainTel (index=1)
        or an AuxTel (index=2) controller.
        """
        super().__init__("ScriptQueue", index=index)
        self.index = index
        self.queue_list = []
        self.cmd_pause.callback = self.do_pause
        self.cmd_add.callback = self.do_add
        self.cmd_resume.callback = self.do_resume

    async def pub_hb(self):
        """Publish the heartbeat. This ensures the controller is running.
        The test scripts check for the heartbeat before proceeding.

        """
        try:
            while True:
                self.evt_heartbeat.put()
                await asyncio.sleep(1.0)
        except asyncio.CancelledError:
            self.log.debug("Heartbeat ended normally")
        except Exception:
            self.log.exception("Heartbeat failed!")

    async def start(self):
        """Start the Controller and the hertbeat."""
        await super().start()
        self.hb_task = asyncio.create_task(self.pub_hb())

    async def do_pause(self, data):
        """Pause the ScriptQueue to add scripts to the queue."""
        # self.log.info("ScriptQueue paused\n")
        pass

    async def do_add(self, data):
        """Add scripts to the ScriptQueue queue.
        This mock function uses a simple array to mimic the queue.
        It simply appends the script path to the array.

        Parameters
        ----------
        data : ``cmd_add.DataType``
            Data is an object that contains the configuration for the script.
            This includes the path to the script and the Location in
            queue.

        """
        # self.log.info("Script: " + data.path)
        # self.log.info("Location: " + data.location)
        self.queue_list.append(data.path)

    async def do_resume(self, data):
        """Resume the ScriptQueue after adding the scripts
        to the queue. The ScriptQueue will then execute
        the scripts.

        """
        # self.log.info("ScriptQueue resumed\n")
        pass

    async def close_tasks(self):
        """This closes the resources for the controller,
        and terminates the heartbeat loop.

        """
        self.hb_task.cancel()
        await super().close_tasks()

    async def do_move(self):
        pass

    async def do_requeue(self):
        pass

    async def do_showAvailableScripts(self):
        pass

    async def do_showQueue(self):
        """Show the queue via the output from the queue event."""
        pass

    async def do_showSchema(self):
        pass

    async def do_showScript(self):
        pass

    async def do_stopScripts(self):
        pass

    @classmethod
    async def amain(cls) -> None:
        csc = cls()
        await csc.done_task
