import time, sys, threading, logging, traceback, uuid, os, builtins
from collections import defaultdict, OrderedDict
from uuid import uuid4, getnode
from threading import Thread
from queue import Queue

import multiprocessing
ENV = multiprocessing.get_context("spawn")

from .transport import MQTT
from .logger import JellyLogger, LoggingLevel, _print

LOG = logging.getLogger(__name__)


class JellyRuntime:
  def __init__ (self, client, scope):
    self.client = client
    self.scope = scope

  def evaluate (self, code):
    LOG.log(LoggingLevel.STATUS, 'starting evaluate')
    try:
      exec(code, globals(), self.scope)
    except Exception as err:
      #LOG.error("%s", err)
      LOG.exception(err)
    finally:
      LOG.log(LoggingLevel.STATUS, 'evaluate complete')

class JellyClient:
  def __init__ (self, workspace=None, project=None, process=None, version='v1', host='ws.web-jelly.com', port=1884):
    self.version = version
    self.client_id = str(uuid.uuid4())    
    self.config = dict(
      workspace=workspace, project=project, process=process
    )

    self.transport = MQTT(host, port, self.client_id)
    self.transport.connect()

    self.logging = JellyLogger(self)
    self.rpc = JellyRPC(self)
    self.runtimes = {}
    self.api = dict()

  def set_app (self, api):
    if hasattr(api, '__dict__'):
      self.api = api.__dict__
    elif isinstance(api, dict):
      self.api = api
    else:
      raise ValueError('api must be a dict or object')

  def serve (self):
    while 1:
      time.sleep(0.1)

  def evaluate (self, id, code):
    if not id in self.runtimes:
      self.runtimes[id] = JellyRuntime(self, self.api)
    self.runtimes[id].evaluate(code)

  def kill (self):
    LOG.log(LoggingLevel.STATUS, 'process stopping')
    self.transport.wait_for_publish()
    os._exit(0)
  
  def introduce (self):
    self.publish('status', self.config)

  def make_topic (self, method):
    c = self.config
    topic = "%s/%s/%s/%s/%s/%s/%s/%s" % (
      self.version, c['workspace'], 'client', self.client_id, 
      'outbox', method, c['project'], c['process']
    )
    return topic

  def activate (self, **kw):
    self.config.update(**kw)
    app_path = os.path.abspath(self.config.get('app', '.'))
    sys.path.append(app_path)
    self.logging.activate(**self.config.get('logging', {}))
    self.rpc.activate(**self.config.get('rpc', {}))
    self.introduce()
    LOG.log(LoggingLevel.STATUS, 'process started')

  def publish (self, method, payload):
    topic = self.make_topic(method)
    payload.update(scope=self.get_scope())
    self.transport.publish(topic, payload)

  def get_scope (self):
    c = self.config
    return "%s/%s/%s" % (c['workspace'], c['project'], c['process'])  


# == RPC ==
class Action:
  def __init__ (self, client, action_id, handler):
    self.client = client
    self.id = action_id
    self.handler = handler
  
  def execute (self, param):
    self.client.execute_action(self.id, self.handler, param)

class JellyRPC:
  def __init__ (self, client):
    self.client = client
    self.transport = client.transport
    self.active_calls = {}
    self.actions = {}
    self._main_thread = None
    
  def activate (self, **kwargs):
    self._main_thread = Thread(target=self._main_loop)
    self._main_thread.daemon = True
    self._main_thread.start()

  def _main_loop (self):
    requests = self.transport.subscribe()
    while 1:
      for req in requests:
        try:
          self._handle_request(req)
        except Exception as err:
          traceback.print_exc()
          LOG.exception(err)
      time.sleep(0.01)

  def _handle_request (self, req):
    _print('handle request', req.payload)
    type = req.payload.get('type').lower()
    args = req.payload.get('payload')
    #LOG.info("> %s(%s)", type, args)
    if type == 'evaluate':
      self.client.evaluate(args['id'], args['code'])
    elif type == 'connect':
      self.client.introduce()
    elif type == 'kill':
      self.client.kill()

