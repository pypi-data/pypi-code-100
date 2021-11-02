# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:33:04 2021

@author: mumuz
"""


from simuwater.simuwater import PySimuwaterException

class SwmmLinks(object):
    
    def __init__(self, sim, inp_id):
        if not sim._isStarted:
            raise PySimuwaterException('SWMM Model Within Simuwater Not Open')
        self._sim = sim
        self._inp_id = inp_id
        self._model = sim._model
        self._cur_index = 0
        self._nLinks = self._model.simuwater_getSwmmObjCount(self._inp_id, 2)
    
    def __len__(self):
        return self._model.simuwater_getSwmmObjCount(self._inp_id, 2)
    
    def __contains__(self, link_id):
        if self._model.simuwater_getSwmmObjIndex(self._inp_id, 2,link_id) < 0:
            return False
        return True
    
    def __getitem__(self, link_id):
        if self.__contains__(link_id):
            return SwmmLink(self._sim, self._inp_id, link_id)
        else:
            raise PySimuwaterException('Link ID: {} Does not Exists'.format(link_id))
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur_index < self._nLinks:
            link_obj = self.__getitem__(self._link_id)
            self._cur_index += 1
            return link_obj
        else:
            raise StopIteration()
    
    next = __next__  # Python 2
    
    @property
    def _link_id(self):
        return self._model.simuwater_getSwmmObjID(self._inp_id, 2, self._cur_index)[1]
        
class SwmmLink(object):
    
    def __init__(self, sim, inp_id, link_id):
        if not sim._isStarted:
            raise PySimuwaterException('SWMM Model Within Simuwater Not Open')
        if sim._model.simuwater_getSwmmObjIndex(inp_id, 2, link_id) < 0:
            raise PySimuwaterException('ID Invalid')
        self._sim = sim
        self._model = sim._model
        self._inp_id = inp_id
        self._link_id = link_id
        
    @property
    def link_id(self): 
        return self._link_id
    
    @property
    def flow(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 2, self._link_id, 0)[1]
    
    @property
    def depth(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 2, self._link_id, 1)[1]
    
    @property
    def velocity(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 2, self._link_id, 2)[1]
    
    @property
    def volume(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 2, self._link_id, 3)[1]
    
    @property
    def capacity(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 2, self._link_id, 4)[1]
    
    def set_setting(self,setting):
        return self._model.simuwater_setSwmmSetting(self._inp_id, self._link_id, setting)