import inspect, time, sys, builtins, logging, traceback, re, hashlib
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

class LogType:
  LOG=0
  EVENT=1

class JellyfishLoggingHandler(logging.NullHandler):
  def __init__ (self, client):
    super(JellyfishLoggingHandler, self).__init__()
    self.client = client
    
  def emit(self, record):
    publish_logging_record(self.client, record)


def create_stack (stack):
  info = inspect.getinnerframes(stack)
  stack_data = []
  for frame in info:
    frame_data = {
      'source': ''.join(frame.code_context),
      'line': frame.lineno, 'file': frame.filename, 'function': frame.function
    }
    stack_data.append(frame_data)
  return stack_data

def publish_logging_record (client, record):
  record.levelname = log_level_name(record.levelno)
  message = record.getMessage()
  try:
    stack = None
    log_type = LogType.LOG
    log_hash = None
    msg = record.msg
    args = record.args
    
    if record.exc_info:
      exc = traceback.format_exception(*record.exc_info)
      msg = ''.join(exc)
      args = []
      log_type = LogType.EVENT
      stack = create_stack(record.exc_info[2])
      hash_value = record.exc_info[0].__name__ + ':' + '-'.join([s['source'] for s in stack])
      
      hash_object = hashlib.md5(hash_value.encode())
      log_hash = str(hash_object.hexdigest())
    elif not isinstance(msg, str):
      args = [msg]
      msg = "%s"
    
    if args and not isinstance(args, (tuple, list,)):
      args = [args]  
    items = [client.printer.print_any(arg) for arg in args]
    
    shape = "%s:%s:%s:%s:%s" % (
      len(message), len(list(re.finditer("\r\n?|\n", message))),
      len(msg), len(list(re.finditer("\r\n?|\n", message))),
      len(args)
    )
    client.publish_log(dict(
      name=record.name, msg=msg, level=record.levelname,
      levelno=record.levelno, ts=time.time()*1000.0,
      thread=record.thread, threadName=record.threadName,
      process=record.process, module=record.module,
      lineno=record.lineno, pathname=record.pathname,
      args=items, message=message, shape=shape,
      stack=stack, type=log_type, hash=log_hash
    ))
  except Exception as err:
    _print(traceback.format_exc())

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
    #builtins.print = new_print    
    
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
      try:
        self.client.publish('log', log)
      except:
        _print('failed to publish log')
        _print(log)
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
      result = self.print_dict(value)
    elif t == 'list':
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
    result = self.print_dict(result)
    return {'type': 'object', 'class': t.__class__.__name__, 'value': result}

    