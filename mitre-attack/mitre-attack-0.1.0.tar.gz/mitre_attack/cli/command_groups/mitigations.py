from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click


@click.group()
@click.pass_context
def mitigations(_):
    """
    Query or count mitigations.
    """
    pass


@mitigations.command()
@click.option('--mitigation-id')
@click.option('--mitigation-name')
@click.pass_context
def get_mitigation(_: click.Context, mitigation_id: str, mitigation_name: str):
    if not (mitigation_id or mitigation_name):
        raise ValueError("An ID or name is required")

    api = MitreAttack()
    mitigation = api.enterprise.get_mitigation(mitigation_id=mitigation_id, mitigation_name=mitigation_name)
    if mitigation:
        click.echo(mitigation.to_json())


@mitigations.command()
@click.option('--mitigation-ids')
@click.option('--mitigation-names')
@click.pass_context
def get_mitigations(_: click.Context, mitigation_ids: str, mitigation_names: str):
    api = MitreAttack()
    for mitigation in api.enterprise.iter_mitigations(
        mitigation_ids=click.str_to_strs(mitigation_ids),
        mitigation_names=click.str_to_strs(mitigation_names),
    ):
        click.echo(mitigation.to_json())


@mitigations.command()
@click.option('--mitigation-ids')
@click.option('--mitigation-names')
@click.pass_context
def count_mitigations(_: click.Context, mitigation_ids: str, mitigation_names: str):
    api = MitreAttack()
    n = api.enterprise.count_mitigations(
        mitigation_ids=click.str_to_strs(mitigation_ids),
        mitigation_names=click.str_to_strs(mitigation_names),
    )
    click.echo(n)
