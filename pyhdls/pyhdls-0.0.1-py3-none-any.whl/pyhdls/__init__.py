import logging 

logger = logging.getLogger('pyhd')
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s (%(filename)s:%(lineno)d) %(message)s ",'%Y/%m/%d %H:%M:%S'))
logger.addHandler(ch)



import sys
print(sys.meta_path)
print(sys.path_hooks)
print(sys.meta_path[0].find_spec("sys"))

from . import import_hook

sys.meta_path.insert(0,import_hook.PyhdFinder)

from .hd import hardware

print(type(sys))
print(__package__)

