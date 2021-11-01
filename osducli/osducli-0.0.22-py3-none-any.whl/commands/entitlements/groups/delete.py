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

"""Entitlements groups delete command"""

import click
from osdu.entitlements import EntitlementsClient

from osducli.click_cli import CustomClickCommand, State, global_params
from osducli.cliclient import CliOsduClient, handle_cli_exceptions


# click entry point
@click.command(cls=CustomClickCommand)
@click.option("-g", "--group", help="Email address of the group", required=True)
@handle_cli_exceptions
@global_params
def _click_command(state: State, group: str):
    """Delete a group."""
    delete_group(state, group)


def delete_group(state: State, group: str):
    """Delete a group

    Args:
        state (State): Global state
        group (str): Unique email identifier of the group
    """
    connection = CliOsduClient(state.config)

    entitlements_client = EntitlementsClient(connection)
    entitlements_client.delete_group(group)
