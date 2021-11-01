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

"""Code to handle status commands"""

import click
from requests.exceptions import RequestException

from osducli.click_cli import CustomClickCommand, State, command_with_output
from osducli.cliclient import CliOsduClient, handle_cli_exceptions
from osducli.config import (
    CONFIG_FILE_URL,
    CONFIG_LEGAL_URL,
    CONFIG_SCHEMA_URL,
    CONFIG_SEARCH_URL,
    CONFIG_STORAGE_URL,
    CONFIG_UNIT_URL,
    CONFIG_WORKFLOW_URL,
)
from osducli.log import get_logger

logger = get_logger(__name__)


@click.command(cls=CustomClickCommand)
@handle_cli_exceptions
@command_with_output("results[]")
def _click_command(state: State):
    # def _click_command(ctx, debug, config, hostname):
    """Shows the status of OSDU services"""
    return status(state)


def status(state: State):  # pylint: disable=unused-argument
    """status command entry point

    User friendly mode displays results as received for responsiveness.
    Args:
        state (State): Global state
    """
    connection = CliOsduClient(state.config)
    results = []
    services = [
        ("File service", CONFIG_FILE_URL, "readiness_check"),
        ("Legal service", CONFIG_LEGAL_URL, "_ah/readiness_check"),
        ("Schema service", CONFIG_SCHEMA_URL, "schema?limit=1"),
        ("Search service", CONFIG_SEARCH_URL, "health/readiness_check"),
        ("Storage service", CONFIG_STORAGE_URL, "health"),
        ("Unit service", CONFIG_UNIT_URL, "../_ah/readiness_check"),
        ("Workflow service", CONFIG_WORKFLOW_URL, "../readiness_check"),
    ]
    for service in services:
        result = _check_status(connection, service[0], service[1], service[2])
        results.append(result)
        if state.is_user_friendly_mode():
            print(f"{result['name'].ljust(20)} {result['status']}\t {result['reason']}")

    return None if state.is_user_friendly_mode() else {"results": results}


def _check_status(connection: CliOsduClient, name: str, config_url_key: str, url_extra_path: str):
    """Check the status of the given service"""
    try:
        response = connection.cli_get(config_url_key, url_extra_path)
        _status = response.status_code
        _reason = response.reason
    except RequestException as _ex:  # pylint: disable=broad-except
        exception_message = str(_ex) if len(str(_ex)) > 0 else "Unknown Error"
        logger.debug(exception_message)
        _status = _ex.response.status_code if _ex.response else -1
        _reason = _ex.response.reason if _ex.response else exception_message

    result = {"name": name, "status": _status, "reason": _reason}
    return result
