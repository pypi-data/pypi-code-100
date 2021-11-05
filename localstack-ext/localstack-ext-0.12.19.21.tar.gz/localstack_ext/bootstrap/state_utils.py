import logging
LeJpE=bool
LeJpS=hasattr
LeJpd=set
LeJpb=True
LeJpj=False
LeJpz=isinstance
LeJpg=dict
LeJpx=getattr
LeJpr=None
LeJpa=str
LeJpo=Exception
LeJpV=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[LeJpE,Set]:
 if LeJpS(obj,"__dict__"):
  visited=visited or LeJpd()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return LeJpb,visited
  visited.add(wrapper)
 return LeJpj,visited
def get_object_dict(obj):
 if LeJpz(obj,LeJpg):
  return obj
 obj_dict=LeJpx(obj,"__dict__",LeJpr)
 return obj_dict
def is_composite_type(obj):
 return LeJpz(obj,(LeJpg,OrderedDict))or LeJpS(obj,"__dict__")
def api_states_traverse(api_states_path:LeJpa,side_effect:Callable[...,LeJpr],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except LeJpo as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with LeJpV(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except LeJpo as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with LeJpV(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
