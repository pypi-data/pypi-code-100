from enum import IntEnum

from pzwin.Constants import *

class WinEvent:
    _type:WinEventType
    _subType:int
    _params:dict
    def __init__(self, weType:WinEventType, subType:int, params:dict):
        self._type = weType
        self._subType = subType
        self._params = params
    @property
    def type(self)->WinEventType:
        return self._type
    @type.setter
    def type(self, weType:WinEventType):
        self._type = weType        

    @property
    def subType(self)->int:
        return self._subType
    @subType.setter
    def subType(self, subType:int):
        self._subType = subType     

    @property
    def params(self)->dict:
        return self._params
    @params.setter
    def params(self, paramDict:dict):
        self._params = paramDict     
