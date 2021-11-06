
from nvdsw.runtimes.runtime import Runtime
import uuid
import logging
import time


log = logging.getLogger('nvaiert')

class nvaie(Runtime):

  def __init__(self):
    self._auth_token = None
    self.user = None
    self.menu_items = {}
    self.menu_items['1001'] = {'id': '1001', 'name': 'PyTorch', 'description': 'GPU Accelerated PyTorch 1.10.0a0+ecc3718 (21.07)'}
    self.menu_items['1002'] = {'id': '1002', 'name': 'Tensorflow 1.X', 'description': 'Tensorflow1 Container v21.07'}
    self.menu_items['1003'] = {'id': '1003', 'name': 'Tensorflow 2.X', 'description': 'Tensorflow2 Container v21.07'}
    self.menu_items['1004'] = {'id': '1004', 'name': 'RAPIDS', 'description': 'RAPIDS Container v21.07'}
    self.menu_items['1005'] = {'id': '1005', 'name': 'PyTorch Lightning', 'description': 'Pytorch Lightning Container v1.3.8'}
    self.menu_items['1006'] = {'id': '1006', 'name': 'Kaggle', 'description': 'Kaggle Container v101'}
    self.menu_items['1007'] = {'id': '1007', 'name': 'Merlin PyTorch', 'description': 'Merlin PyTorch Training Container v0.5.3'}
    self.menu_items['1008'] = {'id': '1008', 'name': 'Merlin Tensorflow', 'description': 'Merlin Tensorflow Training Container v0.5.3'}

    self.flavors = {}
    self.flavors['10001'] = {'id': '10001', 'name': 'tall', 'description': 'small flavor'}
    self.flavors['10002'] = {'id': '10002', 'name': 'grande', 'description': 'medium flavor'}
    self.flavors['10003'] = {'id': '10003', 'name': 'venti', 'description': 'large flavor'}
    self.flavors['10004'] = {'id': '10004', 'name': 'ventissimo', 'description': 'extra large flavor'}

    self.users = {}
    self.users['ubuntu'] = {'userid': 'ubuntu', 'passwd': 'ubuntu', 'name': 'Mark Shuttleworth', 'company': 'Canonical'}
    self.users['acme'] = {'userid': 'acme', 'passwd': 'acme', 'name': 'John Doe', 'company': 'Acme Inc.'}
    self.users['walmart'] = {'userid': 'walmart', 'passwd': 'walmart', 'name': 'Doug McMillon', 'company': 'Walmart'}
    self.users['cia'] = {'userid': 'cia', 'passwd': 'cia', 'name': 'Gina Haspel', 'company': 'CIA'}
    self.users['uhg'] = {'userid': 'uhg', 'passwd': 'uhg', 'name': 'Andrew Witty', 'company': 'UHG'}
    self.users['facebook'] = {'userid': 'facebook', 'passwd': 'facebook', 'name': 'Mark Zuckerberg', 'company': 'Facebook'}
    self.users['google'] = {'userid': 'google', 'passwd': 'google', 'name': 'Sundar Pichai', 'company': 'Google'}

    self.resource_ids = []
    self.resources = {}

  def auth(self, creds): 
    if creds == None:
      return False

    user = self.users.get(creds['userid'])
    if user is None or creds['passwd'] != user['passwd']:
      return False
        
    self.user = user
    return True
 
  def logout(self): 
    self.user = None

  def authed(self):
    # presumably, check if the auth token is not too old?
    if self.user is not None:
      return True
    else:
      return False

    # get the stuff provided with the auth data

  def get_user(self):
    return self.user
    
  def get_menu(self):
    response = {}
    response['error'] = ''
    if not self.authed():
      response['error'] = 'noauth'
      return response

    
    response['items'] = self.menu_items
    return response
            
  def get_flavors(self):
    response = {}
    response['error'] = ''
    if not self.authed():
      response['error'] = 'noauth'
      return response  

    response['items'] = self.flavors
    return response

  def get_flavor(self, flavor_id):
    # nothing to add at this time :-)
    return self.flavors[flavor_id]


  def get_menu_item(self, menu_item_id):
    # nothing to add at this time :-)
    return self.menu_items[menu_item_id]

#   def create_resource1(self, menu_item_id, flavor_id, params = None): 
#     return None

  # this will return resource id
  def create_resource(self, menu_item_id, flavor_id, *params): 
    resource_id = str(uuid.uuid4())
    resource = {'id': resource_id,
               'status': 'active', 
               'rtype': 'remote',
               'menu_item_id': menu_item_id,
               'flavor_id': flavor_id,
               'created': time.time(),
               'url': 'https://10.10.22.23:54345?token=trhuyjjuysarghtws'
               }
    self.resources[resource_id] = resource
    self.resource_ids.append(resource_id)
    return resource_id

  def get_resources(self):
    if not self.authed():
      return {}
    return self.resources

  def get_resource_ids(self):
    if not self.authed():
      return []
    return self.resource_ids

  # for status purposes
  def get_resource(self, resource_id):
    return self.resources.get(resource_id)


  def delete_resource(self, resource_id):
    self.resource_ids.remove(resource_id)
    self.resources.pop(resource_id)
    return True

  def stop_resource(self, resource_id):
    # ideally, this should be gradual and take time.. 
    self.resources[resource_id]['status'] = 'stopped'
    # if this wasn't successful, this should not return true
    # alternatively, this could return a change request id.. 
    return True    

  def start_resource(self, resource_id):
    # ideally, this should be gradual and take time.. 
    self.resources[resource_id]['status'] = 'active'
    # if this wasn't successful, this should not return true
    # alternatively, this could return a change request id..     
    return True 

  def restart_resource(self, resource_id):
    # ideally, this should be gradual and take time.. 
    self.resources[resource_id]['status'] = 'active'
    # if this wasn't successful, this should not return true
    # alternatively, this could return a change request id..     
    return True  


# strictly for testing
if __name__ == '__main__':

  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  log.debug("starting..")

  rt = nvaie()
  log.debug('initially, are we authenticated? ' + str(rt.authed()))

  rc = rt.get_menu()
  log.debug("get_menu before auth returned: " + rc['error'])

  creds = {'userid': 'ubuntu', 'passwd': 'ubuntu'}
  rc = rt.auth(creds)
  log.debug("auth returned: " + str(rc))
  log.debug("are we authed now? " + str(rt.authed()))

  user = rt.get_user()
  log.debug("user name is: " + user['name'])

  rc = rt.get_menu()
  if rc['error'] == '':
    items = rc['items']
    log.debug("get_menu returned: " + str(len(items)) + ' menu items')

  menu_item = rt.get_menu_item('1001')
  log.debug("get_menu_item returned: " + menu_item['name'] )


  rc = rt.get_flavors()
  if rc['error'] == '':
    items = rc['items']
    log.debug("get_flavors returned: " + str(len(items)) + ' flavor items')  

  flavor = rt.get_flavor('10001')
  log.debug("get_flavor returned: " + flavor['name'] )

  resource_id = rt.create_resource('1001', '10001')
  log.debug("create_resource returned: " + resource_id )

  resource = rt.get_resource(resource_id)
  log.debug("get_resource returned: " + resource['url'] + ' status: ' + resource['status'])

  resource_id = rt.create_resource('1001', '10001')
  log.debug("create_resource returned: " + resource_id )

  resource = rt.get_resource(resource_id)
  log.debug("get_resource returned: " + resource['url'] + ' status: ' + resource['status'])

  resources = rt.get_resources()
  log.debug("found " + str(len(resources)) + " resources")
