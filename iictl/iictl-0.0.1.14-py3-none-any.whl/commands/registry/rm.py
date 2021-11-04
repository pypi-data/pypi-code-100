import click
from iictl.commands.registry.main import registry
from iictl.crud.secret import read_secret
from iictl.crud.secret import delete_secret
from iictl.utils.exception import NotFoundError
from iictl.utils.click import global_option
from iictl.utils.kube import verify_object_name

@registry.command(help='Remove registry') #really meant it?()
@click.option('-n', '--namespace', type=str, help='Namespace', callback=global_option)
@click.argument('name')
def rm(name, namespace):
    verify_object_name(name)
    
    try:
        delete_secret(
            name=name,
            namespace=namespace,
        )
        click.echo(f'secret "{name}" was deleted.')
    except NotFoundError as e:
        click.echo(f'secret "{name}" not found')
        exit(1)
