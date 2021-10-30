import importlib
from .cdn_client import CdnClient
from .nas_client import NasClient
from .dds_client import DdsClient
from .kafka_client import KafkaClient
from .order_client import OrderClient
from .vpn_client import VpnGatewayClient
from proxy_tools import proxy


prod_mapper = {
    'cdn': CdnClient,
    'nas': NasClient,
    'dds': DdsClient,
    'kafka': KafkaClient,
    'order': OrderClient,
    'vpn': VpnGatewayClient
}


def get_current_client(prod):
    module = importlib.import_module('cloudplatform_auth')
    get_access_func = getattr(module, 'get_alicloud_access_info')
    access_key_id, access_key_secret, region, config = get_access_func()
    return prod_mapper[prod](access_key_id, access_key_secret, region, config)


@proxy
def cdn_client():
    return get_current_client('cdn')


@proxy
def nas_client():
    return get_current_client('nas')


@proxy
def dds_client():
    return get_current_client('dds')


@proxy
def kafka_client():
    return get_current_client('kafka')


@proxy
def order_client():
    return get_current_client('order')


@proxy
def vpn_client():
    return get_current_client('vpn')