import os

import click


def add_options(options):
    """
    Share options between commands
    https://stackoverflow.com/questions/40182157/shared-options-and-flags-between-commands
    """

    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


_dagit_url = lambda: os.getenv("DAGSTER_CLOUD_DAGIT_URL")


def _api_token():
    return os.getenv("DAGSTER_CLOUD_API_TOKEN")


def _show_api_token_prompt():
    password_exists = bool(_api_token())
    show_prompt = not password_exists
    return show_prompt


def _show_dagit_url_prompt():
    url_exists = bool(_dagit_url())
    return (
        "Your Dagster Cloud url, in the form of 'https://{ORGANIZATION_NAME}.dagster.cloud/{DEPLOYMENT_NAME}'"
        if not url_exists
        else True
    )


create_cloud_dagit_client_options = [
    click.option(
        "--url",
        type=click.STRING,
        default=_dagit_url,
        prompt=_show_dagit_url_prompt(),
        help=r"Your Dagster Cloud url, in the form of 'https://{ORGANIZATION_NAME}.dagster.cloud/{DEPLOYMENT_NAME}'.",
    ),
    click.option(
        "--api-token",
        type=click.STRING,
        default=_api_token,
        prompt=_show_api_token_prompt(),
        hide_input=True,
        required=True,
        help="API token generated in Dagit",
    ),
]
