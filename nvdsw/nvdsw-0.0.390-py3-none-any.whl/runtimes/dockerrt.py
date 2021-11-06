
from gi.repository import GLib
import os

from nvdsw.runtimes.runtime import Runtime
import uuid
import logging
import time
import iso8601

import docker
import traceback
import sys
import threading, queue
from threading import RLock
import pathlib
# import ctypes

from docker import APIClient

log = logging.getLogger('dockerrt')
PKG_DIR = str(pathlib.Path(__file__).parent.absolute())

# def trace_function(): 
#   print("Passing the trace function and current thread is:", str(threading.current_thread().getName())) 

class SoftKillableThread(threading.Thread):
  def softkill(self):
    self.softkilled = True


  def is_softkilled(self):
    try:
      sk = self.softkilled
    except Exception:
      self.softkilled = False

    return self.softkilled

class dockerrt(Runtime):

  def __init__(self, config, ymenus, settings):

    # low level docker cli
    self.cli = docker.APIClient(base_url='unix://var/run/docker.sock')

    # regular docker client
    self.dc = docker.from_env()
    self.config = config
    self.ymenus = ymenus
    self.settings = settings

    self.menu_items = {}

    # this is an ephemeral structure, meaning it gets wiped when the client is restarted
    # the idea is to keep track of / state of operations such as forced image pull or pause, which will not be persisted
    # also, the regular pull of latest tags needs this structure to prevent re-adding the unpulled images to the pull queue
    # not all images will have an entry here but just thosee touched by the user or the threads
    # key: image name (img:tag)
    # value: status: queued, paused, pulling
    self.ephem_img_status = {}
    self.ephem_img_status_lock = RLock()

    # this is for attaching log windows to image pulls
    self.img_pull_widgets = {}
    self.img_pull_widget_lock = RLock()

    # key: img, value: thread id that's woring on it
    self.imgs_being_pulled = {}
    self.imgs_being_pulled_lock = RLock()


    # no flavors yet
    self.flavors = {}

    self.resource_ids = []
    self.resources = {}

    self.img_pull_queue = queue.Queue()
    self.img_pull_threads = []

    if settings.get()['Experimental']['LAUNCHER_ENABLED']:
      # this thread will periodically monitor the state of the latest tags. If any are missing, they will be appended to the img pull queue
      self.img_check_thread = threading.Thread(target=self.img_check_loop)
      self.img_check_thread.daemon = True
      self.img_check_thread.start()

##      threading.settrace(trace_function())

      for i in range(self.settings.get()['Containers']['IMAGE_PULL_THREAD_POOL_SIZE']):
        t = SoftKillableThread(target=self.img_pull_loop)
        t.daemon = True
        
        t.start()
        self.img_pull_threads.append(t)
    else:
      log.info('experimental launcher interface not enabled, not starting threads')

  def img_check_loop(self):
    while True:
      log.info('image check thread waking up')
      # checking in the loop because this setting could have changed by the user dynamically
      if self.settings.get()['Containers']['AUTOPULL_LATEST_IMAGES']:
        images = self.get_menu()['items'].items()
        for _, i in images:
          # check just the most recent tag...
          _, t = list(i['tags'].items())[0]
#          print(i['image'])
#          print(t['tag'])
          img_name = i['image'] + ':' + t['tag']
          if t['status'] != 'pulled':
            # need to also check for pulling, paused in the ephemeral mem structure
            with self.ephem_img_status_lock:
              if self.ephem_img_status.get(img_name) is None:
                log.info('image ' + i['image'] + ' and tag ' + t['tag'] + ' have status ' + t['status'] + ' so adding to pull queue..')
                self.img_pull_queue.put((i,t))
                # need to update the ephemeral memory structure so the thread does not keep adding the same image over and over
                self.ephem_img_status[img_name] = 'queued'
            

      IMG_CHECK_INTERVAL = int(self.config['MAIN']['IMG_CHECK_INTERVAL'])
      log.info('image check thread sleeping for ' + self.config['MAIN']['IMG_CHECK_INTERVAL'])
      time.sleep(IMG_CHECK_INTERVAL)

  def img_pull_loop(self):
    while True:
      i,t = self.img_pull_queue.get()
      # this item is now gone from the queue
      log.info('autopull thread waking up')
      log.info('fetched image ' + i['image'] + ' and tag ' + t['tag'] + ' from pull queue..')
      
      img = i['image']
      tag = t['tag']
      img_name = img + ':' + tag

  
      
      with self.ephem_img_status_lock:
        estat = self.ephem_img_status.get(img_name)
        if estat == 'queued':
          log.info("img_pull_thread starting to pull " + img_name)
          self.ephem_img_status[img_name] = 'pulling'
        else:
          # this should not happen. only process items in the 'queued' state
          log.warning('WEIRD! pulled from queue item ' + img_name + ' with ephem stat '+ str(estat) + ' ..ignoring i guess..' )
          continue

      DOCKERFILE_DIR = PKG_DIR + '/../' + self.config['MAIN']['DOCKERFILE_DIR']
      dockerpath = DOCKERFILE_DIR + '/' + img
      dockerfile = 'Dockerfile' + '.' + tag

      log.debug("building image " + img_name + ' from ' + dockerfile)

      # announce that we are working on this image.. 
      with self.imgs_being_pulled_lock:
        # self.imgs_being_pulled[img_name] = threading.get_native_id()
        self.imgs_being_pulled[img_name] = threading.currentThread()
   
      
      try:
        ##self.dc.images.build(tag = img_name, path = dockerpath, dockerfile = dockerfile)
        
#        cli = docker.APIClient()
        response = self.cli.build(tag = img_name, path = dockerpath, dockerfile = dockerfile, decode = True)
        img_paused = False
        dotCount = 0
        for line in response:
          # how many dots in a row have we emitted
          with self.img_pull_widget_lock:
            widg = self.img_pull_widgets.get(img_name)
            if widg is not None:
              # don't even parse if there's no window
              pline = self.parse_docker_api_output_line(line)
              if pline is not None:
                if pline == '.':
                  dotCount += 1
                else:
                  if dotCount > 0:
                    # terminate the dots
                    pline = '\n' + pline
                    dotCount = 0
                if dotCount > 50:
                  pline += '\n'
                  dotCount = 0
                GLib.idle_add(self.append_line_to_widget, widg, pline)


          if threading.currentThread().is_softkilled():
            log.info('Thread softkilled, interrupting this image pull')
            response.close()
            threading.currentThread().softkilled = False
            log.info("image " + img_name + " goes into paused state")
            with self.ephem_img_status_lock:
              self.ephem_img_status[img_name] = 'paused'
            img_paused = True

        if img_paused == True:
          continue

      except Exception:
        log.error("unable to build image " + img_name)
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.error(traceback.format_exception(exc_type, exc_value, exc_tb))  
        log.error("image " + img_name + " goes into paused state")
        with self.ephem_img_status_lock:
          self.ephem_img_status[img_name] = 'paused'

        continue
      finally:
        # we are done with this image
        with self.imgs_being_pulled_lock:
          self.imgs_being_pulled.pop(img_name)

      log.debug("built image " + img_name)
      # remove the img_name from the ephem structure .. it's now pulled
      with self.ephem_img_status_lock:
        self.ephem_img_status.pop(img_name)
  
  def parse_docker_api_output_line(self, line):
    if line is None:
      return None

    if line.get('stream') is not None:
      # just print a dot and be done with it.. doing backspace chars on the spinning thingy is weird
      return '.'
    if line.get('status') is not None:
#      try:
        p = line.get('progressDetail')
        if p is None or len(p) == 0:
        # if p is None or p.get('current') is None:
          pl = line.get('status') + ':' + line.get('id') 
          log.debug('line: ' + str(line))
          log.debug('pline: ' + pl)
          return pl

        perc = 100 * p.get('current')/ p.get('total')
        pl = line.get('status') + ' ' + line.get('id') + ' {:.2f} %\n'.format(perc) # + ' %\n'
        return pl
#      except:
#        log.error('failed to parse: ' + str(line))
#      return 
    # if we are here, not sure what to do
    if line.get('aux') is not None and line.get('aux').get('ID') is not None:
      return line.get('aux').get('ID')

    log.warning('failed to parse: ' + str(line))
    return str(line)

  # append a line of output to the textview buffer
  def append_line_to_widget(self, textview, line):
    buf = textview.get_buffer()
    end_iter = buf.get_end_iter()
    buf.insert(end_iter, line)

    text_mark_end = buf.create_mark("", buf.get_end_iter(), False)
    textview.scroll_to_mark(text_mark_end, 0, False, 0, 0)

  # no auth yet
  def auth(self, creds): 
    return True

  # # no auth yet
  def logout(self): 
    return True

  # no auth yet
  def authed(self):
    return True

  # no auth yet
  def get_user(self):
    return None
    
  def get_image(self, img_name):
    try:
      i = self.dc.images.get(img_name)
      return i
    except docker.errors.ImageNotFound:
      log.debug("image " + img_name + " is not present locally")  
      return None
    except Exception:
      log.warning("unable to connect to docker")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      return None

  def get_menu(self, active_only = False):
    
    if active_only:
      return self.get_active_menu()

    # no caching since all is dynamic
    self.menu_items = {}
    response = {}
    response['error'] = ''
    if not self.authed():
      response['error'] = 'noauth'
      return response

    for j in self.ymenus['jupyter']:
      # just pass the yaml through
      mitem = j.copy()
      tags = {}
      for tag in mitem['tags']:
        img = self.get_image(mitem['image'] + ':' + tag) 
        if img is not None:
          tags[tag] =  {'id': img.short_id, 'tag': tag, 'status': 'pulled'}
          tags[tag] ['created'] = iso8601.parse_date(img.attrs['Created']).timestamp()
          tags[tag] ['size'] = img.attrs['Size']
        else:
          es = self.get_ephem_img_status(mitem['image'] + ':' + tag)
          if es is None:
            tags[tag] =  {'id': '', 'tag': tag, 'status': 'not pulled'}
          else:
            tags[tag] =  {'id': '', 'tag': tag, 'status': es}

        # overwrite the original list with the new dict
        mitem['tags'] = tags
        self.menu_items[mitem['id']] = mitem
           
    response['items'] = self.menu_items
    return response

  def get_active_menu(self):
    
    # get only the images that are being pulled or queued or paused at the moment
    # this is just an ephemeral list that excludes any images that docker knows about and requies to queries to it.
    # FAST!
    # there is no caching of this whatsoever
    menu_items = {}
    response = {}
    response['error'] = ''
    if not self.authed():
      response['error'] = 'noauth'
      return response

    for j in self.ymenus['jupyter']:
      mitem = j.copy()
      tags = {}
      for tag in mitem['tags']:
        es = self.get_ephem_img_status(mitem['image'] + ':' + tag)
        if es is not None:
          tags[tag] =  {'id': '', 'tag': tag, 'status': es}
        mitem['tags'] = tags
        menu_items[mitem['id']] = mitem
           
    response['items'] = menu_items
    return response

  # no flavors yet      
  def get_flavors(self):
    response = {}
    response['error'] = ''
    response['items'] = self.flavors
    return response

  # no flavors yet
  def get_flavor(self, flavor_id):
    return self.flavors[flavor_id]


  def get_ephem_img_status(self, img_tag):
    with self.ephem_img_status_lock:
      es = self.ephem_img_status.get(img_tag)
      return es

  def attach_widget_menu_item_tag_caching(self, widj, menu_item, tag):
    img_name = menu_item['image'] + ':' + tag['tag']
    with self.img_pull_widget_lock:
      self.img_pull_widgets[img_name] = widj
      log.debug('attached widget to ' + img_name)

  def remove_widget_menu_item_tag_caching(self, menu_item, tag):
    img_name = menu_item['image'] + ':' + tag['tag']
    with self.img_pull_widget_lock:
      self.img_pull_widgets.pop(img_name)
      log.debug('removed widget from ' + img_name)

  def cache_menu_item_tag(self, menu_item_id, tag_id):
    menu_item = self.get_menu_item(menu_item_id)
    tag = menu_item['tags'][tag_id]
    img_name = menu_item['image'] + ':' + tag_id
    log.debug('processing request to cache ' + img_name)
    if tag['status'] == 'not pulled' or tag['status'] == 'paused':
      # need to also check for pulling, paused in the ephemeral mem structure
      with self.ephem_img_status_lock:
        es = self.ephem_img_status.get(img_name)
        if es is None or es == 'paused':
          log.info('image ' + menu_item['image'] + ' and tag ' + tag['tag'] + ' have ephem status ' + str(es) + ' so force adding to pull queue..')
          self.img_pull_queue.put((menu_item,tag))
          self.ephem_img_status[img_name] = 'queued'
        else:
          log.warning('image ' + img_name + ' has ephem status ' + es + 'so not trying to add it to the queue again')
          return False

    else:
      log.warning('image ' + img_name + ' has status of ' + tag['status'] + ' so not trying to add it to the queue again')
      return False
    
    return True

    

  def uncache_menu_item_tag(self, menu_item_id, tag_id):
    menu_item = self.get_menu_item(menu_item_id)
    tag = menu_item['tags'][tag_id]
    img_name = menu_item['image'] + ':' + tag_id

    # hopefully, if we are here, the image is present locally and is not in the queue.. 
    if tag['status'] != 'pulled':
      log.warning('image ' + img_name + ' has status of ' + tag['status'] + ' so not trying to remove it')
      return False

    log.debug('processing request to delete ' + img_name)

    
    # this really shouldn't happen but let's take a look in the ephem structure too..
    with self.ephem_img_status_lock:
      es = self.ephem_img_status.get(img_name)
      if es is not None:
        log.debug("image " + img_name + 'has status ' + es + ' so not trying to remove it as it likely does not exist locally. ')
        return False
    
    try:
      self.dc.images.remove(img_name, force = True)
    except docker.errors.ImageNotFound:
      log.info("image " + img_name + " is not present locally")  
      return False
    except docker.errors.APIError:
      log.info("docker.errors.APIError")  
      return False
    except Exception:
      log.warning("unable to remove " + img_name)
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))
      return False

    
    log.debug('successfully deleted ' + img_name)
    return True
    # if the user deleted the latest tag for some image, it's possible that it'll immediately get entered back into the queue
    # that's okay

  def get_thread_id_for_img_being_pulled(self, img_name):
    with self.imgs_being_pulled_lock:
      return self.imgs_being_pulled.get(img_name)

  def pause_caching_menu_item_tag(self, menu_item_id, tag_id):
    menu_item = self.get_menu_item(menu_item_id)
    tag = menu_item['tags'][tag_id]
    img_name = menu_item['image'] + ':' + tag_id
    log.debug('processing request to pause ' + img_name)
    
    # paranoid safety checks..
    if tag['status'] == 'pulled':
      log.warning('image ' + img_name + ' has status of ' + tag['status'] + ' so not trying to pause it')
      return False

    with self.ephem_img_status_lock:
      es = self.ephem_img_status.get(img_name)
      if es is None:
        log.debug("image " + img_name + 'is not in the pull queue so not trying to pause it. ')
        return False
      elif es == 'queued':
        self.ephem_img_status[img_name] = 'paused'
        log.debug("image " + img_name + ' was paused')
        return True
      elif es == 'pulling':
        log.debug("image " + img_name + ' is being pulled.. we need to pause it but this is not yet implemented')
        thread = self.get_thread_id_for_img_being_pulled(img_name)
        if thread is not None:
          thread.softkill()
#        tid = self.get_thread_id_for_img_being_pulled(img_name)
#        if tid is not None:
#          log.debug("Thread working on img is: " + str(tid))
#          res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(SystemExit))
#          print(res)
        else:
          log.debug('could not find thread working on our image')

      else:
        # should never get here
        log.warning('image ' + img_name + ' has status of ' + tag['status'] + ' so not trying to pause it')
        return False
    

  def unpause_caching_menu_item_tag(self, menu_item_id, tag_id):
    img_name = self.get_menu_item(menu_item_id)['image'] + ':' + tag_id
    log.debug('putting request to unpause ' + img_name + ' back in the queue..')
    # this item was in the queue; put it back into the queue
    return self.cache_menu_item_tag(menu_item_id, tag_id)

  def get_menu_item(self, menu_item_id, pull_tag_status = True):
    # go to the source for information.
    # update our in-memory structure

    # this existing one could have old tag status, but the list of tags isn't changed.
    mitem = self.menu_items.get(menu_item_id)

    # the point of skipping tag status is speed
    if not pull_tag_status:
      return mitem

    tags = {}
    for tag in mitem['tags']:
      img = self.get_image(mitem['image'] + ':' + tag) 
      if img is not None:
        tags[tag] =  {'id': img.short_id, 'tag': tag, 'status': 'pulled'}
        tags[tag] ['created'] = iso8601.parse_date(img.attrs['Created']).timestamp()
        tags[tag] ['size'] = img.attrs['Size']
      else:
        es = self.get_ephem_img_status(mitem['image'] + ':' + tag)
        if es is None:
          tags[tag] =  {'id': '', 'tag': tag, 'status': 'not pulled'}
        else:
          tags[tag] =  {'id': '', 'tag': tag, 'status': es}

      # overwrite the original list with the new dict
      mitem['tags'] = tags
    return mitem

  # this will return resource id
  def create_resource(self, menu_item_id, flavor_id, tag, attrs): 
    
    menu_item = self.get_menu_item(menu_item_id)
    if menu_item is None:
      log.error("unknown menu item id: " + menu_item_id)
      return None

    if not tag in menu_item['tags']:
      log.error('tag ' + tag + ' is not known')
      return None
    
    t = menu_item['tags'][tag]
    if t['id'] == '':
      log.error('tag ' + tag + ' has no id and status of ' + t['status'])
      return None

    image_id = t['id']

    envs = menu_item['environment']
    # some envs are lists so we can put weird cased vars in there
    if envs is not None and type(envs) is dict:
      for k,vv in envs.items():
        if vv is None:
          log.info("config file has no value for key " + k + " so trying env")
          v1 = os.getenv(k)
            
          if v1 is None:
            log.info("still could not get value. oh well")
          else:
            log.info("in env found value " + v1 + " for key " + k)
            envs[k] = v1

    remove_flag = False
    # this label will always be attached to the containers
    default_label = self.config['MAIN']['DOCKER_GENERAL_LABEL']
    container_label = menu_item['container_label']

    # shouldn't this also be a label?
    
    labels = {}
    labels[default_label] = ''
    labels[container_label] = ''
    labels['nvdsw_menu_item_id'] = menu_item_id
    labels['nvdsw_tag'] = tag

    if attrs.get('ports') is not None:
      browser_port = list(attrs['ports'].keys())[0]
      labels['nvdsw_browser_port'] = browser_port

#    if self.config['MAIN']['DOCKER_REMOVE_FLAG'] == 'True':
#      remove_flag = True

    name = None
    if attrs['name'] != 'auto-assigned':
      name = attrs['name']

    device_requests=[]
    gpus = []
    if attrs.get('gpus') is not None:
      for gpu in attrs['gpus']:
        log.debug('gpu: ' + gpu)
        gpus.append(gpu) 

      dr = docker.types.DeviceRequest(device_ids = gpus, capabilities=[['gpu']])
      device_requests.append(dr)
    
    if len(device_requests) > 0:
      docker_runtime = 'nvidia'
    else:
      docker_runtime = 'runc'

    # likely need to check that this image actually exists??
    try: 
      # menu_item['image'] + ':' + latest_tag,menu_item['command']
      c = self.dc.containers.run(image_id, menu_item['command'],
        detach = True, ipc_mode = 'host', remove = remove_flag, volumes = attrs.get('volumes'),
        labels = labels, entrypoint = menu_item['entrypoint'], ports = attrs.get('ports'), 
        environment = envs, name = name, runtime = docker_runtime, device_requests = device_requests)
    except docker.errors.ImageNotFound: 
      log.error('could not create container, image not found')
      return None
    except Exception:
      log.error("unable to create container")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.error(traceback.format_exception(exc_type, exc_value, exc_tb))  
      return None

    except docker.errors.ContainerError:
      log.error('could not create container, ContainerError')
      return None

    except docker.errors.APIError:
      log.error('could not create container, APIError')
      return None
      
    cs = c.status

    cnm = c.attrs['Name'].split('/')[-1]
    log.debug("the container is up and running with name " + cnm + " and status " + cs)
#     print(c.attrs['Created'])


    # likely need more fields in the resource 
    # the url is fake for now.
    resource = self.container2resource(c)
    self.resources[c.short_id] = resource
    self.resource_ids.append(c.short_id)
    return c.short_id

  def container2resource(self,c):
    r = {}
    try:
      r['id'] = c.short_id
      r['name'] = c.name
      r['gpus'] = self.parse_gpu_nums(c.attrs['HostConfig']['DeviceRequests'])
      r['ports'] = self.parse_ports(c.attrs['NetworkSettings']['Ports'])
      r['volumes'] = c.attrs['HostConfig']['Binds']
      r['status'] = c.status
      r['rtype'] = 'local'

    ## skipping this for speed purposes.. We don't display image_id on the running row, per se
    ##  r['image_id'] = c.image.short_id
      
      if c.labels.get('nvdsw_menu_item_id') is None:
        log.info('container ' + c.name + ' does not have the menu item id tag, skipping')
        return None

      r['menu_item_id'] = c.labels['nvdsw_menu_item_id']
      r['tag'] = c.labels['nvdsw_tag']

      # let us not load the logs to speeed things up
      ## r['logs'] = c.logs(timestamps = True)

      r['created'] = iso8601.parse_date(c.attrs['Created']).timestamp()


      if 'nvdsw_browser_port' in c.labels:
        container_browser_port = c.labels['nvdsw_browser_port']
        r['browser_port'] = container_browser_port
        p = c.attrs['NetworkSettings']['Ports']
        k = p.get(container_browser_port)
        if k is not None:
          host_browser_port = k[0]['HostPort']
          r['url'] = "http://localhost:" + host_browser_port + "/lab"
    except docker.errors.NotFound:
      # the container may die at any time..
      return None
    except Exception:
      log.warning("unable to parse container")
      exc_type, exc_value, exc_tb = sys.exc_info()
      log.warning(traceback.format_exception(exc_type, exc_value, exc_tb))  
      return None
    return r

  def get_resources(self):
    if not self.authed():
      return {}

    # no caching
    self.resource_ids = []
    self.resources = {}

    filt = {}
    filt['label'] = self.config['MAIN']['DOCKER_GENERAL_LABEL']
    cs = self.dc.containers.list(filters = filt, all = True)
    for c in cs:
#      if self.config['MAIN']['DOCKER_GENERAL_LABEL'] in c.labels:
    
        r = self.container2resource(c)
        if r is not None:
          self.resource_ids.append(c.short_id)
          self.resources[c.short_id] = r

    return self.resources

  def get_resource_ids(self):
    if not self.authed():
      return []

    # no caching
    self.resource_ids = []

    filt = {}
    filt['label'] = self.config['MAIN']['DOCKER_GENERAL_LABEL']
    cs = self.dc.containers.list(filters = filt, sparse = True)
    for c in cs:
  #    if self.config['MAIN']['DOCKER_GENERAL_LABEL'] in c.labels:
        self.resource_ids.append(c.short_id)
        
    return self.resource_ids

  # for status purposes

  def get_resource(self, resource_id):
    try: 
      c = self.dc.containers.get(resource_id)
    except docker.errors.NotFound:
      log.error('container ' + resource_id + ' does not exist')
      # need to remove it from mem
      try: 
        self.resource_ids.remove(resource_id)
      except ValueError:
        log.info('the resource_id was already gone from resource_ids')
      self.resources.pop(resource_id, None)

      return None
    except docker.errors.APIError:
      log.error('could not create container, API Error')
      return None

    r = self.container2resource(c)
    if r is not None:
      self.resources[resource_id] = r
    else:
      try: 
        self.resource_ids.remove(resource_id)
      except ValueError:
        log.info('the resource_id was already gone from resource_ids')
      self.resources.pop(resource_id, None)
    return r


  def delete_resource(self, resource_id):
    c = None
    try:
      c = self.dc.containers.get(resource_id)
    except docker.errors.NotFound:
      log.warning('container with id ' + resource_id + ' was not found')
      try: 
        self.resource_ids.remove(resource_id)
      except ValueError:
        log.info('the resource_id was already gone from resource_ids')
      self.resources.pop(resource_id, None)
    except docker.errors.APIError:
      log.error('docker api error')
      return False
    
    if c is not None:
      try:
        c.remove(force = True)
        try: 
          self.resource_ids.remove(resource_id)
        except ValueError:
          log.info('the resource_id was already gone from resource_ids')

        self.resources.pop(resource_id, None)
      except docker.errors.APIError:
        log.error('docker api error, unable to remove container')
        return False

    return True
      

  def stop_resource(self, resource_id):

    c = None
    try:
      c = self.dc.containers.get(resource_id)
    except docker.errors.NotFound:
      log.warning('container with id ' + resource_id + ' was not found')
      try: 
        self.resource_ids.remove(resource_id)
      except ValueError:
        log.info('the resource_id was already gone from resource_ids')

      self.resources.pop(resource_id, None)
      return False
    except docker.errors.APIError:
      log.error('docker api error')
      return False
    
    if c is not None:
      try:
        c.stop(timeout = int(self.config['MAIN']['DOCKER_STOP_TIMEOUT']))
        self.resources[resource_id]['status'] = c.status
        return True
      except docker.errors.APIError:
        log.error('docker api error, unable to stop container')
        return False
    else:
      return False    

  def start_resource(self, resource_id):

    # should we wait for the web server to catch up?  
    c = None
    try:
      c = self.dc.containers.get(resource_id)
    except docker.errors.NotFound:
      log.warning('container with id ' + resource_id + ' was not found')
      try:
        self.resource_ids.remove(resource_id)
      except ValueError:
        log.info('the resource_id was already gone from resource_ids')

      self.resources.pop(resource_id, None)
      return False
    except docker.errors.APIError:
      log.error('docker api error')
      return False
    
    if c is not None:
      try:
        c.start()
        self.resources[resource_id]['status'] = c.status
        return True
      except docker.errors.APIError:
        log.error('docker api error, unable to start container')
        return False
      except Exception:
        log.error("unable to start container")
        exc_type, exc_value, exc_tb = sys.exc_info()
        log.error(traceback.format_exception(exc_type, exc_value, exc_tb))  
        return False
    else:
      return False   

  def restart_resource(self, resource_id):


    # should we wait for the web server to catch up?   
    c = None
    try:
      c = self.dc.containers.get(resource_id)
    except docker.errors.NotFound:
      log.warning('container with id ' + resource_id + ' was not found')
      try:
        self.resource_ids.remove(resource_id)
      except ValueError:
        log.info('the resource_id was already gone from resource_ids')
      self.resources.pop(resource_id, None)
      return False
    except docker.errors.APIError:
      log.error('docker api error')
      return False
    
    if c is not None:
      try:
        c.restart(timeout = int(self.config['MAIN']['DOCKER_STOP_TIMEOUT']))
        self.resources[resource_id]['status'] = c.status
        return True
      except docker.errors.APIError:
        log.error('docker api error, unable to restart container')
        return False
    else:
      return False 

  def parse_ports(self, ports):
    parsed_ports = {}
    for k,v in ports.items():
      # {'6006/tcp': None, '8888/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '49168'}, {'HostIp': '::', 'HostPort': '49168'}]}
      container_port = k
#       print(k)
#       print(v)
      if v is not None:
        local_port = v[0]['HostPort']
        parsed_ports[container_port] = local_port

    return parsed_ports


  def parse_gpu_nums(self, device_str):
  #  log.debug("in parse_gpu_nums")
   # >>> c.attrs['HostConfig']['DeviceRequests']
   # [{'Driver': '', 'Count': 0, 'DeviceIDs': ['0'], 'Capabilities': [['gpu']], 'Options': {}}]
    gpunums = []
    for ds in device_str:
      gpu_capable = False
      for i in ds['Capabilities']:

        for j in i:
          if j == 'gpu':
            gpu_capable = True
            break
          
        if gpu_capable:  # flatten this list
          for dev_id in ds['DeviceIDs']:
            gpunums.append(int(dev_id))
  #  for g in gpunums:
  #    log.debug("parse_gpu_nums: found gpu " + str(g))
    return gpunums

# strictly for testing
if __name__ == '__main__':

  import configparser
  import yaml
  import pathlib
  from nvdsw.tools.settings_yaml import SettingsYaml

  log.setLevel(logging.DEBUG)
  log.addHandler(logging.StreamHandler())
  log.debug("starting..")

  PKG_DIR = str(pathlib.Path(__file__).parent.absolute())
#   print(PKG_DIR)
  config = configparser.ConfigParser()
  # case-sensitive
  config.optionxform = str
  config.read(PKG_DIR + '/../config/config.ini')

  menus_fname = PKG_DIR + "/../" + config['MAIN']['MENUS_YAML']
  try:
    ymenus = yaml.load(open(menus_fname, 'r'), Loader=yaml.SafeLoader) 
  except FileNotFoundError:
    log.error("menus file not found " + menus_fname)

# usersettings = None
  settings = SettingsYaml(PKG_DIR + "/../" + config['MAIN']['USERSETTINGS_YAML'])
  try:
    settings.load() 
  except FileNotFoundError:
    log.error("settings file not found " + config['MAIN']['USERSETTINGS_YAML'])  

  rt = dockerrt(config, ymenus, settings)

  rc = rt.get_menu()
  if rc['error'] == '':
    items = rc['items']
    log.debug("get_menu returned: " + str(len(items)) + ' menu items')
#     print(items)
    for _,m in items.items():
      log.debug('menu item id: '+ m['id'] + ' name: ' + m['name'] + ' tags: '+ str(m['tags']))

  menu_item = rt.get_menu_item('1001')
  log.debug("get_menu_item returned: " + menu_item['name'] )


  rc = rt.get_flavors()
  if rc['error'] == '':
    items = rc['items']
    log.debug("get_flavors returned: " + str(len(items)) + ' flavor items')  

  attrs = {}
  attrs['name'] = 'auto-assigned'
  attrs['ports'] = {'8888/tcp': ''}
  resource_id = rt.create_resource(menu_item_id = '1005', flavor_id = None, tag = '21.08', attrs = attrs)
  log.debug("create_resource returned: " + resource_id )
  log.debug("get_resource returned: " + str(rt.get_resource(resource_id)) )

  rc = rt.stop_resource(resource_id)
  log.debug("stop_resource returned: " + str(rc))
  log.debug("get_resource returned: " + str(rt.get_resource(resource_id)) )

  rc = rt.start_resource(resource_id)
  log.debug("start_resource returned: " + str(rc))
  log.debug("get_resource returned: " + str(rt.get_resource(resource_id)) )

  rc = rt.restart_resource(resource_id)
  log.debug("restart_resource returned: " + str(rc))
  log.debug("get_resource returned: " + str(rt.get_resource(resource_id)) )

#   resource = rt.get_resource(resource_id)
#   log.debug("get_resource returned: " + resource['url'] + ' status: ' + resource['status'])

  resource_id = rt.create_resource(menu_item_id = '1000', flavor_id = None, tag = '21.07', attrs = attrs)
  log.debug("create_resource returned: " + resource_id )
  log.debug("get_resource returned: " + str(rt.get_resource(resource_id)) )

#   resource = rt.get_resource(resource_id)
#   log.debug("get_resource returned: " + resource['url'] + ' status: ' + resource['status'])

  resources = rt.get_resources()
  log.debug("found " + str(len(resources)) + " resources")
  for id, r in list(resources.items()):
    print(r)
    rt.delete_resource(id)
