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

import subprocess


def assert_yaml_formatted(yaml_string):
    """Assert that the given string is properly yaml formatted.

    To call this from a unit test (see ``tests/test_yaml.py``)::

        IntegrationTests.assert_yaml_formatted(yaml_string)

    Parameters
    ----------
    yaml_string : `str`
        String, either stdin or printed content from a file.

    Raises
    ------
    AssertionError
        If string not formatted properly as assessed by ``yamllint``.

    Notes
    -----
    Yamllint works with files or stdin, but the invocation syntax is
    different. Most instances in the integration testing will be
    strings, so this test uses the stdin invocation.
    """
    args = ["yamllint", "-"]
    byte_string = bytes(yaml_string, "utf-8")
    child_proccess = subprocess.Popen(
        args, stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    child_proccess.stdin.write(byte_string)
    result = child_proccess.communicate()[0]
    result = result.decode("utf-8")
    child_proccess.stdin.close()
    if any(exception in result for exception in ("warning", "error")):
        raise AssertionError(result)


def logging_statement(statement):
    """Print a logging statement

    Parameters
    ----------
    statement : `string`
        statement; The string to print
    """
    print(statement)
