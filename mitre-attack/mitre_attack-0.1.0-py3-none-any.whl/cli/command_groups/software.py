from mitre_attack.api.client import MitreAttack

import mitre_attack.cli.click as click
import mitre_attack.cli.command_groups.malware as malware_command_group
import mitre_attack.cli.command_groups.tools as tools_command_group


@click.group()
@click.pass_context
def software(_):
    """
    Query or count malware and tools.
    """
    pass


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def get_software(_: click.Context, software_ids: str, software_names: str):
    api = MitreAttack()
    for row in api.enterprise.iter_software(
        software_ids=click.str_to_strs(software_ids),
        software_names=click.str_to_strs(software_names),
    ):
        click.echo(row.to_json())


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def count_software(_: click.Context, software_ids: str, software_names: str):
    api = MitreAttack()
    n = api.enterprise.count_software(
        software_ids=click.str_to_strs(software_ids),
        software_names=click.str_to_strs(software_names),
    )
    click.echo(n)


@software.command()
@click.option('--software-id')
@click.option('--software-name')
@click.pass_context
def get_malware_family(ctx: click.Context, software_id: str, software_name: str):
    ctx.invoke(malware_command_group.get_malware_family, software_id=software_id, software_name=software_name)


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def get_malware_families(ctx: click.Context, software_ids: str, software_names: str):
    ctx.invoke(malware_command_group.get_malware_families, software_ids=software_ids, software_names=software_names)


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def count_malware_families(ctx: click.Context, software_ids: str, software_names: str):
    ctx.invoke(malware_command_group.count_malware_families, software_ids=software_ids, software_names=software_names)


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def get_tool(ctx: click.Context, software_ids: str, software_names: str):
    ctx.invoke(tools_command_group.get_tool, software_ids=software_ids, software_names=software_names)


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def get_tools(ctx: click.Context, software_ids: str, software_names: str):
    ctx.invoke(tools_command_group.get_tools, software_ids=software_ids, software_names=software_names)


@software.command()
@click.option('--software-ids')
@click.option('--software-names')
@click.pass_context
def count_tools(ctx: click.Context, software_ids: str, software_names: str):
    ctx.invoke(tools_command_group.count_tools, software_ids=software_ids, software_names=software_names)
