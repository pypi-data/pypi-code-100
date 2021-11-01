try:
    import upsidedown  
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    from zalgo_text import zalgo as zalg
    
except (ModuleNotFoundError, ImportError):
    pass

import random

from .exception import *

gen = random.SystemRandom()



class teg:
    def __init__(self):
        try:
            self.zal = zalg.zalgo()
            
        except NameError:
            pass
        
    def udown(self, intext):
        """Generates upside-down text"""
        try:
            return upsidedown.transform(str(intext))
        
        except NameError:
            raise ModuleError("Upsidedown must be installed. Try pip install upsidedown or pip install beetroot[text].")
        
    def zalgo(self, intext, **kwargs):
        """Generates Zalgo text"""
        craziness = int(
            round(
                kwargs.get(
                    "crazy",
                    10
                )
            )
        )
        try:
            self.zal.numAccentsUp = (craziness, craziness * 10)
            self.zal.numAccentsDown = (craziness, craziness * 10)
            self.zal.numAccentsMiddle = (craziness, craziness * 10)
            self.zal.maxAccentsPerLetter = craziness * 40
            return self.zal.zalgofy(str(intext))
        
        except NameError:
            raise ModuleError("Zalgo_text must be installed. Try pip install zalgo-text or pip install beetroot[text].")
        
text = teg()
del teg