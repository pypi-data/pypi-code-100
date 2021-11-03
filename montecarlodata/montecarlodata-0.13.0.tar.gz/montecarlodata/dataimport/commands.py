import click

from montecarlodata.dataimport.dbt import DbtImportService


@click.group(help='Import data.', name='import')
def import_subcommand():
    """
    Group for any import related subcommands
    """
    pass


@import_subcommand.command(help='Import DBT manifest.')
@click.argument('MANIFEST_FILE', required=True, type=click.Path(exists=True))
@click.pass_obj
def dbt_manifest(ctx, manifest_file):
    DbtImportService(config=ctx['config'], dbt_manifest_file=manifest_file).import_dbt_manifest()
