#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Version command"""

import sys

import click

import osducli
from osducli.click_cli import CustomClickCommand, global_params
from osducli.cliclient import handle_cli_exceptions


# click entry point
@click.command(cls=CustomClickCommand)
@handle_cli_exceptions
@global_params
def _click_command(_):
    """Version information"""
    version()


def get_runtime_version() -> str:
    """Get the runtime information.

    Returns:
        str: Runtime information
    """
    import platform

    version_info = "\n\n"
    version_info += "Python ({}) {}".format(platform.system(), sys.version)
    version_info += "\n\n"
    version_info += "Python location '{}'".format(sys.executable)
    return version_info


def version():
    """Print version information to standard system out."""
    version_info = f"OSDU Cli Version {osducli.__VERSION__}"
    version_info += get_runtime_version()
    print(version_info)
