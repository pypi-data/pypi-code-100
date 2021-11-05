import click
from kubernetes import client, config
from iictl.utils.click import global_option_with_default

@click.group()
@click.pass_context
@click.option('-n', '--namespace', type=str, help='Namespace', callback=global_option_with_default('default'))
def cli(ctx, namespace):
    ctx.ensure_object(dict)
    
    
