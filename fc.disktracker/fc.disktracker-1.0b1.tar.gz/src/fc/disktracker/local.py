import json
import subprocess
import sys

from fc.disktracker.disk import Disk


def parse_model_name(model_name):
    '''Try to parse a combined Manufacturer/Model string into its parts.

    Returns (manufacturer, model)

    '''
    if model_name.startswith('Samsung ') or model_name.startswith('INTEL '):
        return model_name.split(' ', maxsplit=1)
    else:
        raise ValueError(f'Cannot parse {model_name!r}')


def smartctl(*args):
    try:
        result = subprocess.run(
            ['smartctl', '-j'] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            encoding='ascii')
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as Error:
        for message in json.loads(Error.output)['smartctl']['messages']:
            print(message['string'])
        print(Error)
        sys.exit(1)


class LocalDisk(Disk):

    bus = None
    device = None

    def __init__(self, bus, device):
        self.bus = bus
        self.device = device
        self._scan()

    def _scan(self):
        '''Gather data about this disk from the local machine.'''
        result = smartctl('-i', self.device, '-d', self.bus)

        self.manufacturer = result.get('vendor')
        self.model = result.get('product')

        if not (self.manufacturer and self.model):
            self.manufacturer, self.model = parse_model_name(
                result['model_name'])

        self.serial = result['serial_number']


class LocalInventory(object):

    EXCLUDE_MANUFACTURERS = ['LSI', 'AVAGO']
    EXCLUDE_MODELS = ['PERC H700', 'MR9361-8i']

    def __init__(self):
        self.disks = []

    def scan(self):
        self.disks = []
        smartctl_scan_output = smartctl('--scan')

        for candidate in smartctl_scan_output.get('devices'):
            disk = LocalDisk(candidate['type'], candidate['name'])

            if disk.manufacturer in self.EXCLUDE_MANUFACTURERS:
                continue
            if disk.model in self.EXCLUDE_MODELS:
                continue

            self.disks.append(disk)
