"""CLI 'profile' command"""

import click
from matatika.cli.display import Column, Table
from matatika.cli.utility import Resolver
from .root import matatika


@matatika.command('profile', short_help='Return the authenticated user profile')
@click.pass_context
def profile(ctx):
    """Returns the authenticated user profile"""

    client = Resolver(ctx).client(workspace_id=None)
    profile_ = client.profile()

    labels = Column()
    values = Column()

    labels.add("ID", "NAME")
    values.add(profile_['id'], profile_['name'])

    table = Table(labels, values)
    click.echo(table.create(separator="\t-->\t"))
