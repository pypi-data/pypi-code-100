import click

from .login.commands import login_cli
from .saml.commands import saml_cli


def create_settings_cli_group():
    commands = {
        "login": login_cli,
        "saml": saml_cli,
    }

    @click.group(commands=commands)
    def group():
        """Customize your dagster-cloud settings."""

    return group


settings_cli = create_settings_cli_group()
