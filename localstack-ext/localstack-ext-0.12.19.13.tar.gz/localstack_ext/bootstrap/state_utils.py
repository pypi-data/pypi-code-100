import logging
cEJjx=bool
cEJjR=hasattr
cEJjQ=set
cEJjd=True
cEJjt=False
cEJja=isinstance
cEJjo=dict
cEJjX=getattr
cEJjr=None
cEJju=str
cEJjp=Exception
cEJjV=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[cEJjx,Set]:
 if cEJjR(obj,"__dict__"):
  visited=visited or cEJjQ()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return cEJjd,visited
  visited.add(wrapper)
 return cEJjt,visited
def get_object_dict(obj):
 if cEJja(obj,cEJjo):
  return obj
 obj_dict=cEJjX(obj,"__dict__",cEJjr)
 return obj_dict
def is_composite_type(obj):
 return cEJja(obj,(cEJjo,OrderedDict))or cEJjR(obj,"__dict__")
def api_states_traverse(api_states_path:cEJju,side_effect:Callable[...,cEJjr],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except cEJjp as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with cEJjV(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except cEJjp as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
