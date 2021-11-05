import click
from tabulate import tabulate
from iictl.commands import cli
from iictl.utils.click import global_option
from iictl.crud.pod import list_pod
from iictl.utils import chain_get

@cli.command(help='Print instance list')
@click.option('-n', '--namespace', type=str, help='Namespace', callback=global_option)
@click.option('-o', '--output', type=click.Choice(['default', 'wide']), default='default', help='Output type. "wide" option print more information.')
def ps(namespace, output):
    pods = list_pod(
        namespace=namespace,
        label_selector='deep.est.ai/app',
    )
    
    if output == 'default':
        table = [{
            'NAME': chain_get(pod, ('metadata', 'labels', 'deep.est.ai/app')),
            'IMAGE': chain_get(pod, ('spec', 'containers', 0, 'image')),
            'STATUS': 'Ready' if chain_get(pod, ('status', 'container_statuses', 0, 'ready'), default=False) else 'NotReady',
        } for pod in pods]
        
#         maxcolwidths = [30, 30, 30] # PENDING: from tabulate feature merging issue
    elif output == 'wide':
        table = []
        
        for pod in pods:
            col = {}
            col['NAME'] = chain_get(pod, ('metadata', 'labels', 'deep.est.ai/app'))
            col['IMAGE'] = chain_get(pod, ('spec', 'containers', 0, 'image'))
            col['STATUS'] = 'Ready' if chain_get(pod, ('status', 'container_statuses', 0, 'ready'), default=False) else 'NotReady'
            
            message = chain_get(pod, ('status', 'container_statuses', 0, 'last_state', 'terminated', 'message'), default='')
            message = message or chain_get(pod, ('status', 'container_statuses', 0, 'last_state', 'terminated', 'reason'), default='')
            message = message or chain_get(pod, ('status', 'conditions', 0, 'message'), default='')
            
            message = message or chain_get(pod, ('status', 'container_statuses', 0, 'state', 'waiting', 'message'), default='')
            
            col['MESASGE'] = message
            col['NODE'] = chain_get(pod, ('spec', 'node_name'), default='')
            
            cpu_limit = chain_get(pod, ('spec', 'containers', 0, 'resources', 'limits', 'cpu'), default='0')
            gpu_limit = chain_get(pod, ('spec', 'containers', 0, 'resources', 'limits', 'nvidia.com/gpu'), default='0')
            
            col['RESOURCE_LIMIT'] = f'CPU: {cpu_limit}, GPU: {gpu_limit}'
            
            table.append(col)
        
#         maxcolwidths = [30, 30, 30, 50]
        
        
        
    click.echo(tabulate(table, headers='keys'))