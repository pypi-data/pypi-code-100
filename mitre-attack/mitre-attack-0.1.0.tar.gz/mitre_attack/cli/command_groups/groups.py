from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click


@click.group()
@click.pass_context
def groups(_):
    """
    Query or count groups.
    """
    pass


@groups.command()
@click.option('--group-id')
@click.option('--group-name')
@click.pass_context
def get_group(_: click.Context, group_id: str, group_name: str):
    if not (group_id or group_name):
        raise ValueError("An ID or name is required")

    api = MitreAttack()
    group = api.enterprise.get_group(group_id=group_id, group_name=group_name)
    if group:
        click.echo(group.to_json())


@groups.command()
@click.option('--group-ids')
@click.option('--group-names')
@click.pass_context
def get_groups(_: click.Context, group_ids: str, group_names: str):
    api = MitreAttack()
    for group in api.enterprise.iter_groups(
        group_ids=click.str_to_strs(group_ids),
        group_names=click.str_to_strs(group_names),
    ):
        click.echo(group.to_json())


@groups.command()
@click.option('--group-ids')
@click.option('--group-names')
@click.pass_context
def count_groups(_: click.Context, group_ids: str, group_names: str):
    api = MitreAttack()
    n = api.enterprise.count_groups(
        group_ids=click.str_to_strs(group_ids),
        group_names=click.str_to_strs(group_names),
    )
    click.echo(n)
