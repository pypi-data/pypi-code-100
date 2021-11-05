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

"""Custom cluster upgrade specific commands"""
import click

from osducli.click_cli import CustomClickCommand, State, command_with_output
from osducli.cliclient import CliOsduClient, handle_cli_exceptions
from osducli.config import CONFIG_SEARCH_URL


@click.command(cls=CustomClickCommand)
@handle_cli_exceptions
@command_with_output("sort_by(aggregations,&key)[*].{Key:key,Count:count}")
def _click_command(state: State):
    """List count of populated records"""

    return records(state)


def records(state: State):
    """[summary]

    Args:
        state (State): Global state
    """
    request_data = {"kind": "*:*:*:*", "limit": 1, "query": "*", "aggregateBy": "kind"}

    connection = CliOsduClient(state.config)
    json_response = connection.cli_post_returning_json(CONFIG_SEARCH_URL, "query", request_data)

    return json_response
