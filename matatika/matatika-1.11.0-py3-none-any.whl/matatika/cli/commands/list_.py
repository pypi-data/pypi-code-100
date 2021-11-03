"""CLI 'list' command and subcommands"""

import click
from matatika.cli.utility import Resolver
from matatika.cli.display import Column, Table
from matatika.types import Resource
from .root import matatika


@matatika.group('list', short_help='List all available resources')
@click.pass_context
@click.option("-m", "--minimal", is_flag=True, help="Output the resource data only")
def list_(ctx, minimal):
    """Display a list of all available resources of a specified type"""

    ctx.obj['minimal'] = minimal


@list_.command('workspaces', short_help='List all available workspaces')
@click.pass_context
def list_workspaces(ctx):
    """Display a list of all available workspaces"""

    minimal = ctx.obj['minimal']

    client = Resolver(ctx).client(workspace_id=None)
    workspaces = client.list_resources(Resource.WORKSPACE)

    ids = Column("WORKSPACE ID")
    names = Column("NAME")

    if minimal:
        for column in (ids, names):
            column.heading = None

    for workspace in workspaces:
        ids.add(workspace['id'])
        names.add(workspace['name'])

    table = Table(ids, names)
    click.echo(table)

    if not minimal:
        click.echo(f"\nTotal workspaces: {len(workspaces)}")


@list_.command('datasets', short_help='List all available datasets')
@click.pass_context
@click.option('--workspace-id', '-w', type=click.UUID, help='Workspace ID')
def list_datasets(ctx, workspace_id):
    """Display a list of all available datasets"""

    minimal = ctx.obj['minimal']

    ctx.obj['workspace_id'] = workspace_id
    client = Resolver(ctx).client()
    datasets = client.list_resources(Resource.DATASET)

    ids = Column("DATASET ID")
    aliases = Column("ALIAS")
    titles = Column("TITLE")

    if minimal:
        for column in (ids, aliases, titles):
            column.heading = None

    for dataset in datasets:
        ids.add(dataset['id'])
        aliases.add(dataset['alias'])
        titles.add(dataset['title'])

    table = Table(ids, aliases, titles)
    click.echo(table)

    if not minimal:
        click.echo(f"\nTotal datasets: {len(datasets)}")
