
from importlib.abc import Loader, MetaPathFinder
import sys 
import logging 

logger = logging.getLogger("pyhdls")

class PyhdLoader(Loader):
    """ loads a module. 
    """
    def __init__(self):
        pass 
    
    def create_module(self, spec):
        pass
    
    def exec_module(self, module):
        pass 


class PyhdFinder(MetaPathFinder):
    """ find a loader to load module 
    """ 
    def _find_self(self):
        pass
    def find_spec(self, fullname, path, target=None):
        return None