# pylint: disable=too-many-locals, too-many-branches

"""CLI 'publish' command"""

# standard
from pathlib import Path
# external
import click
# local
from matatika.cli.display import Column, Table
from matatika.cli.utility import Resolver
from matatika.types import Resource
from matatika.cli.parse_service import parse_yaml, parse_notebook
from .root import matatika


NOTEBOOK = ['.ipynb']
YAML = ['.yml', '.yaml']
SUPPORTED_FILETYPES = NOTEBOOK + YAML


@matatika.command('publish', short_help='Publish one or more files(s)')
@click.pass_context
@click.argument('user-file', type=click.Path(exists=True))
@click.option("--workspace-id", "-w", type=click.UUID, help="Workspace ID")
@click.option("--dataset-alias", '-alias', type=click.STRING, help="Dataset Alias")
def publish(ctx, user_file, workspace_id, dataset_alias):
    """Publish one or more dataset(s) or a channels from a YAML file into a workspace"""

    ctx.obj['workspace_id'] = workspace_id
    client = Resolver(ctx).client()

    file_ext = Path(user_file).suffix

    if file_ext not in SUPPORTED_FILETYPES:
        click.secho("Filetype not supported", fg='red')
        return

    if file_ext in YAML:
        yaml_files, yaml_type = parse_yaml(user_file, dataset_alias, file_ext)
        if yaml_files is None and yaml_type == Resource.DATASET:
            click.secho("Cannot specify alias option with more than one dataset", fg='red')
            return
    elif file_ext in NOTEBOOK:
        yaml_type = Resource.DATASET
        yaml_files = parse_notebook(user_file, dataset_alias, file_ext)

    if yaml_type == Resource.DATASET:
        published_files = client.publish(yaml_type, yaml_files)

        click.secho(f"Successfully published {len(published_files)} dataset(s)\n",
                    fg='green')

        ids = Column("DATASET ID")
        aliases = Column("ALIAS")
        titles = Column("TITLE")
        statuses = Column("STATUS")

        for dataset, status_code in published_files:
            if status_code == 201:
                status = click.style("NEW", fg='magenta')
            else:
                status = click.style("UPDATED", fg='cyan')

            if not dataset.alias:
                dataset.alias = click.style(str(dataset.alias), fg='yellow')

            ids.add(dataset.dataset_id)
            aliases.add(dataset.alias)
            titles.add(dataset.title)
            statuses.add(status)

        table = Table(ids, aliases, titles, statuses)
        click.echo(table)

    if yaml_type == Resource.CHANNEL:
        published_files = client.publish(yaml_type,yaml_files)

        click.secho(f"Successfully published {len(published_files)} channels(s)\n",
                    fg='green')

        ids = Column("CHANNEL ID")
        name = Column("NAME")
        description = Column("DESCRIPTION")
        statuses = Column("STATUS")

        for channel, status_code in published_files:
            if status_code == 201:
                status = click.style("NEW", fg='magenta')
            else:
                status = click.style("UPDATED", fg='cyan')

            ids.add(channel.channel_id)
            name.add(channel.name)
            description.add(channel.description)
            statuses.add(status)

        table = Table(ids, name, description, statuses)
        click.echo(table)
