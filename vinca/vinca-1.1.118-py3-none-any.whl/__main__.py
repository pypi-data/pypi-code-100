'''Vinca 112
Simple Spaced Repetition'''

import inspect as _inspect
from pathlib import Path as _Path
from vinca.cardlist import Cardlist as _Cardlist
from vinca.card import Card as _Card
from vinca.config import config
from vinca.generators import generators_dict as _generators_dict
import fire as _fire

# load the card generators into the module
for _hotkey, _generator_func in _generators_dict.items():
	locals()[_generator_func.__name__] = _generator_func
	locals()[_hotkey] = _generator_func

# create a collection (cardlist) out of all the cards
_ALL_CARDS = [_Card(int(id.name)) for id in config.cards_path.iterdir()] 
col = _Cardlist(_ALL_CARDS)
# import all the methods of the collection object directly into the module's namespace
for _method_name, _method in _inspect.getmembers(col):
	locals()[_method_name] = _method

# utility functions
help = lambda: 'Use --help instead'
version = lambda: 112

_fire.Fire()
'''
Add the following code to the ActionGroup object in helptext.py of fire to get proper aliasing
A better way would be to go back further into the code and check if two functions share the same id

  def Add(self, name, member=None):
    if member and member in self.members:
      dupe = self.members.index(member)
      self.names[dupe] += ', ' + name
      return
    self.names.append(name)
    self.members.append(member)
'''
'''
Make this substitution on line 458 of core.py to allow other iterables to be accessed by index

    # is_sequence = isinstance(component, (list, tuple))
    is_sequence = hasattr(component, '__getitem__') and not hasattr(component, 'values')
'''
'''
And make a corresponding change in generating the help message

  is_sequence = hasattr(component, '__getitem__') and not hasattr(component, values)
  # if isinstance(component, (list, tuple)) and component:
  if is_sequence and component:
'''
