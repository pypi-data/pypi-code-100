import logging
kdyrp=bool
kdyrB=hasattr
kdyrC=set
kdyrS=True
kdyro=False
kdyrF=isinstance
kdyrD=dict
kdyrK=getattr
kdyrn=None
kdyrV=str
kdyrQ=Exception
kdyrW=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[kdyrp,Set]:
 if kdyrB(obj,"__dict__"):
  visited=visited or kdyrC()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return kdyrS,visited
  visited.add(wrapper)
 return kdyro,visited
def get_object_dict(obj):
 if kdyrF(obj,kdyrD):
  return obj
 obj_dict=kdyrK(obj,"__dict__",kdyrn)
 return obj_dict
def is_composite_type(obj):
 return kdyrF(obj,(kdyrD,OrderedDict))or kdyrB(obj,"__dict__")
def api_states_traverse(api_states_path:kdyrV,side_effect:Callable[...,kdyrn],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except kdyrQ as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with kdyrW(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except kdyrQ as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
