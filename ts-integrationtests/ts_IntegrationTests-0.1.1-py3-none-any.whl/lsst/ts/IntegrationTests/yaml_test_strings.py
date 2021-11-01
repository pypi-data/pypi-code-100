# This file is part of ts_IntegrationTests.
#
# Developed for the Rubin Observatory Telescope and Site System.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import yaml


def yaml_test_string1():
    """Return a properly formatted YAML test string.

    To call this from a unit test (see ``tests/test_yaml.py``)::

        IntegrationTests.yaml_test_string1()

    """
    yaml_string = yaml.safe_load(
        """
        data:
        - - CCCamera
        - DISABLED
        - Normal
        - - CCHeaderService
        - DISABLED
        - - CCArchiver
        - DISABLED
        """
    )
    return yaml.safe_dump(yaml_string, explicit_start=True, canonical=True)


def bad_yaml():
    """Return an improperly formatted YAML string.

    To call this from a unit test (see ``tests/test_yaml.py``)::

        IntegrationTests.bad_yaml()

    """
    bad_yaml_string = "\tHello\nWorld"
    return bad_yaml_string
