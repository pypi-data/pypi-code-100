from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click


@click.group()
@click.pass_context
def relationships(_):
    """
    Query or count relationships.
    """
    pass


@relationships.command()
@click.option('--relationship-ids')
@click.option('--relationship-types')
@click.option('--source-refs')
@click.option('--source-ref-types')
@click.option('--target-refs')
@click.option('--target-ref-types')
@click.pass_context
def get_relationships(
        _: click.Context,
        relationship_ids: str,
        relationship_types: str,
        source_refs: str,
        source_ref_types: str,
        target_refs: str,
        target_ref_types: str):

    api = MitreAttack()
    for relationship in api.enterprise.iter_relationships(
        relationship_ids=click.str_to_strs(relationship_ids),
        relationship_types=click.str_to_strs(relationship_types),
        source_refs=click.str_to_strs(source_refs),
        source_ref_types=click.str_to_strs(source_ref_types),
        target_refs=click.str_to_strs(target_refs),
        target_ref_types=click.str_to_strs(target_ref_types),
    ):
        click.echo(relationship.to_json())


@relationships.command()
@click.option('--relationship-ids')
@click.option('--relationship-types')
@click.option('--source-refs')
@click.option('--source-ref-types')
@click.option('--target-refs')
@click.option('--target-ref-types')
@click.pass_context
def count_relationships(
        _: click.Context,
        relationship_ids: str,
        relationship_types: str,
        source_refs: str,
        source_ref_types: str,
        target_refs: str,
        target_ref_types: str):

    api = MitreAttack()
    n = api.enterprise.count_relationships(
        relationship_ids=click.str_to_strs(relationship_ids),
        relationship_types=click.str_to_strs(relationship_types),
        source_refs=click.str_to_strs(source_refs),
        source_ref_types=click.str_to_strs(source_ref_types),
        target_refs=click.str_to_strs(target_refs),
        target_ref_types=click.str_to_strs(target_ref_types),
    )
    click.echo(n)
