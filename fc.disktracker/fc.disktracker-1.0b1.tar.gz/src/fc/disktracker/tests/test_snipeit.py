from fc.disktracker import snipeit
from fc.disktracker import local
import requests
import pytest


config = {'token': 'TOKEN',
          'url': 'URL'}


@pytest.fixture(autouse=True)
def gethostname(monkeypatch):
    def mocked_hostname():
        return 'patty'
    monkeypatch.setattr('socket.gethostname', mocked_hostname)


@pytest.fixture()
def responses_200(monkeypatch):
    class MockResponse(object):
        def __init__(self, status_code, url, headers):
            self.status_code = status_code
            self.url = url
            self.headers = headers

        def raise_for_status(self):
            pass

        def json(self):
            return {'status': 'success',
                'messages': 'Asset created successfully. :)',
                'payload': {'PAYLOAD'}}

    def mock_get(url, headers, params):
            return MockResponse(200, url, headers)

    def mock_post(url, headers, params):
            return MockResponse(200, url, headers)

    def mock_delete(url, headers, params):
            return MockResponse(200, url, headers)

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'post', mock_post)
    monkeypatch.setattr(requests, 'delete', mock_delete)


@pytest.fixture()
def responses_201(monkeypatch):
    class MockResponse(object):
        def __init__(self, status_code, url, headers):
            self.status_code = status_code
            self.url = url
            self.headers = headers

        def raise_for_status(self):
            pass

        def json(self):
            return {
                   'status': 'error',
                   'messages': {
                     'status_id': [
                       'The selected status id is invalid.']}}

    def mock_post(url, headers, params):
        return MockResponse(201, url, headers)

    def mock_delete(url, headers, params):
       return MockResponse(201, url, headers)

    monkeypatch.setattr(requests, 'post', mock_post)
    monkeypatch.setattr(requests, 'delete', mock_delete)


def test_snipe_mapping_no_change(mock_api):

    api = snipeit.API(config['url'],
                      config['token'])

    status = snipeit.SnipeMapping(api, 'statuslables')
    status._add(5, 'Ready to Deploy')
    assert status.READY_TO_DEPLOY == 2
    assert status.__getitem__(2) == 'Ready to Deploy'

    categories = snipeit.SnipeMapping(api, 'categories')
    assert categories.DISKS == 2
    assert categories.SERVER == 4

    models = snipeit.SnipeMapping(api, 'models')
    assert models.GENERIC_SERVER == 3


def test_snipe_mapping_missing_category(mock_api):

    api = snipeit.API(config['url'],
                      config['token'])

    categories = snipeit.SnipeMapping(api, 'categories')
    assert categories.SERVER == 4

    with pytest.raises(KeyError) as execinfo:

        categories.DISKS

    assert 'Disks' in str(execinfo.value)


def test_snipe_mapping_missing_model(mock_api):

    api = snipeit.API(config['url'],
                      config['token'])

    models = snipeit.SnipeMapping(api, 'models')
    models.ensure('new model')
    assert models.name_by_id[12345] == 'new model'


def test_api_init(monkeypatch, responses_200):

    api = snipeit.API(config['url'],
                      config['token'])
    assert api.url == 'URL'
    assert api.token == 'TOKEN'


def test_api_get(monkeypatch, responses_200):
    api = snipeit.API(config['url'],
                      config['token'])
    r = api.get('hardware', search='test', category_id=4)
    assert r == {
        'status': 'success',
        'messages': 'Asset created successfully. :)',
        'payload': {'PAYLOAD'}}


def test_api_post(monkeypatch, responses_200):
    api = snipeit.API(config['url'],
                      config['token'])
    p = api.post('hardware', name='name')
    assert p == {'PAYLOAD'}


def test_api_post_error(monkeypatch, responses_201):
    api = snipeit.API(config['url'],
                      config['token'])

    with pytest.raises(snipeit.APIError) as execinfo:
        api.post('hardware', name='name')

    assert ("""\
('post', 'hardware', {'name': 'name'}, \
{'status': 'error', \
'messages': {'status_id': ['The selected status id is invalid.']}})"""
            in str(execinfo.value))


def test_api_delete(monkeypatch, responses_200):
    api = snipeit.API(config['url'],
                      config['token'])
    d = api.delete('hardware', id=2,)
    assert d == {
        'status': 'success',
        'messages': 'Asset created successfully. :)',
        'payload': {'PAYLOAD'}}


def test_api_delete_error(monkeypatch, responses_201):
    api = snipeit.API(config['url'],
                      config['token'])

    with pytest.raises(snipeit.APIError) as execinfo:
        api.delete('hardware', id=2,)

    assert ("""\
('delete', 'hardware', {'id': 2}, \
{'status': 'error', \
'messages': {'status_id': ['The selected status id is invalid.']}})"""
            in str(execinfo.value))


def test_snipe_inventory_no_change(smartctl, mock_api):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])
    snipe_inventory.update(local_inventory)

    assert len(snipe_inventory.snipe_disks) == 9

    serials = ['K5G5Y1YA',
               'K5G4DWJA',
               'K5GHZ0ZA',
               'K5J0NKXG',
               'P6GTWVZU',
               'K5G4U5UA',
               'K5G562ZA',
               'PHWL5361036V480QGN']

    for snipe_disk in snipe_inventory.snipe_disks_host:
        assert snipe_disk.serial in serials
        serials.remove(snipe_disk.serial)


def test_snipe_inventory_one_new_disk(smartctl, mock_api):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])
    snipe_inventory.update(local_inventory)

    assert len(snipe_inventory.snipe_disks) == 9

    serials = ['K5G5Y1YA',
               'K5G4DWJA',
               'K5GHZ0ZA',
               'K5J0NKXG',
               'P6GTWVZU',
               'K5G4U5UA',
               'K5G562ZA',
               'PHWL5361036V480QGN']

    for snipe_disk in snipe_inventory.snipe_disks_host:
        assert snipe_disk.serial in serials
        serials.remove(snipe_disk.serial)

    assert len(snipe_inventory.checkout_disks) == 1
    assert snipe_inventory.checkout_disks[0].serial == 'K5G5Y1YA'


def test_snipe_inventory_one_new_disk_but_newer_exists(smartctl, mock_api):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])
    snipe_inventory.update(local_inventory)

    serials = ['K5G5Y1YA',
               'K5G4DWJA',
               'K5GHZ0ZA',
               'K5J0NKXG',
               'P6GTWVZU',
               'K5G4U5UA',
               'K5G562ZA',
               'PHWL5361036V480QGN']

    for snipe_disk in snipe_inventory.snipe_disks_host:
        assert snipe_disk.serial in serials
        serials.remove(snipe_disk.serial)

    assert len(snipe_inventory.checkout_disks) == 1
    assert snipe_inventory.checkout_disks[0].serial == 'K5G5Y1YA'


def test_snipe_inventory_check_in_one_disk(smartctl, mock_api):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])
    snipe_inventory.update(local_inventory)

    assert len(snipe_inventory.snipe_disks) == 9

    serials = ['K5G5Y1YA',
               'K5G4DWJA',
               'K5GHZ0ZA',
               'K5J0NKXG',
               'P6GTWVZU',
               'K5G4U5UA',
               'K5G562ZA',
               's-e-r-i-a-l-2',
               'PHWL5361036V480QGN']

    for snipe_disk in snipe_inventory.snipe_disks_host:
        assert snipe_disk.serial in serials
        serials.remove(snipe_disk.serial)

    assert len(snipe_inventory.checkin_disks) == 1
    assert snipe_inventory.checkin_disks[0].serial == 's-e-r-i-a-l-2'


def test_snipe_inventory_local_disk_checked_out_to_different_server(
        smartctl, mock_api):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])
    snipe_inventory.update(local_inventory)

    assert len(snipe_inventory.snipe_disks) == 9

    serials = ['K5G5Y1YA',
               'K5G4DWJA',
               'K5GHZ0ZA',
               'K5J0NKXG',
               'P6GTWVZU',
               'K5G4U5UA',
               'K5G562ZA',
               's-e-r-i-a-l-2',
               'PHWL5361036V480QGN']

    for snipe_disk in snipe_inventory.snipe_disks_host:
        assert snipe_disk.serial in serials
        serials.remove(snipe_disk.serial)

    assert len(snipe_inventory.checkin_disks) == 1
    assert snipe_inventory.checkin_disks[0].serial == 'PHWL5361036V480QGN'

    assert len(snipe_inventory.checkout_disks) == 1
    assert snipe_inventory.checkout_disks[0].serial == 'PHWL5361036V480QGN'


def test_snipe_inventory_create_host_asset(smartctl, mock_api):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])
    snipe_inventory.update(local_inventory)

    assert len(snipe_inventory.snipe_disks) == 9
    assert len(snipe_inventory.snipe_disks_host) == 0

    serials_checkin = ['K5G5Y1YA',
                       'K5G4DWJA',
                       'K5GHZ0ZA',
                       'K5J0NKXG',
                       'P6GTWVZU',
                       'K5G4U5UA',
                       'K5G562ZA',
                       'PHWL5361036V480QGN']

    assert len(snipe_inventory.checkin_disks) == 8

    for snipe_disk in snipe_inventory.checkin_disks:
        assert snipe_disk.serial in serials_checkin
        serials_checkin.remove(snipe_disk.serial)

    serials_checkout = ['K5G5Y1YA',
                        'K5G4DWJA',
                        'K5GHZ0ZA',
                        'K5J0NKXG',
                        'P6GTWVZU',
                        'K5G4U5UA',
                        'K5G562ZA',
                        'PHWL5361036V480QGN']
    for snipe_disk in snipe_inventory.checkout_disks:
        assert snipe_disk.serial in serials_checkout
        serials_checkout.remove(snipe_disk.serial)


def test_snipe_inventory_has_errors(smartctl, mock_api, monkeypatch):

    local_inventory = local.LocalInventory()
    local_inventory.scan()

    snipe_inventory = snipeit.SnipeITInventory(config['url'],
                                               config['token'])

    def raise_api_error(self):
        raise snipeit.APIError(
            'method', 'path', 'params',
            {'messages': 'MESSAGE', 'status': 'STATUS'})

    monkeypatch.setattr(
        'fc.disktracker.snipeit.SnipeITDisk.checkout', raise_api_error)
    monkeypatch.setattr(
        'fc.disktracker.snipeit.SnipeITDisk.checkin', raise_api_error)

    snipe_inventory.update(local_inventory)
    assert snipe_inventory.has_errors


def test_api_error():
    error = snipeit.APIError(
        'method', 'path', 'params',
        {'messages': 'MESSAGE', 'status': 'STATUS'})
    assert isinstance(error, Exception)
    assert repr(error) == 'method path: STATUS MESSAGE'
