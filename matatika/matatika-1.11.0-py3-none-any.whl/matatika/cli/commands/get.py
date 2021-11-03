"""CLI 'get' command and subcommands"""

import click
from matatika.cli.utility import Resolver
from matatika.utility import is_uuid4
from .root import matatika


@matatika.group('get', short_help='Get a specific resource')
def get():
    """Display a specific resource"""


@get.command('dataset', short_help='Get a dataset')
@click.pass_context
@click.argument("dataset-id-or-alias")
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
def get_dataset(ctx, dataset_id_or_alias, workspace_id):
    """Display a dataset resource"""

    ctx.obj['workspace_id'] = workspace_id
    excludes = {'workspace_id': None} if is_uuid4(dataset_id_or_alias) else {}

    client = Resolver(ctx).client(**excludes)
    dataset = client.get_dataset(dataset_id_or_alias, raw=True)

    click.echo(dataset)
