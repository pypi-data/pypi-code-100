# Copyright 2021 Rapyuta Robotics
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import click
from click_help_colors import HelpColorsCommand

from riocli.auth.util import select_project, get_token
from riocli.config import Configuration


@click.command(
    cls=HelpColorsCommand,
    help_headers_color='yellow',
    help_options_color='green',
)
@click.option('--email', prompt='Email',
              help='Email of the Rapyuta.io account')
@click.option('--password', prompt='Password', hide_input=True,
              help='Password for the Rapyuta.io account')
def login(email: str, password: str):
    """
    Log into the Rapyuta.io account using the CLI. This is required to use most of the
    functionalities of the CLI.
    """

    config = Configuration()
    config.data['email_id'] = email
    config.data['password'] = password

    config.data['auth_token'] = get_token(email, password)

    # Save if the file does not already exist
    if not config.exists:
        click.echo('Logged in successfully!')
        config.save()
    else:
        click.echo("[Warning] rio already has a config file present")
        click.confirm('Do you want to override the config', abort=True)

    select_project(config)
    config.save()
    click.echo('Logged in successfully!')
