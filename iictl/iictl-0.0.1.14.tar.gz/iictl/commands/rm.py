import click
from iictl.commands.main import cli
from iictl.crud.integrated_instance import delete_integrated_instance
from iictl.utils.exception import NotFoundError
from iictl.utils.click import global_option
from iictl.utils.kube import verify_object_name

@cli.command(help='Remove instance')
@click.option('-f', '--force', is_flag=True, help='[DEPRECATED] Forced deletion instance.')
@click.option('-n', '--namespace', type=str, help='Namespace', callback=global_option)
@click.argument('name', nargs=-1)
def rm(name, force, namespace):
    if len(name) == 0:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
            
    for it in name:
        verify_object_name(it)
        
        try:
            delete_integrated_instance(
                namespace=namespace,
                name=it
            )
        except NotFoundError as e:
            click.echo(f'integrated instance "{it}" not found')
        else:
            click.echo(f'integrated instance "{it}" deleted')
