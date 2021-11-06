from mitre_attack.cli.command_groups.groups import groups
from mitre_attack.cli.command_groups.malware import malware
from mitre_attack.cli.command_groups.mitigations import mitigations
from mitre_attack.cli.command_groups.relationships import relationships
from mitre_attack.cli.command_groups.software import software
from mitre_attack.cli.command_groups.tactics import tactics
from mitre_attack.cli.command_groups.techniques import techniques
from mitre_attack.cli.command_groups.tools import tools

import click


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.ensure_object(dict)


COMMAND_GROUPS = [
    tactics,
    techniques,
    groups,
    software,
    malware,
    tools,
    mitigations,
    relationships,
]
for command_group in COMMAND_GROUPS:
    cli.add_command(command_group)
