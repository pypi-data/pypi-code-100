from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click


@click.group()
@click.pass_context
def techniques(_):
    """
    Query or count techniques.
    """
    pass


@techniques.command()
@click.option('--technique-id')
@click.option('--technique-name')
@click.pass_context
def get_technique(_: click.Context, technique_id: str, technique_name: str):
    if not (technique_id or technique_name):
        raise ValueError("An ID or name is required")

    api = MitreAttack()
    technique = api.enterprise.get_technique(technique_id=technique_id, technique_name=technique_name)
    if technique:
        click.echo(technique.to_json())


@techniques.command()
@click.option('--technique-ids')
@click.option('--technique-names')
@click.pass_context
def get_techniques(_: click.Context, technique_ids: str, technique_names: str):
    api = MitreAttack()
    for technique in api.enterprise.iter_techniques(
        technique_ids=click.str_to_strs(technique_ids),
        technique_names=click.str_to_strs(technique_names),
    ):
        click.echo(technique.to_json())


@techniques.command()
@click.option('--technique-ids')
@click.option('--technique-names')
@click.pass_context
def count_techniques(_: click.Context, technique_ids: str, technique_names: str):
    api = MitreAttack()
    n = api.enterprise.count_techniques(
        technique_ids=click.str_to_strs(technique_ids),
        technique_names=click.str_to_strs(technique_names),
    )
    click.echo(n)
