from urllib.parse import urlparse
from biolib.biolib_api_client import RemoteHost
from biolib.biolib_docker_client import BiolibDockerClient
from biolib.biolib_logging import logger
from biolib.compute_node.remote_host_proxy import RemoteHostProxy
from biolib.compute_node.webserver.webserver_types import WebserverConfig
from biolib.typing_utils import List

_BIOLIB_ENCLAVE_REMOTE_HOSTS: List[RemoteHost] = [
    {'hostname': 'biolib-cloud-api.s3.amazonaws.com'},
    {'hostname': 'prod-eu-west-1-starport-layer-bucket.s3.eu-west-1.amazonaws.com'},
    {'hostname': 'biolib.com'},
    {'hostname': 'containers.biolib.com'},
    {'hostname': 'containers.staging.biolib.com'},
    {'hostname': 'staging-elb.biolib.com'},
]


def start_enclave_remote_hosts(config: WebserverConfig) -> None:
    logger.debug('Starting Docker network for enclave remote host proxies')
    docker = BiolibDockerClient.get_docker_client()
    public_network = docker.networks.create(
        driver='bridge',
        internal=False,
        name='biolib-enclave-remote-hosts-network',
    )

    biolib_remote_host_proxies: List[RemoteHostProxy] = []
    base_hostname = urlparse(config['base_url']).hostname
    if not base_hostname:  # Make sure base_hostname is not None for typing reasons
        raise Exception('Base hostname not set, likely due to base url not being set. This is required in enclaves')

    _BIOLIB_ENCLAVE_REMOTE_HOSTS.append({'hostname': base_hostname})

    logger.debug('Starting enclave remote host proxies')
    for remote_host in _BIOLIB_ENCLAVE_REMOTE_HOSTS:
        remote_host_proxy = RemoteHostProxy(remote_host, public_network, internal_network=None, job_id=None)
        remote_host_proxy.start()
        biolib_remote_host_proxies.append(remote_host_proxy)

    logger.debug('Writing to enclave /etc/hosts')
    with open('/etc/hosts', mode='a') as hosts_file:
        for proxy in biolib_remote_host_proxies:
            ip_address = proxy.get_ip_address_on_network(public_network)
            hosts_file.write(f'\n{ip_address} {proxy.hostname}')
