import logging
yGJcI=bool
yGJck=hasattr
yGJcY=set
yGJcV=True
yGJcR=False
yGJcK=isinstance
yGJcs=dict
yGJcj=getattr
yGJcC=None
yGJcQ=str
yGJcv=Exception
yGJcP=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
from localstack.utils.common import ObjectIdHashComparator
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[yGJcI,Set]:
 if yGJck(obj,"__dict__"):
  visited=visited or yGJcY()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return yGJcV,visited
  visited.add(wrapper)
 return yGJcR,visited
def get_object_dict(obj):
 if yGJcK(obj,yGJcs):
  return obj
 obj_dict=yGJcj(obj,"__dict__",yGJcC)
 return obj_dict
def is_composite_type(obj):
 return yGJcK(obj,(yGJcs,OrderedDict))or yGJck(obj,"__dict__")
def api_states_traverse(api_states_path:yGJcQ,side_effect:Callable[...,yGJcC],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except yGJcv as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with yGJcP(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except yGJcv as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
