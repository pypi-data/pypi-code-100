import click

from vessl.cli._base import VesslGroup
from vessl.cli._util import print_table, truncate_datetime
from vessl.cli.organization import organization_name_option
from vessl.cli.project import project_name_option
from vessl.model import list_models, read_model
from vessl.volume import copy_volume_file


@click.command(name="model", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@organization_name_option
@project_name_option
def list():
    models = list_models()
    print_table(
        models,
        ["ID", "Version", "Created", "Status"],
        lambda x: [x.id, x.version, truncate_datetime(x.created_dt), x.status],
    )


@cli.vessl_command()
@click.argument("version", type=click.INT, required=True)
@click.argument("path", type=click.Path(), required=True)
@organization_name_option
@project_name_option
def download(version: int, path: str):
    model = read_model(version=version)
    copy_volume_file(model.artifact_volume_id, "", None, path, True)
