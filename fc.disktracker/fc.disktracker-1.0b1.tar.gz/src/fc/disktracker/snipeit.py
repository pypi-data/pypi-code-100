import socket
import requests
from fc.disktracker.disk import Disk


class SnipeITDisk(Disk):

    asset_id = None
    checked_out_to_asset_id = None

    def __init__(self, inventory):
        self.inventory = inventory
        self.api = inventory.api

    @classmethod
    def from_local_disk(cls, local_disk, inventory):
        new_disk = SnipeITDisk(inventory)
        new_disk.manufacturer = local_disk.manufacturer
        new_disk.model = local_disk.model
        new_disk.serial = local_disk.serial
        return new_disk

    def create_asset(self):
        '''
        Returns True if disk was created in Snipe-IT, False otherwise. It may
        occur that the disk already does exist in Snipe-IT.
        '''
        manufacturer_id = self.inventory.manufacturers.ensure(self.manufacturer)

        model_id = self.inventory.models.ensure(
            self.model,
            category_id=self.inventory.categories.DISKS,
            manufacturer_id=manufacturer_id)

        r = self.api.post(
            'hardware',
            status_id=self.inventory.status.READY_TO_DEPLOY,
            model_id=model_id,
            serial=self.serial)

        disk_ids = list()
        returned_id = r['id']
        disk_ids.append(returned_id)

        r = self.api.get(
            'hardware',
            search=self.serial,
            category_id=self.inventory.categories.DISKS)
        for entry in r['rows']:
            disk_ids.append(entry['id'])

        if min(disk_ids) == returned_id:
            self.asset_id = returned_id
            return True
        else:
            d = self.api.delete(
                'hardware',
                id=returned_id,
            )
            self.inventory._update_current_snipe_inventory()
            return False

    def checkout(self):
        self.api.post(f'hardware/{self.asset_id}/checkout',
                      checkout_to_type='asset',
                      assigned_asset=self.inventory.host_asset_id)

    def checkin(self):
        self.api.post(f'hardware/{self.asset_id}/checkin')


class SnipeMapping(object):

    labels = {
        'READY_TO_DEPLOY': 'Ready to Deploy',
        'DISKS': 'Disks',
        # Trailing Whitespace is intentional, because snipe.it also contains it
        'GENERIC_SERVER': 'Generic Server ',
        'SERVER': 'Server'}

    def __init__(self, api, endpoint):
        self.api = api
        self.endpoint = endpoint

        self.refresh()

    def refresh(self):
        self.id_by_name = {}
        self.name_by_id = {}
        for entry in self.api.get(self.endpoint)['rows']:
            self._add(entry['id'], entry['name'])

    def _add(self, id, name):
        if name in self.id_by_name and self.id_by_name[name] < id:
            # This is not perfect but should be sufficient for now.
            # We managed to create the same item multiple times but we
            # consistently only use the one with the lowest id.
            return
        self.id_by_name[name] = id
        self.name_by_id[id] = name

    def ensure(self, name, **kw):
        if name in self:
            return self[name]
        return self.add(name, **kw)

    def add(self, name, **kw):
        self.api.post(self.endpoint, name=name, **kw)
        # To catch race conditions where we accidentally created
        # the same object twice, we just load the whole view
        # again and ensure that there are no duplicates.
        self.refresh()
        return self[name]

    def __getitem__(self, name_or_id):
        if isinstance(name_or_id, int):
            return self.name_by_id[name_or_id]
        else:
            return self.id_by_name[name_or_id]

    def __getattr__(self, label):
        label = self.labels[label]
        return self.id_by_name[label]

    def __contains__(self, name):
        return name in self.id_by_name


class APIError(Exception):

    def __init__(self, method, path, params, result):
        self.method = method
        self.path = path
        self.params = params
        self.result = result

    def __repr__(self):
        return (f"{self.method} {self.path}: {self.result['status']} "
                f"{self.result['messages']}")


class API(object):

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get(self, path, **params):
        return self._request(path, params, 'get')

    def post(self, path, **params):
        result = self._request(path, params, 'post')
        if result['status'] != 'success':
            raise APIError('post', path, params, result)
        return result['payload']

    def delete(self, path, **params):
        result = self._request(path, params, 'delete')
        if result['status'] != 'success':
            raise APIError('delete', path, params, result)
        return result

    def _request(self, path, params, method):
        m = getattr(requests, method)
        r = m(
            f'{self.url}/api/v1/{path}',
            headers={
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json',
                'Accept': 'application/json'},
            params=params)
        r.raise_for_status()
        return r.json()


class SnipeITInventory(object):

    def __init__(self, url, token):
        self.api = API(url, token)

        self.snipe_disks = []
        self.snipe_disks_host = []

        self.checkout_disks = []
        self.checkin_disks = []

        self.host_name = socket.gethostname()
        self.created_new_server_asset = False

        self.status = SnipeMapping(self.api, 'statuslabels')
        self.models = SnipeMapping(self.api, 'models')
        self.manufacturers = SnipeMapping(self.api, 'manufacturers')
        self.categories = SnipeMapping(self.api, 'categories')

        # Trigger the well-known attributes for the disks and server
        # categories. If the categories do not exist this causes a somewhat
        # resonable error message to be shown.
        self.categories.DISKS
        self.categories.SERVER

        self.host_asset_id = self._ensure_host_asset_id()
        self.has_errors = False

    def _ensure_host_asset_id(self):
        r = self.api.get(
            'hardware',
            search=self.host_name,
            category_id=self.categories.SERVER)

        # The search is fuzzy. The API does not have a way to explicitly
        # search for the name. Pick the literal match.
        ids = []
        for candidate in r['rows']:
            if candidate['name'] == self.host_name:
                ids.append(candidate['id'])
        id_ = min(ids, default=None)
        if id_ is not None:
            return id_
        else:
            self.api.post(
                'hardware',
                name=self.host_name,
                status_id=self.status.READY_TO_DEPLOY,
                model_id=self.models.GENERIC_SERVER,
                 )
            self.created_new_server_asset = True
            return self._ensure_host_asset_id()

    def update(self, local_disks):
        self._update_current_snipe_inventory()

        # Ensure that for all local disks we do have an asset in
        # Snipe.
        for local_disk in local_disks.disks:
            if local_disk not in self.snipe_disks:
                # Need to create a new asset in Snipe
                disk = SnipeITDisk.from_local_disk(local_disk, self)
                if disk.create_asset():
                    self.snipe_disks.append(disk)

        for disk in self.snipe_disks:
            try:
                if disk in local_disks.disks:
                    # Ensure our local disks are checked out to us
                    if disk.checked_out_to_asset_id == self.host_asset_id:
                        # It's already checked out to us.
                        continue
                    elif disk.checked_out_to_asset_id is not None:
                        # It's checked out somewhere else.
                        self.checkin_disks.append(disk)
                        disk.checkin()
                    self.checkout_disks.append(disk)
                    disk.checkout()
                else:
                    # Ensure disks that are no longer with us are checked in
                    if disk.checked_out_to_asset_id == self.host_asset_id:
                        self.checkin_disks.append(disk)
                        disk.checkin()
            except Exception as e:
                print(e)
                self.has_errors = True

    def _update_current_snipe_inventory(self):
        self.snipe_disks = []
        for asset in self.api.get(
                'hardware', category_id=self.categories.DISKS)['rows']:
            disk = SnipeITDisk(self)
            disk.manufacturer = asset['manufacturer']['name']
            disk.manufacturer_id = asset['manufacturer']['id']
            disk.model = asset['model']['name']
            disk.model_id = asset['model']['id']
            disk.serial = asset['serial']
            disk.asset_id = asset['id']
            if asset['assigned_to']:
                disk.checked_out_to_asset_id = asset['assigned_to']['id']
                if (disk.checked_out_to_asset_id ==
                        self.host_asset_id and
                        disk not in self.snipe_disks_host):
                    self.snipe_disks_host.append(disk)
            self.snipe_disks.append(disk)
