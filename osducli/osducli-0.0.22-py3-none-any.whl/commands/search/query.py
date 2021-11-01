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

"""Search service query command"""

import click
from osdu.search import SearchClient

from osducli.click_cli import CustomClickCommand, State, command_with_output
from osducli.cliclient import CliOsduClient, handle_cli_exceptions


# click entry point
@click.command(cls=CustomClickCommand)
@click.option("-k", "--kind", "kind", help="kind to search for")
@click.option("-id", "--id", "_id", help="id to search for")
@click.option(
    "-l",
    "--limit",
    "limit",
    default=10,
    show_default=True,
    help="maximum number of records to return.",
)
@handle_cli_exceptions
@command_with_output("results[*].{Id:id,Kind:kind,CreateTime:createTime}")
def _click_command(state: State, kind: str, _id: str, limit: int):
    """Query search service"""
    return query(state, kind, _id, limit)


def query(
    state: State, kind: str, id: str, limit: int
):  # pylint: disable=invalid-name,redefined-builtin
    """Query search service

    Args:
        state (State): Global state
    """
    connection = CliOsduClient(state.config)

    search_client = SearchClient(connection)
    json_response = search_client.query(kind, id, limit)

    return json_response
