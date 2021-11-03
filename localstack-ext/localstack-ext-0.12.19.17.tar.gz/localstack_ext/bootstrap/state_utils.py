import logging
zcinS=bool
zcinA=hasattr
zcink=set
zcint=True
zcinK=False
zcinu=isinstance
zcino=dict
zcinD=getattr
zcinO=None
zcinh=str
zcinE=Exception
zcinM=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[zcinS,Set]:
 if zcinA(obj,"__dict__"):
  visited=visited or zcink()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return zcint,visited
  visited.add(wrapper)
 return zcinK,visited
def get_object_dict(obj):
 if zcinu(obj,zcino):
  return obj
 obj_dict=zcinD(obj,"__dict__",zcinO)
 return obj_dict
def is_composite_type(obj):
 return zcinu(obj,(zcino,OrderedDict))or zcinA(obj,"__dict__")
def api_states_traverse(api_states_path:zcinh,side_effect:Callable[...,zcinO],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except zcinE as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with zcinM(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except zcinE as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with zcinM(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
