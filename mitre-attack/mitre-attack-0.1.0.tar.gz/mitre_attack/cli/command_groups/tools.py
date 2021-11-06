from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click


@click.group()
@click.pass_context
def tools(_):
    """
    Query or count tools.
    """
    pass


@tools.command()
@click.option('--software-id')
@click.option('--software-name')
@click.pass_context
def get_tool(_: click.Context, software_id: str, software_name: str):
    if not (software_id or software_name):
        raise ValueError("An ID or name is required")

    api = MitreAttack()
    tool = api.enterprise.get_tool(software_id=software_id, software_name=software_name)
    if tool:
        click.echo(tool.to_json())


@tools.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def get_tools(_: click.Context, software_ids: str, software_names: str):
    api = MitreAttack()
    for row in api.enterprise.iter_tools(
        software_ids=click.str_to_strs(software_ids),
        software_names=click.str_to_strs(software_names),
    ):
        click.echo(row.to_json())


@tools.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def count_tools(_: click.Context, software_ids: str, software_names: str):
    api = MitreAttack()
    n = api.enterprise.count_tools(
        software_ids=click.str_to_strs(software_ids),
        software_names=click.str_to_strs(software_names),
    )
    click.echo(n)
