import logging
tIBiG=None
tIBix=str
tIBiH=int
tIBib=open
tIBiV=bool
tIBie=False
tIBif=classmethod
import os
from localstack.config import TMP_FOLDER
from localstack_ext.bootstrap.cpvcs.constants import(CPVCS_DIR,DEFAULT_POD_DIR,DELTA_LOG_DIR,HEAD_FILE,KNOWN_VER_FILE,MAX_VER_FILE,OBJ_STORE_DIR,REFS_DIR,REV_SUB_DIR,VER_LOG_FILE,VER_LOG_STRUCTURE,VER_SUB_DIR)
LOG=logging.getLogger(__name__)
class PodConfigContext:
 default_instance=tIBiG
 def __init__(self,pod_root_dir:tIBix):
  self.cpvcs_root_dir=pod_root_dir
  self.pod_root_dir=pod_root_dir
 def get_cpvcs_root_dir(self)->tIBix:
  return self.pod_root_dir
 def get_head_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,HEAD_FILE)
 def get_max_ver_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,MAX_VER_FILE)
 def get_known_ver_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,KNOWN_VER_FILE)
 def get_ver_log_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,VER_LOG_FILE)
 def get_obj_store_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,OBJ_STORE_DIR)
 def get_rev_obj_store_path(self)->tIBix:
  return os.path.join(self.get_obj_store_path(),REV_SUB_DIR)
 def get_ver_obj_store_path(self)->tIBix:
  return os.path.join(self.get_obj_store_path(),VER_SUB_DIR)
 def get_ver_refs_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,REFS_DIR,VER_SUB_DIR)
 def get_rev_refs_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,REFS_DIR,REV_SUB_DIR)
 def get_delta_log_path(self)->tIBix:
  return os.path.join(self.pod_root_dir,self.get_obj_store_path(),DELTA_LOG_DIR)
 def update_ver_log(self,author:tIBix,ver_no:tIBiH,rev_id:tIBix,rev_no:tIBiH):
  with tIBib(self.get_ver_log_path(),"a")as fp:
   fp.write(f"{VER_LOG_STRUCTURE.format(author=author, ver_no=ver_no, rev_rid_no=f'{rev_id}_{rev_no}')}\n")
 def create_version_symlink(self,name:tIBix,key:tIBix)->tIBix:
  return self._create_symlink(name,key,self.get_ver_refs_path())
 def create_revision_symlink(self,name:tIBix,key:tIBix)->tIBix:
  return self._create_symlink(name,key,self.get_rev_refs_path())
 def is_initialized(self)->tIBiV:
  return self.pod_root_dir and os.path.isdir(self.pod_root_dir)
 def _create_symlink(self,name:tIBix,key:tIBix,path:tIBix)->tIBix:
  symlink=os.path.join(path,name)
  with tIBib(symlink,"w")as fp:
   fp.write(key)
  return symlink
 def _get_head_key(self)->tIBix:
  return self._get_key(self.get_head_path())
 def get_max_ver_key(self)->tIBix:
  return self._get_key(self.get_max_ver_path())
 def _get_key(self,path:tIBix)->tIBix:
  with tIBib(path,"r")as fp:
   key_path=fp.readline()
  with tIBib(key_path,"r")as fp:
   key=fp.readline()
   return key
 def get_obj_file_path(self,key:tIBix)->tIBix:
  return os.path.join(self.get_obj_store_path(),key)
 def is_remotly_managed(self)->tIBiV:
  return tIBie
 def set_pod_context(self,pod_name:tIBix):
  self.pod_root_dir=os.path.join(self.cpvcs_root_dir,pod_name)
 def pod_exists_locally(self,pod_name:tIBix)->tIBiV:
  return os.path.isdir(os.path.join(self.cpvcs_root_dir,pod_name))
 @tIBif
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
