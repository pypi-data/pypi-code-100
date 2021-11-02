import pytest
import os
from fc.disktracker import main
from fc.disktracker import local
from fc.disktracker import snipeit


@pytest.fixture(autouse=True)
def mock_snipe_inventory(monkeypatch):

    class MockDisk:
        def __init__(self, serial, manufacturer, model):
            self.serial = serial
            self.manufacturer = manufacturer
            self.model = model

    def __init__(self, url, token,):
        self.has_errors = False
        self.snipe_disks_host = [
            MockDisk('serial1', 'manufacturer1', 'model1')]
        self.checkin_disks = [MockDisk('serial2', 'manufacturer2', 'model2')]
        self.checkout_disks = [MockDisk('serial3', 'manufacturer3', 'model3')]
        self.created_new_server_asset = True
        self.host_name = 'HOSTNAME'

    def update(self, local_inventory):
        pass

    monkeypatch.setattr(
        'fc.disktracker.snipeit.SnipeITInventory.__init__', __init__)
    monkeypatch.setattr(
        'fc.disktracker.snipeit.SnipeITInventory.update', update)


def test_main_no_error(monkeypatch, smartctl, mock_api):
    def return_config():
        return {'token': 'JustSomeStringToBeUsedAsMockToken',
                'url': 'https://some.snipeitinstance.com'}
    monkeypatch.setattr('fc.disktracker.main.get_config', return_config)

    def print_nothing(local_inventory, snipe_inventory):
        pass
    monkeypatch.setattr('fc.disktracker.main.print_result', print_nothing)

    main.main()


def test_main_snipit_error(monkeypatch, capfd, smartctl, mock_api):
    def return_config():
        return {'token': 'JustSomeStringToBeUsedAsMockToken',
                'url': 'https://some.snipeitinstance.com'}
    monkeypatch.setattr('fc.disktracker.main.get_config', return_config)

    def print_nothing(local_inventory, snipe_inventory):
        pass
    monkeypatch.setattr('fc.disktracker.main.print_result', print_nothing)

    def snipe_it_inventory_init_has_errors(self, url, token):
        self.has_errors = True
        pass
    monkeypatch.setattr(
        'fc.disktracker.snipeit.SnipeITInventory.__init__',
        snipe_it_inventory_init_has_errors)
    with pytest.raises(SystemExit) as pytest_wrapped:
        main.main()
    out, err = capfd.readouterr()
    assert pytest_wrapped.type == SystemExit
    assert pytest_wrapped.value.code == 1


def test_print_result(smartctl, mock_snipe_inventory, capsys):
    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory('url', 'token')
    snipe_inventory.update(local_inventory)
    main.print_result(local_inventory, snipe_inventory)

    captured = capsys.readouterr()
    assumed_stdout = '''The asset for server "HOSTNAME" was created!

Disks found locally:
Serial number: P6GTWVZU                       Manufacturer: HGST            Model: HUS724020ALS640
Serial number: K5G4DWJA                       Manufacturer: HGST            Model: HUS726020AL5210
Serial number: K5G4U5UA                       Manufacturer: HGST            Model: HUS726020AL5210
Serial number: K5G562ZA                       Manufacturer: HGST            Model: HUS726020AL5210
Serial number: K5G5Y1YA                       Manufacturer: HGST            Model: HUS726020AL5210
Serial number: K5GHZ0ZA                       Manufacturer: HGST            Model: HUS726020AL5210
Serial number: K5J0NKXG                       Manufacturer: HGST            Model: HUS726020AL5210
Serial number: PHWL5361036V480QGN             Manufacturer: INTEL           Model: SSDSC2BB480G4

Disks checked out to HOSTNAME before:
Serial number: serial1                        Manufacturer: manufacturer1   Model: model1

Disks that were now checked in by disktracker:
Serial number: serial2                        Manufacturer: manufacturer2   Model: model2

Disks that were now checked out to HOSTNAME by disktracker:
Serial number: serial3                        Manufacturer: manufacturer3   Model: model3
'''  # noqa
    assert assumed_stdout == captured.out


def test_get_config(monkeypatch):
    monkeypatch.setattr(
        'fc.disktracker.main.PATH_CONFIG',
        os.path.join(os.path.dirname(__file__), 'etc/disktracker/disktracker.conf'))
    monkeypatch.setattr(
        'fc.disktracker.main.PATH_TOKEN',
        os.path.join(os.path.dirname(__file__), 'etc/disktracker/token'))

    assert main.get_config() == {'token': 'TOKEN', 'url': 'URL'}
