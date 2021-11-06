from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click


@click.group()
@click.pass_context
def tactics(_):
    """
    Query or count tactics.
    """
    pass


@tactics.command()
@click.option('--tactic-id')
@click.option('--tactic-name')
@click.pass_context
def get_tactic(_: click.Context, tactic_id: str, tactic_name: str):
    if not (tactic_id or tactic_name):
        raise ValueError("An ID or name is required")

    api = MitreAttack()
    tactic = api.enterprise.get_tactic(tactic_id=tactic_id, tactic_name=tactic_name)
    if tactic:
        click.echo(tactic.to_json())


@tactics.command()
@click.option('--tactic-ids')
@click.option('--tactic-names')
@click.pass_context
def get_tactics(_: click.Context, tactic_ids: str, tactic_names: str):
    api = MitreAttack()
    for tactic in api.enterprise.iter_tactics(
        tactic_ids=click.str_to_strs(tactic_ids),
        tactic_names=click.str_to_strs(tactic_names),
    ):
        click.echo(tactic.to_json())


@tactics.command()
@click.option('--tactic-ids')
@click.option('--tactic-names')
@click.pass_context
def count_tactics(_: click.Context, tactic_ids: str, tactic_names: str):
    api = MitreAttack()
    n = api.enterprise.count_tactics(
        tactic_ids=click.str_to_strs(tactic_ids),
        tactic_names=click.str_to_strs(tactic_names),
    )
    click.echo(n)
