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

__all__ = ["BaseScript"]

from lsst.ts import salobj
from lsst.ts.idl.enums import ScriptQueue


class BaseScript:
    """Defines the common attributes and functions for an
       AuxTel or MainTel script.

    Notes
    -----
    Use index=1 for MainTel, 2 for AuxTel. The index is defined as a class
    attribute for simplicity.  The sub-Classes define which index,
    if necessary.
    The BaseScript class defaults to index=1, as the most common option.

    Attributes
    ----------
    index : `int`
        The index represents the Main Telescope, index=1, or the
        Auxilliary Telescope, index=2.
    configs : `tuple`
        The list of Yaml-formatted script configurations.
        They are stored in the configs.py module.
    scripts : `tuple`
        The list of Standard or External scripts to execute.
    """

    # See Attributes for the definition.
    index = 1
    configs = None
    scripts = None

    def __init__(self, isStandard=True, queue_placement="LAST"):
        """Initialize the given Standard or External
           script, with the given Yaml configuration, placed in the
           given ScriptQueue location.

        Parameters
        ----------
        isStandard : `bool`
            If True, the script is in ts_standardscripts (True is the
            default, as it is the most common option).
            if False, the script is in ts_externalscripts.
        queue_placement : `str`
            Options are "FIRST" "LAST" "BEFORE" or "AFTER" and are
            case insensistive ("FIRST" is the default, for convenience).
            The BaseScript Class will convert to the appropriate
            ScriptQueue.Location enum object.

        """
        self.isStandard = isStandard
        self.queue_placement = queue_placement

    async def run(self):
        """Run the specified standard or external script."""
        async with salobj.Domain() as domain, salobj.Remote(
            domain=domain, name="ScriptQueue", index=self.index
        ) as remote:
            # Since `async with` is used,
            # you do NOT have to wait for the remote to start

            # Convert the queue_placement parameter to the approprirate
            # ScriptQueue.Location Enum object.
            queue_placement = getattr(
                ScriptQueue.Location, self.queue_placement.upper()
            )

            # Wait for the next ScriptQueue heartbeat to ensure it is running.
            await remote.evt_heartbeat.next(flush=True, timeout=30)
            # Pause the ScriptQueue to load the scripts into the queue.
            await remote.cmd_pause.start(timeout=10)
            # Add scripts to the queue.
            for script, config in zip(self.scripts, self.configs):
                await remote.cmd_add.set_start(
                    timeout=10,
                    isStandard=self.isStandard,
                    path=script,
                    config=config,
                    logLevel=10,
                    location=queue_placement,
                )
            # Resume the ScriptQueue to begin script execution.
            await remote.cmd_resume.set_start(timeout=10)
