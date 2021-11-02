import json
import pytest

from fc.disktracker import local


def test_model_name_parser():
    assert (local.parse_model_name('INTEL SSDSC2BB480G4') ==
            ['INTEL', 'SSDSC2BB480G4'])
    assert local.parse_model_name('Samsung Evo 860') == ['Samsung', 'Evo 860']
    with pytest.raises(ValueError):
        local.parse_model_name('OtherModelString')


def test_local_disk(smartctl):
    disk = local.LocalDisk('scsi', '/dev/sda')
    assert disk.bus == 'scsi'
    assert disk.device == '/dev/sda'

    assert disk.manufacturer == 'LSI'
    assert disk.model == 'Some product'
    assert disk.serial == '006ec9aed58a9f412000f6a11ab0b242'

    disk = local.LocalDisk('/dev/bus/0', 'megaraid,0')
    assert disk.bus == '/dev/bus/0'
    assert disk.device == 'megaraid,0'

    assert disk.manufacturer == 'INTEL'
    assert disk.model == 'SSDSC2BB480G4'
    assert disk.serial == 'PHWL5361036V480QGN'


def test_local_inventory(smartctl):
    inventory = local.LocalInventory()
    inventory.scan()
    assert len(inventory.disks) == 8


def test_smartctl_wrapper(monkeypatch):
    def mocked_run(*args, **kw):
        class Result:
            stdout = '{}'
        r = dict(args=args, kw=kw)
        r = json.dumps(r)
        result = Result()
        result.stdout = r
        return result
    monkeypatch.setattr('subprocess.run', mocked_run)
    assert local.smartctl('--scan') == {
        'args': [['smartctl', '-j', '--scan']],
        'kw': {'check': True, 'encoding': 'ascii', 'stderr': -1, 'stdout': -1}}
