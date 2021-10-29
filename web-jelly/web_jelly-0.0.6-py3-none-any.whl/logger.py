import inspect, time, sys, builtins, logging, traceback
from uuid import uuid4

_print = builtins.print

def now ():
  return int(time.time() * 1000)

def uuid ():
  return str(uuid4())

def function_name (fn):
  klass = fn.__self__.__class__.__name__
  return "%s.%s" % (klass, fn.__name__)

def _parse_messages (list_of_messages):
  return ' '.join(map(str, list_of_messages))

class LoggingLevel:
  STATUS = 60
  CRITICAL = 50
  ERROR = 40
  WARNING = 30
  INFO = 20
  DEBUG = 10
  NOTSET = 0

def log_level_name (level):
  if level == LoggingLevel.STATUS:
    return 'STATUS'
  elif level == LoggingLevel.CRITICAL:
    return 'CRITICAL'
  elif level == LoggingLevel.ERROR:
    return 'ERROR'
  elif level == LoggingLevel.WARNING:
    return 'WARNING'
  elif level == LoggingLevel.INFO:
    return 'INFO'
  elif level == LoggingLevel.NOTSET:
    return 'NOTSET'
  return ''


class JellyfishLoggingHandler(logging.NullHandler):
  def __init__ (self, client):
    super(JellyfishLoggingHandler, self).__init__()
    self.client = client
    
  def emit(self, record):
    publish_logging_record(self.client, record)


def publish_logging_record (client, record):
  record.levelname = log_level_name(record.levelno)
  message = record.getMessage()
  #message = record.msg
  if record.exc_info:
    try:
      exc = traceback.format_exception(*record.exc_info)
      message += '\n' + '\n'.join(exc)
    except:
      _print('WARNING: failed to format exception')
  #if record.exc_text:
  #  print('publish record exception', record)
  #  message += '\n' + record.exc_text
  #print(record.__dict__)
  #if isinstance(record.msg, str):
  #  message = record.getMessage()
  #else:
  #message = record.msg
  try:
    args = record.args
    if args and not isinstance(args, (tuple, list,)):
      args = [args]  
    items = [client.printer.print_any(arg) for arg in args]
    
    client.publish_log(dict(
      name=record.name, message=record.msg, level=record.levelname,
      levelno=record.levelno, ts=time.time()*1000.0,
      threadid=record.thread, threadName=record.threadName,
      processid=record.process, module=record.module,
      lineno=record.lineno, pathname=record.pathname,
      args=items
    ))
  except Exception as err:
    _print(err)
    #_print(traceback.format_exception(err))
    #traceback.print_exc()

class JellyLogger:

  def __init__ (self, client):
    self.client = client
    self.active_request = None
    self.level = LoggingLevel.INFO
    self.current_print_line = None
    self.printer = ObjectPrinter()

  def activate (self, level='INFO'):
    # NOTE:
    #   for some reason, adding a handler messes with basicConfig somehow
    #   have to use logging factory to intercept logs 
    self.level = LoggingLevel.DEBUG
    _print('activated logging with level', self.level)
    old_factory = logging.getLogRecordFactory()
    def record_factory(*args, **kwargs):
      record = old_factory(*args, **kwargs)
      publish_logging_record(self, record)
      return record
    logging.setLogRecordFactory(record_factory)
    
    print_logger = logging.getLogger('print')
    def new_print (*args, **kwargs):
      end = kwargs.get('end')
      log_msg = " ".join(["%s" for _ in range(len(args))])
      print_logger.info(log_msg, *args)
      _print(*args, **kwargs)
    builtins.print = new_print    
    
    # NOTE: do not do this: (test with basicConfig)
    # logging.root.addHandler(JellyfishLoggingHandler(self))
    
  def publish_log (self, log):
    level = log.get('levelno') # logging.getLevelName(self.level)
    log_level = self.level # logging.getLevelName(log.get('level'))
    #_print('LOG', level, log_level)
    if not isinstance(level, int) or not isinstance(log_level, int):
      return _print('skipped log', level, log_level)
    if log_level <= level:
      log['_id'] = str(uuid())
      #_print('PUBLISH')
      self.client.publish('log', log)
    else:
      _print('skipped log', level, log_level)

  def set_active_request (self, req_id):
    self.active_request = req_id

  



class ObjectPrinter:
  def __init__ (self, full=False):
    self.full = full

  def print_any (self, value):
    result = {'type': 'unknown', 'value': None}
    t = type(value).__name__
    if value is None:
      result = dict(type='null')
    elif isinstance(value, Exception):
      result = {'type': 'error', 'value': dict(type=t, message=str(value))}
    elif t == 'int' or t == 'str' or t == 'bool' or t == 'long' or t == 'float' or t == 'NoneType':
      result = {'type': t, 'value': value}
    elif t == 'dict':
      #result = {'type': 'dict', 'value': {}}
      result = self.print_dict(value)
    elif t == 'list':# or isinstance(value, Iterable):
      #result = {'type': 'list', 'value': []}
      result = self.print_list(value)
    elif t == 'function':
      result = {'type': 'function', 'value': value.__name__}
    elif t == 'type':
      result = {'type': 'type', 'value': value.__name__}
    elif t == 'module':
      result = {'type': 'module', 'value': value.__name__ + '.py'}
    elif hasattr(value, '__render__'):
      return self.print_any(value.__render__())
    elif hasattr(value, '__serialize__'):
      result = value.__serialize__(self.print_any)
    elif hasattr(value, '__dict__'):
      result = self.print_instance(value)
    else:
      result = self.print_instance(value)
    return result

  def print_dict (self, d):
    result = {'type': 'dict', 'value': {}}
    for k,v in d.items():
      result['value'][k] = self.print_any(v)
    return result
    
  def print_list (self, l):
    result = []
    for val in l:
      result.append(self.print_any(val))
    return {'type': 'list', 'value': result}

  def print_instance (self, t):
    result = {}
    #if hasattr(t, '__dict__'):
    #  for k, v in t.__dict__.items():
    #    if k.startswith('_'):
    #      continue
    #    result[k] = self.print_any(v)
    #else:
    #  return {'type': 'str', 'value': str(t)}
    #for k, v in t.__class__.__dict__.items():
    #  if k.startswith('_'):
    #    continue
    #  result[k] = self.print_any(v)
    result = self.print_dict(result)
    return {'type': 'object', 'class': t.__class__.__name__, 'value': result}

    





"""

class Logger:
  def __init__ (self, paths=None):
    self.paths = paths # files not in here will not get logged
    self.logs = []
    
  def clear (self):
    self.logs = []

  def log (self, *messages):
    return self._create_log('LOG', inspect.stack(), *messages)

  def error (self, *messages):
    return self._create_log('ERROR', inspect.stack(), *messages)

  def exception (self, exc):
    type, exc, tb = sys.exc_info()
    info = inspect.getinnerframes(tb)
    info.reverse()
    return self._create_log('ERROR', info, type.__name__, str(exc))

  def parse_value (self, value):
    if is_primitive(value):
      return value
    return repr(value)

  def is_app_frame (self, frame):
    # TODO: use self.paths
    return True
    
  def get_object_path (self, value):
    path = []
    if hasattr(value, '__module__'):
      path.append(getattr(value, '__module__'))
    if hasattr(value, '__class__'):
      path.append(getattr(value, '__class__').__name__)
    return path

  def parse_locals (self, fn_name, _locals, _globals):
    result = {}
    is_method = 'self' in _locals

    parent = []
    fn_object = None
    #if is_method:
    #  parent = self.get_object_path(_locals['self']) + [fn_name]
    #  fn_object = getattr(_locals['self'], fn_name) #.__dict__[fn_name]
    #elif fn_name in _globals:
    #  parent = [_globals['__name__'], fn_name]
    #  fn_object = _globals[fn_name]
    
    for k, v in _locals.items():
      if k.startswith('__') or k == 'self':
        continue
      result[k] = self.parse_value(v)
    return {'locals': result, 'fullpath': '.'.join(parent)}

  def _create_log (self, log_type, stack, *messages):
    items = []
    for msg in messages:
      item = {
        'value': msg, # self.parse_value(msg), 
        'object': id(msg), 'type': type(msg).__name__
      }
      items.append(item)
    
    sdata = []
    for frame in stack:
      if not self.is_app_frame(frame):
        continue
      ldata = self.parse_locals(frame.function, frame.frame.f_locals, frame.frame.f_globals)
      frame_data = {
        #'locals': ldata['locals'], 
        'fullpath': ldata['fullpath'],
        'line': frame.lineno, 'file': frame.filename, 'function': frame.function
      }
      sdata.append(frame_data)

    log = {
      'type': log_type, 'time': int(time.time() * 1000.0),
      'items': items,
      'stack': sdata
    }
    self.logs.append(log)
    return log


class PrintObserver:
  def __init__ (self):
    #self.command = command
    #self.service = service
    self.buffer = [[]]
    self.real_print = builtins.print

  def is_empty (self):
    return len(self.buffer) == 0

  def get (self):
    return self.buffer.pop(0)

  def digest (self):
    while not self.is_empty():
      yield self.get()
      
  def stop (self):
    builtins.print = self.real_print

  def start (self, callback):
    def _print (*args, file=None, end=''):
      self.buffer.append([])
      for item in args:
        #sys.stdout.write(str(item) + ' ')
        self.write(item)
      #sys.stdout.write(end or '\n')
      callback(self.buffer[-1])
    builtins.print = _print

  def write (self, item):
    line = self.buffer[-1]
    line.append(item)
    #if type(item) is str and item.endswith('\n'):
      #self.service.emit(self.command, 'LOG', self.buffer)
    #  self.buffer.append([])

  def flush (self):
    pass

"""