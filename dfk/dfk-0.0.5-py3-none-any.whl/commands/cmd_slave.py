import ipaddress

import click
from defektor_api import ApiException, Slave

import dfk.config
from dfk.cli import DfkCli


@click.group("slave")
def cli():
    """👷 Slave machine management."""


@dfk.config.require_login
@cli.command()
@click.argument("address", required=True)
@click.argument("user", required=True)
@click.argument("private_key_path", required=True, type=click.Path(exists=True))
@click.argument("port", required=False)
def add(address, user, private_key_path, port):
    """Add a slave machine to run the work-loads."""

    try:
        address = ipaddress.ip_address(address)

        with open(private_key_path, 'r') as private_key_file:
            private_key_data = private_key_file.read().replace('\n', '')

        # TODO: Add user and remove id!
        slave = Slave(id=0, address=str(address), credentials=private_key_data)

        if port is not None:
            slave.port = port

        add_slave_result = DfkCli.api_instance.slave_add(slave)
        click.echo(add_slave_result)
    except ApiException as api_exception:
        click.echo(
            f"ERROR: adding te slave with address {address}, user {user}, and private_key_path {private_key_path}.\n{api_exception}")
    except IOError as file_read_exception:
        click.echo(f"ERROR: reading private key from path {private_key_path}.\n{file_read_exception}")
    except ValueError as address_format_exception:
        click.echo(f"ERROR: reading address.\n{address_format_exception}")


@dfk.config.require_login
@cli.command()
def list():
    """Lists slaves."""

    try:
        list_slaves_result = DfkCli.api_instance.slave_list()
        click.echo(list_slaves_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: listing slaves.\n{api_exception}")


@dfk.config.require_login
@cli.command()
@click.argument("id", required=True)
def remove(id):
    """Removes a slave machine."""

    try:
        remove_slave_result = DfkCli.api_instance.slave_delete(slave_id=id)
        click.echo(remove_slave_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: removing slave with id {id}.\n{api_exception}")
