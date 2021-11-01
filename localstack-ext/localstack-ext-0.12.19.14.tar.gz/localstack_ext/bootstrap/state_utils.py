import logging
WCDXJ=bool
WCDXa=hasattr
WCDXv=set
WCDXq=True
WCDXd=False
WCDXK=isinstance
WCDXR=dict
WCDXg=getattr
WCDXO=None
WCDXY=str
WCDXV=Exception
WCDXx=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[WCDXJ,Set]:
 if WCDXa(obj,"__dict__"):
  visited=visited or WCDXv()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return WCDXq,visited
  visited.add(wrapper)
 return WCDXd,visited
def get_object_dict(obj):
 if WCDXK(obj,WCDXR):
  return obj
 obj_dict=WCDXg(obj,"__dict__",WCDXO)
 return obj_dict
def is_composite_type(obj):
 return WCDXK(obj,(WCDXR,OrderedDict))or WCDXa(obj,"__dict__")
def api_states_traverse(api_states_path:WCDXY,side_effect:Callable[...,WCDXO],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except WCDXV as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with WCDXx(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except WCDXV as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
