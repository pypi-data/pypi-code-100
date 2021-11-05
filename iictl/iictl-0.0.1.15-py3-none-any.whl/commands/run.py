import click
import iictl.utils.parse as parse
from iictl.commands.main import cli
from iictl.crud.integrated_instance import create_integrated_instance
from iictl.format.integrated_instance import get_integrated_instance_format
from iictl.utils.exception import ParseError, PortError, AlreadyExistError
from iictl.utils.click import global_option
from iictl.utils.kube import verify_object_name

@cli.command(help='Run instance')
@click.option('--name', type=str, help='Instance Name.', required=True)
@click.option('--gpus', default=0, type=int, help='GPU resource requests.')
@click.option('--cpus', default='20', type=str, help='CPU resource limits.')
@click.option('-e', '--env', type=str, multiple=True, help='Environment variables. NAME=VALUE format.')
@click.option('-v', '--volume', type=str, multiple=True, help='Volume mount. VOLUME_NAME:MOUNT_PATH format.') # pvcname:mountpath:ro
@click.option('--domain', type=str, multiple=True, help='Assign domain to port. PORT:DOMAIN format.')
@click.option('-w', '--workdir', 'working_dir', type=str, help='Working directory of container.')
@click.option('--image-pull-secret', type=str, help='Docker registry auth name')
@click.option('--image-pull-policy', type=click.Choice(['Always', 'IfNotPresent', 'Never']), default='Always', help='Image pull policy.')
@click.option('-n', '--namespace', type=str, help='Namespace', callback=global_option)
@click.option('--gpu-node', type=click.Choice(['rtx2080ti', 'rtx3090']), help="GPU model name.")
@click.argument('image')
@click.argument('command', nargs=-1)
def run(name, namespace, env, volume, domain, working_dir, image_pull_secret, image_pull_policy, image, command, gpu_node, gpus, cpus):
    verify_object_name(name)
    
    try:
        envs = parse.parse_envs(env)
        volumes = parse.parse_volumes(volume)
        lb = parse.parse_domains(domain)
    except ParseError as e:
        click.echo(str(e))
        exit(1)
    except PortError as e:
        click.echo(str(e))
        exit(1)
        
    node_selector = {}
    
    if gpu_node == 'rtx2080ti':
        node_selector = {'nvidia.com/gpu.product': 'NVIDIA-GeForce-RTX-2080-Ti'}
    elif gpu_node == 'rtx3090':
        node_selector = {'nvidia.com/gpu.product': 'NVIDIA-GeForce-RTX-3090'}
        
    if gpus == 0:
        envs.append(('NVIDIA_VISIBLE_DEVICES', 'none'))
        
    ii = get_integrated_instance_format(
        name=name,
        image=image,
        command=command,
        lb=lb,
        envs=envs,
        volume_mounts=volumes,
        working_dir=working_dir,
        gpus=gpus,
        cpus=cpus,
        image_pull_secret=image_pull_secret,
        image_pull_policy=image_pull_policy,
        node_selector=node_selector,
    )
    
    try:
        create_integrated_instance(
            namespace=namespace,
            integrated_instance=ii
        )
    except AlreadyExistError as e:
        click.echo(f'integrated instance {name} is already exist')
        exit(1)
    
    click.echo('resource create requested')