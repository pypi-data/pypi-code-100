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

"""Entitlements my groups command"""

import click
from osdu.entitlements import EntitlementsClient

from osducli.click_cli import CustomClickCommand, State, global_params
from osducli.cliclient import CliOsduClient, handle_cli_exceptions


# click entry point
@click.command(cls=CustomClickCommand)
@click.option("-m", "--member", help="Email of the member to be remove.", required=True)
@click.option("-g", "--group", help="Email address of the group", required=True)
@handle_cli_exceptions
@global_params
def _click_command(state: State, member: str, group: str):
    """Remove member from a group."""
    return add_member(state, member, group)


def add_member(state: State, member: str, group: str) -> dict:
    """ "Remove member from a group.

    Args:
        state (State): Global state
        member (str): Email address of the member
        group (str): Email address of the group

    Returns:
        dict: Response from service
    """
    connection = CliOsduClient(state.config)

    entitlements_client = EntitlementsClient(connection)
    entitlements_client.remove_member_from_group(member, group)
