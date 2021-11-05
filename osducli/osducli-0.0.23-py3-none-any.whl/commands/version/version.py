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
from requests.exceptions import RequestException

import osducli
from osducli.click_cli import CustomClickCommand, State, command_with_output
from osducli.cliclient import CliOsduClient, handle_cli_exceptions
from osducli.config import (
    CONFIG_ENTITLEMENTS_URL,
    CONFIG_LEGAL_URL,
    CONFIG_SCHEMA_URL,
    CONFIG_SEARCH_URL,
    CONFIG_STORAGE_URL,
)
from osducli.log import get_logger

logger = get_logger(__name__)


# click entry point
@click.command(cls=CustomClickCommand)
@handle_cli_exceptions
@command_with_output("results[]")
def _click_command(state: State):
    """Version information"""
    return version(state)


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


def get_api_info(connection: CliOsduClient, config_url_key: str, url_extra_path: str):
    """Check the status of the given service"""
    try:
        response = connection.cli_get_returning_json(config_url_key, url_extra_path)
        return response
    except RequestException:  # pylint: disable=broad-except
        return None


def version(state: State):
    """Print version information to standard system out."""
    if state.is_user_friendly_mode():
        version_info = f"OSDU Cli Version {osducli.__VERSION__}"
        version_info += get_runtime_version()
        print(version_info)

    services = [
        ("File service", CONFIG_ENTITLEMENTS_URL, "info"),
        ("Legal service", CONFIG_LEGAL_URL, "info"),
        ("Schema service", CONFIG_SCHEMA_URL, "info"),
        ("Search service", CONFIG_SEARCH_URL, "info"),
        ("Storage service", CONFIG_STORAGE_URL, "info"),
    ]
    results = []
    connection = CliOsduClient(state.config)
    for service in services:
        result = get_api_info(connection, service[1], service[2])
        results.append(result)
        if state.is_user_friendly_mode():
            print()
            print(service[0])
            print("  Version:", result["version"])
            print("  Build Time:", result["buildTime"])
            print("  Branch:", result["branch"])
            print("  Commit Id:", result["commitId"])

    return None if state.is_user_friendly_mode() else {"results": results}
