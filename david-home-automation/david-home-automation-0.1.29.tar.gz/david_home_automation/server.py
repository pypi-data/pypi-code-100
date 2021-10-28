import click

import david_home_automation.main
from david_home_automation.main import app
from david_home_automation.utils import get_config


@click.command()
@click.option('--server-port', default=5000)
@click.option('--server-host', default="0.0.0.0")
@click.option('--config-file', default='~/.config/david-home-automation.yaml')
def cli(server_port: int, server_host: str, config_file: str):
    # TODO: this is NOT clean
    david_home_automation.main.CONFIG = get_config(config_file)

    app.run(
        host=server_host,
        port=server_port
    )


if __name__ == '__main__':
    cli()
