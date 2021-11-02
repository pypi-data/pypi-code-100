import sys, time, traceback, types, inspect
from collections.abc import Iterable

from .client import JellyClient


global __jelly__
__jelly__ = None
def init (*path, **config):
  global __jelly__
  route = []
  for p in path:
    if not isinstance(p, str):
      raise ValueError('path arguments must be string')
    for r in p.split('/'):
      if r:
        route.append(r)
  
  for i, item in enumerate(route):
    if i == 0:
      config['workspace'] = item
    elif i == 1:
      config['project'] = item
    elif i == 2:
      config['process'] = item

  if not __jelly__:
    __jelly__ = JellyClient()
    __jelly__.configure(**config)
  return __jelly__

def serve ():
  global __jelly__
  __jelly__.serve()

def is_primitive (value):
  primtypes = ['int', 'str', 'bool', 'float', 'long', 'NoneType']
  return type(value).__name__ in primtypes

def is_iterable (value):
  return isinstance(value, Iterable)

def is_list (value):
  return isinstance(value, list) or isinstance(value, tuple)

def is_dict (value):
  return isinstance(value, dict)

def is_module (value):
  return type(value).__name__ == 'module'

def is_builtin (value):
  return is_primitive(value) or is_iterable(value) or is_dict(value) or is_module(value)

def is_instance (value):
  return not is_builtin(value)

def flatten (alist, result=None):
  if result is None:
    result = []
  for item in alist:
    if is_list(item):
      flatten(item, result)
    elif is_primitive(item):
      result.append(item)
    else:
      raise Exception('cannot flatten type: ' + type(item).__name__)
  return result


from .html import Elements, ComponentElement

elements = Elements(ComponentElement(None))
div = elements.div
span = elements.span
button = elements.button
input_ = elements.input