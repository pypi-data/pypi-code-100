import sys
import configparser

from fc.disktracker.local import LocalInventory
from fc.disktracker.snipeit import SnipeITInventory

LINE_TEMPLATE = (
    'Serial number: {disk.serial: <30} Manufacturer: {disk.manufacturer: <15} '
    'Model: {disk.model}')
PATH_CONFIG = '/etc/disktracker/disktracker.conf'
PATH_TOKEN = '/etc/disktracker/token'


def get_config():
    conf = configparser.ConfigParser()
    conf.read(PATH_CONFIG)

    token = open(PATH_TOKEN, 'r').readline().strip()
    url = conf['snipe.it']['url']

    return {'token': token, 'url': url}


def print_result(local_inventory, snipe_inventory):
    if snipe_inventory.created_new_server_asset:
        print(f'The asset for server "{snipe_inventory.host_name}" '
              'was created!')
        print()

    print('Disks found locally:')
    for disk in sorted(local_inventory.disks):
        print(LINE_TEMPLATE.format(disk=disk))
    print()

    print(f'Disks checked out to {snipe_inventory.host_name} before:')
    for disk in sorted(snipe_inventory.snipe_disks_host):
        print(LINE_TEMPLATE.format(disk=disk))
    print()

    print('Disks that were now checked in by disktracker:')
    for disk in sorted(snipe_inventory.checkin_disks):
        print(LINE_TEMPLATE.format(disk=disk))
    print()

    print(f'Disks that were now checked out to {snipe_inventory.host_name} '
          'by disktracker:')
    for disk in sorted(snipe_inventory.checkout_disks):
        print(LINE_TEMPLATE.format(disk=disk))


def main():
    config = get_config()

    if len(sys.argv) > 1 and sys.argv[1] == '--print-config':
        print(f'SnipeIT token is:\n{config["token"]}')
        print(f'SnipeIT url is:\n{config["url"]}')
        sys.exit(0)

    local_inventory = LocalInventory()
    local_inventory.scan()

    snipe_inventory = SnipeITInventory(config['url'],
                                       config['token'])
    snipe_inventory.update(local_inventory)

    print_result(local_inventory, snipe_inventory)

    if snipe_inventory.has_errors:
        sys.exit(1)
