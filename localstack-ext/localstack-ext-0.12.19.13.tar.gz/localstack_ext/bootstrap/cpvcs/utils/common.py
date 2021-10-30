import logging
QqHBE=None
QqHBt=str
QqHBs=int
QqHBr=open
QqHBb=bool
QqHBO=False
QqHBh=classmethod
import os
from localstack.config import TMP_FOLDER
from localstack_ext.bootstrap.cpvcs.constants import(CPVCS_DIR,DEFAULT_POD_DIR,DELTA_LOG_DIR,HEAD_FILE,KNOWN_VER_FILE,MAX_VER_FILE,OBJ_STORE_DIR,REFS_DIR,REV_SUB_DIR,VER_LOG_FILE,VER_LOG_STRUCTURE,VER_SUB_DIR)
LOG=logging.getLogger(__name__)
class PodConfigContext:
 default_instance=QqHBE
 def __init__(self,pod_root_dir:QqHBt):
  self.cpvcs_root_dir=pod_root_dir
  self.pod_root_dir=pod_root_dir
 def get_cpvcs_root_dir(self)->QqHBt:
  return self.pod_root_dir
 def get_head_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,HEAD_FILE)
 def get_max_ver_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,MAX_VER_FILE)
 def get_known_ver_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,KNOWN_VER_FILE)
 def get_ver_log_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,VER_LOG_FILE)
 def get_obj_store_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,OBJ_STORE_DIR)
 def get_rev_obj_store_path(self)->QqHBt:
  return os.path.join(self.get_obj_store_path(),REV_SUB_DIR)
 def get_ver_obj_store_path(self)->QqHBt:
  return os.path.join(self.get_obj_store_path(),VER_SUB_DIR)
 def get_ver_refs_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,REFS_DIR,VER_SUB_DIR)
 def get_rev_refs_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,REFS_DIR,REV_SUB_DIR)
 def get_delta_log_path(self)->QqHBt:
  return os.path.join(self.pod_root_dir,self.get_obj_store_path(),DELTA_LOG_DIR)
 def update_ver_log(self,author:QqHBt,ver_no:QqHBs,rev_id:QqHBt,rev_no:QqHBs):
  with QqHBr(self.get_ver_log_path(),"a")as fp:
   fp.write(f"{VER_LOG_STRUCTURE.format(author=author, ver_no=ver_no, rev_rid_no=f'{rev_id}_{rev_no}')}\n")
 def create_version_symlink(self,name:QqHBt,key:QqHBt)->QqHBt:
  return self._create_symlink(name,key,self.get_ver_refs_path())
 def create_revision_symlink(self,name:QqHBt,key:QqHBt)->QqHBt:
  return self._create_symlink(name,key,self.get_rev_refs_path())
 def is_initialized(self)->QqHBb:
  return self.pod_root_dir and os.path.isdir(self.pod_root_dir)
 def _create_symlink(self,name:QqHBt,key:QqHBt,path:QqHBt)->QqHBt:
  symlink=os.path.join(path,name)
  with QqHBr(symlink,"w")as fp:
   fp.write(key)
  return symlink
 def _get_head_key(self)->QqHBt:
  return self._get_key(self.get_head_path())
 def get_max_ver_key(self)->QqHBt:
  return self._get_key(self.get_max_ver_path())
 def _get_key(self,path:QqHBt)->QqHBt:
  with QqHBr(path,"r")as fp:
   key_path=fp.readline()
  with QqHBr(key_path,"r")as fp:
   key=fp.readline()
   return key
 def get_obj_file_path(self,key:QqHBt)->QqHBt:
  return os.path.join(self.get_obj_store_path(),key)
 def is_remotly_managed(self)->QqHBb:
  return QqHBO
 def set_pod_context(self,pod_name:QqHBt):
  self.pod_root_dir=os.path.join(self.cpvcs_root_dir,pod_name)
 def pod_exists_locally(self,pod_name:QqHBt)->QqHBb:
  return os.path.isdir(os.path.join(self.cpvcs_root_dir,pod_name))
 @QqHBh
 def get(cls):
  if not cls.default_instance:
   pod_root_dir=os.environ.get("POD_DIR")
   if not pod_root_dir:
    pod_root_dir=os.path.join(TMP_FOLDER,DEFAULT_POD_DIR)
   pod_root_dir=os.path.join(pod_root_dir,CPVCS_DIR)
   cls.default_instance=PodConfigContext(pod_root_dir)
  return cls.default_instance
config_context=PodConfigContext.get()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
