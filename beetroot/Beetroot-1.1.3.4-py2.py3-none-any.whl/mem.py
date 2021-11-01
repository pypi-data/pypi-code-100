try:
    from psutil import virtual_memory, swap_memory
    
except:
    pass

from .exception import *
from .objtype import *

class m:
    """Memory shtuff"""
    def mem(self):
        """Returns total, used and available memory."""
        try:
            yee = virtual_memory()
            return [yee.total, yee.used, yee.free]
        
        except NameError:
            raise ModuleError("psutil must be installed to use beetroot.mem.mem(). Use pip install psutil or pip install beetroot[ram].")
        
    def swapmem(self):
        """Returns total, used and available swap memory."""
        try:
            yee = swap_memory()
            return [yee.total, yee.used, yee.free]
        
        except NameError:
            raise ModuleError("psutil must be installed to use beetroot.mem.swapmem(). Use pip install psutil or pip install beetroot[ram].")
mem = m()
del m