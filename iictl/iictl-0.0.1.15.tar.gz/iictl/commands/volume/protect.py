import click
from iictl.commands.volume.main import volume
from iictl.crud.persistent_volume_claim import patch_persistent_volume_claim
from iictl.utils.exception import NotFoundError
from iictl.utils.click import global_option
from iictl.utils.kube import verify_object_name

@volume.command(help='Protect volume')
@click.option('-n', '--namespace', type=str, help='Namespace', callback=global_option)
@click.argument('name')
def protect(name, namespace):
    verify_object_name(name)
    
    try:
        patch_persistent_volume_claim(
            name=name,
            namespace=namespace,
            body={'metadata':{'annotations':{'deep.est.ai/volume-protection': 'true'}}}
        )

        click.echo(f'A volume {name} was protected.')
    except NotFoundError as e:
        click.echo(f'volume "{name}" not found')