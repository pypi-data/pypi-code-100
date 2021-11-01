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

from collections import UserDict

__all__ = ["registry"]


class ConfigRegistry(UserDict):
    def __init__(self):
        super().__init__()

    def __setitem__(self, name, config_yaml):
        """Add the given named configuration to the registry dictionary.

        Notes
        -----
        If the name already appears in the registry, a ValueError is raised.

        Parameters
        ----------
        name : `str`
            The name of the configuration.
            This is the 'key' in the key-value pair.
        config_yaml : `str`
            A YAML formatted string representation of the script configuration.
            This is the 'value' in the key-value pair.

        """
        if name in self.data:
            raise ValueError(f"{name} already present")
        self.data[name] = config_yaml


# Define the registry in the class module, to prevent multiple
# registries exisiting in memory at the same time.
registry = ConfigRegistry()
