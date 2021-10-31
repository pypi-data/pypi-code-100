
from typing import Callable

class Listen:
    callback: Callable
    name: str

    def __new__(cls, name: str, **kwargs):
        def wrap(callback: Callable):
            inst = super(Listen, cls).__new__(cls)
            inst.callback = callback
            inst.name = name
            if inst.__init__: inst.__init__(**kwargs)
            return inst
        return wrap
    
    def __call__(self, bound, *args, **kwargs):
        return self.callback(bound, *args, **kwargs)
    
class Listener:
    toListen: dict[str, Listen]

    def __init__(self):
        self.toListen = {}

        for attrName in dir(self):
            attr = self.__getattribute__(attrName)
            if isinstance(attr, Listen):
                self.toListen[attr.name] = attr
    
    async def trigger(self, event: str, *args, **kwargs):
        if not event in self.toListen: return
        
        listen = self.toListen[event]
        await listen(self, *args, **kwargs)