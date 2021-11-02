# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 11:15:56 2021

@author: mumuz
"""

from simuwater.simuwater import PySimuwaterException

class SwmmNodes(object):
    
    def __init__(self, sim, inp_id):
        if not sim._isStarted:
            raise PySimuwaterException('SWMM Model Within Simuwater Not Open')
        self._sim = sim
        self._inp_id = inp_id
        self._model = sim._model
        self._cur_index = 0
        self._nNodes = self._model.simuwater_getSwmmObjCount(self._inp_id, 1)
    
    def __len__(self):
        return self._model.simuwater_getSwmmObjCount(self._inp_id, 1)
    
    def __contains__(self, node_id):
        if self._model.simuwater_getSwmmObjIndex(self._inp_id, 1,node_id) < 0:
            return False
        return True
    
    def __getitem__(self, node_id):
        if self.__contains__(node_id):
            return SwmmNode(self._sim, self._inp_id, node_id)
        else:
            raise PySimuwaterException('Node ID: {} Does not Exists'.format(node_id))
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._cur_index < self._nNodes:
            node_obj = self.__getitem__(self._node_id)
            self._cur_index += 1
            return node_obj
        else:
            raise StopIteration()
    
    next = __next__  # Python 2
    
    @property
    def _node_id(self):
        return self._model.simuwater_getSwmmObjID(self._inp_id, 1, self._cur_index)[1]
        
class SwmmNode(object):
    
    def __init__(self, sim, inp_id, node_id):
        if not sim._isStarted:
            raise PySimuwaterException('SWMM Model Within Simuwater Not Open')
        if sim._model.simuwater_getSwmmObjIndex(inp_id, 1, node_id) < 0:
            raise PySimuwaterException('ID Invalid')
        self._sim = sim
        self._model = sim._model
        self._inp_id = inp_id
        self._node_id = node_id
        
    @property
    def node_id(self): 
        return self._node_id
    
    @property
    def depth(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 1, self._node_id, 0)[1]
    
    @property
    def head(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 1, self._node_id, 1)[1]
    
    @property
    def volume(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 1, self._node_id, 2)[1]
    
    @property
    def lateral_inflow(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 1, self._node_id, 3)[1]
    
    @property
    def total_inflow(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 1, self._node_id, 4)[1]
   
    @property
    def overflow(self):
        return self._model.simuwater_getSwmmResult(self._inp_id, 1, self._node_id, 5)[1]
    
    def set_external_inflow(self, ext_inflow):
        return self._model.simuwater_setSwmmExtInflow(self._inp_id, self._node_id, ext_inflow)