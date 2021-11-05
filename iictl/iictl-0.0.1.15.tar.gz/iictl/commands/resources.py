import click
from tabulate import tabulate
from iictl.commands.main import cli
from iictl.crud.pod import list_pod
from iictl.crud.node import list_node
from iictl.utils import chain_get
from collections import defaultdict

@cli.command(help='View resources.')
def resources():
    pods = list_pod(
        field_selector='status.phase!=Failed,status.phase!=Succeeded',
    )
    
    node_resources = defaultdict(list)
    
    for pod in pods:
        node_name = chain_get(pod, ('spec', 'node_name'))
        
        if node_name is None:
            continue
        
        for container in chain_get(pod, ('spec', 'containers'), default=[]):
            node_resources[node_name].append(container.get('resources', {}))

    node_gpu_allocated = {}
    for node_name, resources in node_resources.items():
        gpu = 0
        
        for resource in resources:
            gpu += int(chain_get(resource, ('requests', 'nvidia.com/gpu'), default='0'))
        
        node_gpu_allocated[node_name] = gpu
    
    
    nodes = list_node()
    
    node_gpu_capacity = {}
    for node in nodes:            
        gpu_count = int(chain_get(node, ('status', 'capacity', 'nvidia.com/gpu'), default='0'))
        gpu_product = chain_get(node, ('metadata', 'labels', 'nvidia.com/gpu.product'), default='')
            
        node_gpu_capacity[node['metadata']['name']] = (gpu_product, gpu_count)
    
    node_gpu_allocatable = [{
        'NODE NAME': node,
        'GPU MODEL': gpu_product,
        'ALLOCATABLE GPU': gpu_count - node_gpu_allocated[node],
    } for node, (gpu_product, gpu_count) in node_gpu_capacity.items()]
        
    
    click.echo(tabulate(node_gpu_allocatable, headers='keys'))
