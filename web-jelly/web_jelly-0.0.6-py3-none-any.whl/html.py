import traceback, json, types
from . import (
  is_primitive, is_module, is_dict, is_iterable, is_instance, is_list, is_builtin
)





class ComponentElement:
  def __init__ (self, engine):
    self.engine = engine
    self.handler = None
    self._elements = {}
    self.subcomponents = {}
    self._active_elements = set()

  def diff_elements (self, e1, e2):
    if e1.type != e2.type:
      return True
    if type(e1) is not type(e2):
      return False
    if isinstance(e1, TextElement):
      return e1.value != e2.value
    elif isinstance(e1, Element):
      keys = e1.props.keys() & e2.props.keys()
      for k in keys:
        if e1.props.get(k) != e2.props.get(k):
          return True
    return False

  def create_element (self, parent, index, element):
    #key = parent + '.' + str(index)
    item = {'id': element.key, 'index': index, 'parent': parent.key, 'element': element.as_dict()}
    self._elements[item['id']] = element
    return item

  def open_element (self, element):
    return {'action': 'OPEN', 'element': element.as_dict()}

  def close_element (self, element):
    return {'action': 'CLOSE', 'element': element.as_dict()}
  
  def render_to_string (self, template):
    result = ''
    listeners = {}
    for item in self.render('', template):
      e = item['element']
      if e['type'] == 'TEXT':
        result += str(e['value'])
        continue
      props = []
      print(item)

      if item['action'] == 'CLOSE':
        result += '</%s>' % e['type']
        continue
      props.append('data-key="%s"' % e['key'])
      for k, v in e['props'].items():
        props.append('%s="%s"' % (k, v))
      
      listeners.setdefault(e['key'], {})
      listeners[e['key']].update(e['listeners'])
        
      for k, v in e['listeners'].items():
        #print(k, v, type(v))
        props.append('''on%s="ON_EVENT('%s', this);"''' % (k, k))
      result += '<%s%s%s>' % (
        e['type'], ' ' if len(props) else '', ' '.join(props)
      )
    result += '''
<script>
register_listeners(%s)
</script>
''' % listeners
    return result

  def render (self, root, template):
    #self.handler = handler
    self._elements = {}
    root_element = Element(self, None, 'div', [])
    root_element.key = root
    result = template
    try:
      if isinstance(result, Element):
        yield from self.render_element(root_element, 0, result)
      elif is_primitive(result):
        yield from self.render_element(root_element, 0, result)
      elif isinstance(result, (types.GeneratorType, list, tuple,)):
        for index, element in enumerate(result):
          yield from self.render_element(root_element, index, element)
      else:
        raise Exception('unknown render result: ' + repr(result))
      yield from self.render_subcomponents()
    except Exception as err:
      #if hasattr(self.handler, 'state'):
      #  pprint.pprint(self.handler.state._items())
      traceback.print_exc()
      yield from self.render_element(root_element, 0, str(err))

  def render_element (self, parent, index, obj):
    element = None
    if is_primitive(obj):
      element = TextElement(parent, obj)
    elif isinstance(obj, Node):
      element = obj
    else:
      element = ComponentRef(parent, obj)
    element.key = "%s.%s" % (parent.key, index)
    #yield self.create_element(parent, index, element)
    yield self.open_element(element)
    if hasattr(element, 'children'):
      for child_index, child in enumerate(self.list_children(element, element.children)):
        #child.parent = element
        #parent_key = "%s.%s" % (parent, index)
        yield from self.render_element(element, child_index, child)
      yield self.close_element(element)

  def list_children (self, element, children):
    for item in children:
      if is_list(item):
        yield from self.list_children(element, item)
      #elif is_primitive(item):
      #  element = TextElement(element, item)
      else:
        yield item
      #elif is_primitive(item):
      #  yield TextElement(element, item)
      #elif isinstance(item, Node):
      #  yield item
      #else:
      #  yield ComponentRef(element, item)

  def render_subcomponents (self):
    comps = {k: c for (k, c) in self._elements.items() if c.type == 'REF'}
    for key, comp in comps.items(): 
      if not key in self.subcomponents:
        self.subcomponents[key] = ComponentElement(self.engine)
      subcomp = self.subcomponents[key]
      yield from subcomp.render(key, comp.component)


  # API METHODS
  @property
  def elements (self):
    return Elements(self)

  def emit (self, type, **kw):
    return Event(type, **kw)


class Event:
  def __init__ (self, id, type, **kw):
    self.id = id
    self.type = type
    self.payload = kw

  def trigger (self, payload):
    self._on_trigger(payload)

  def on_trigger (self, callback):
    self._on_trigger = callback
    return self
  
  def emit (self, **values):
    return EventTrigger(self, values)


class EventTrigger:
  def __init__ (self, event, values):
    self.event = event
    self.payload = values
  
  def as_dict (self):
    return {'id': self.event.id, 'type': self.event.type, 'payload': self.payload}


class Elements:
  def __init__ (self, ctx):
    self.ctx = ctx
  def __getattr__ (self, name):
    return ElementSignature(self.ctx, None, name)

class ElementSignature:
  def __init__ (self, ctx, parent, type, **props):
    self.ctx = ctx
    self.type = type
    self.parent = parent
    
  def __call__ (self, id=None, **props):
    return Element(self.ctx, self.parent, self.type, id, **props)

class Node:
  def __init__ (self, type, parent):
    self.key = ''
    self.type = type
    self.parent = parent

  @property
  def id (self):
    return ''
  
  @property
  def test (self):
    p = self.parent
    keys = [self.id]
    while p:
      keys.insert(0, p.id)
      p = p.parent
    return '/'.join(keys)

class TextElement(Node):
  def __init__ (self, parent, value):
    super().__init__('TEXT', parent)
    self.value = value

  @property
  def id (self):
    return str(hash(self.value))
  
  def as_dict (self):
    return {'type': self.type, 'value': self.value}

class ComponentRef(Node):
  def __init__ (self, parent, component):
    super().__init__('REF', parent)
    self.component = component

  @property
  def id (self):
    return self.component.__class__.__name__

  def as_dict (self):
    return {'type': self.type}
  
def to_dict (x):
  if is_primitive(x) or isinstance(x, dict):
    return x
  if hasattr(x, 'as_dict'):
    return x.as_dict()
  return None  

class Element(Node):
  def __init__ (self, ctx, parent, type, id, **props):
    super().__init__(type, parent)
    self.ctx = ctx
    self.props = props
    self.children = [] # ctx.list_children(self, children)
    self.listeners = {}
    if id:
      self.props['id'] = id

  @property
  def id (self):
    return self.props.get('id', '')

  def __serialize__ (self, serializer):
    props = {k: parse_prop(p) for (k, p) in self.props.items()}
    listeners = {k: parse_trigger(v) for (k, v) in self.listeners.items()}
    return dict(type='html', value=dict(
      type=self.type, props=props, 
      listeners=listeners, key=self.key,
      children=[serializer(c) for c in self.children]
    ))

  def on (self, **listeners):
    self.listeners.update(listeners)
    return self

  def click (self, trigger):
    return self.on(click=trigger)

  def style (self, **props):
    # TODO: do not overwrite any existing styles, unless it's a re-render
    if not 'style' in self.props:
      self.props['style'] = {}
    self.props['style'].update(**props)
    return self
    style_string = ''
    for k, v in props.items():
      key = k.replace('_', '-')
      style_string += "%s:%s;" % (key, v)
    self.props['style'] = style_string
    return self

  def classes (self, *classnames, **classes):
    names = {k for (k,v) in classes.items() if v} | set(classnames)
    new_names = set(self.props.get('class', '').split(' ')) | names
    #self.props['class'] = ' '.join(new_names)
    self.props['className'] = ' '.join(new_names)
    return self

  def __call__ (self, *children):
    self.children = self.ctx.list_children(self, children)
    return self


# TODO: this should be element-based
#  for example, "line" element will expect "point" elements in "points" attribute
#  have some "extract_elements("points")" maybe
def parse_prop (prop):
  if hasattr(prop, 'as_dict'):
    return prop.as_dict()['props']
  elif isinstance(prop, list):
    return [parse_prop(p) for p in prop]
  return prop

def parse_trigger (trigger):
  return trigger.as_dict()



import uuid

class RenderContext:
  def __init__ (self):
    #self.id = id
    #self.mqtt = mqtt
    self.component = ComponentElement(None)
    self.events = {}
    self.state = {}

  def set_state (self, **values):
    self.state.update(values)

  # API METHODS
  @property
  def elements (self):
    return Elements(self.component)

  def trigger (self, evt):
    self.events[evt['id']].trigger(evt['payload'])

  def event (self, type, **kw):
    id = str(uuid.uuid4())
    evt = Event(id, type, **kw)
    self.events[id] = evt
    return evt

  def render (self, template):
    html = self.component.render_to_string(template)
    return html
    #self.mqtt.publish('v1/output/' + self.id, dict(
    #  type='HTML', event='RENDER', message=html, request_id=self.id
    #))