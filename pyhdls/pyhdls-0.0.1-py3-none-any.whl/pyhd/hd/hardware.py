import math
from . import utils

class UInt:
    def __init__(self,value = None):

        self.value:int = value 
        self.width:int = None 

        if value == None:
            pass 
        elif type(value) is int and value >= 0:
            self.width = utils.width_infer(self.value)
        elif type(value) is str:
            self.value = utils.str2int(value)
            self.width = utils.width_infer(self.value)
        else:
            raise Exception(f"UInt cannot take the value of {value}")

    def W(self, width:int): 
        if self.width > width:
            print("warning: cut width")
        self.width = width 
        return self
            
    def __str__(self):
        return f"UInt<{self.width}>({self.value})"


class Module:
    def __init__(self):
        pass

import sys
print(sys.meta_path)