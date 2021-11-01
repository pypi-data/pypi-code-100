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

import unittest
import subprocess

from inspect import getmembers, isfunction
from lsst.ts import IntegrationTests


class YamlTestCase(unittest.TestCase):
    """Test that the configurations are stored as properly formatted
    Yaml strings.

    """

    def test_yaml_formatted(self):
        """Use the IntegrationTests.yaml_test_string1() configuration to test
        a well-formatted Yaml string.

        """
        yaml_string = IntegrationTests.yaml_test_string1()
        IntegrationTests.assert_yaml_formatted(yaml_string)

    def test_bad_yaml(self):
        """Use the IntegrationTests.bad_yaml() configuration to test
        a non-Yaml-formatted string.

        """
        bad_yaml = IntegrationTests.bad_yaml()
        args = ["yamllint", "-"]
        byte_string = bytes(bad_yaml, "utf-8")
        child_proccess = subprocess.Popen(
            args, stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
        child_proccess.stdin.write(byte_string)
        result = child_proccess.communicate()[0]
        result = result.decode("utf-8")
        child_proccess.stdin.close()
        if any(exception in result for exception in ("warning", "error")):
            assert True
        else:
            assert False

    def test_auxtel_visit_config(self):
        """Test the IntegrationTests.auxtel_visit_config() is
        well-formatted Yaml.

        """
        length = len(getmembers(IntegrationTests.take_image_latiss_configs, isfunction))
        for i in range(length):
            config = getattr(
                IntegrationTests, getmembers(IntegrationTests.configs, isfunction)[i][0]
            )
            yaml_string = config()
            IntegrationTests.assert_yaml_formatted(yaml_string)
