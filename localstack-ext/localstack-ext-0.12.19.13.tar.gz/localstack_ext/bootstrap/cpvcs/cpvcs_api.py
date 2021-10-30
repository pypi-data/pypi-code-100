import inspect
vIWcb=None
vIWcH=set
vIWcQ=open
vIWci=str
vIWcn=filter
vIWcj=int
vIWcm=list
vIWcd=map
vIWcz=False
vIWcy=Exception
vIWcV=bool
vIWcM=True
vIWca=next
vIWcC=sorted
vIWcs=isinstance
vIWcL=dict
vIWcS=getattr
vIWcN=type
import json
import logging
import os
import shutil
import zipfile
from typing import Dict,List,Optional,Set,Tuple
from deepdiff import DeepDiff
from localstack.utils.common import mkdir,rm_rf,short_uid
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_FILE,COMPRESSION_FORMAT,META_ZIP,NIL_PTR,VER_SYMLINK)
from localstack_ext.bootstrap.cpvcs.models import Commit,Revision,StateFileRef,Version
from localstack_ext.bootstrap.cpvcs.obj_storage import default_storage as object_storage
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
from localstack_ext.bootstrap.cpvcs.utils.hash_utils import(compute_file_hash,compute_node_hash,random_hash)
from localstack_ext.bootstrap.state_utils import load_persisted_object
from localstack_ext.constants import API_STATES_DIR
from localstack_ext.utils.persistence import persist_object
from localstack_ext.utils.state_merge import merge_object_state
LOG=logging.getLogger(__name__)
def init(creator:vIWci="Unknown",pod_name="My-Pod"):
 if config_context.pod_exists_locally(pod_name=pod_name):
  LOG.warning(f"Pod with name {pod_name} already exists locally")
  return
 config_context.set_pod_context(pod_name)
 def _create_internal_fs():
  mkdir(config_context.get_cpvcs_root_dir())
  mkdir(config_context.get_ver_refs_path())
  mkdir(config_context.get_rev_refs_path())
  mkdir(config_context.get_ver_obj_store_path())
  mkdir(config_context.get_rev_obj_store_path())
  mkdir(config_context.get_delta_log_path())
 _create_internal_fs()
 r0_hash=random_hash()
 v0_hash=random_hash()
 r0=Revision(hash_ref=r0_hash,parent_ptr=NIL_PTR,creator=creator,rid=short_uid(),revision_number=0,state_files={})
 v0=Version(hash_ref=v0_hash,parent_ptr=NIL_PTR,creator=creator,comment="Init version",active_revision_ptr=r0_hash,outgoing_revision_ptrs={r0_hash},incoming_revision_ptr=vIWcb,state_files=vIWcH(),version_number=0)
 rev_key,ver_key=object_storage.upsert_objects(r0,v0)
 ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=v0.version_number),ver_key)
 with vIWcQ(config_context.get_head_path(),"w")as fp:
  fp.write(ver_symlink)
 with vIWcQ(config_context.get_max_ver_path(),"w")as fp:
  fp.write(ver_symlink)
 with vIWcQ(config_context.get_known_ver_path(),"w")as fp:
  fp.write(ver_symlink)
 config_context.update_ver_log(author=creator,ver_no=v0.version_number,rev_id=r0.rid,rev_no=r0.revision_number)
 LOG.debug(f"Successfully initated CPVCS for pod at {config_context.get_cpvcs_root_dir()}")
def set_pod(pod_name:vIWci):
 config_context.set_pod_context(pod_name)
def create_state_file_from_fs(path:vIWci,file_name:vIWci,service:vIWci,region:vIWci)->vIWci:
 file_path=os.path.join(path,file_name)
 key=compute_file_hash(file_path)
 rel_path=path.split(f"{API_STATES_DIR}/")[1]
 shutil.copy(file_path,os.path.join(config_context.get_obj_store_path(),key))
 state_file=StateFileRef(hash_ref=key,rel_path=rel_path,file_name=file_name,size=os.path.getsize(file_path),service=service,region=region)
 _add_state_file_to_expansion_point(state_file)
 return key
def _create_state_file_from_in_memory_blob(blob)->vIWci:
 tmp_file_name=random_hash()
 tmp_dest=os.path.join(config_context.get_obj_store_path(),tmp_file_name)
 persist_object(blob,tmp_dest)
 key=compute_file_hash(tmp_dest)
 dest=os.path.join(config_context.get_obj_store_path(),key)
 os.rename(tmp_dest,dest)
 return key
def _get_state_file_path(key:vIWci)->vIWci:
 file_path=os.path.join(config_context.get_obj_store_path(),key)
 if os.path.isfile(file_path):
  return file_path
 LOG.warning(f"No state file with found with key: {key}")
def _add_state_file_to_expansion_point(state_file:StateFileRef):
 revision,_=_get_expansion_point_with_head()
 updated_state_files=vIWcH(vIWcn(lambda sf:not sf.congruent(state_file),revision.state_files))
 updated_state_files.add(state_file)
 revision.state_files=updated_state_files
 object_storage.upsert_objects(revision)
def list_state_files(key:vIWci)->Optional[vIWci]:
 cpvcs_obj=object_storage.get_revision_or_version_by_key(key)
 if cpvcs_obj:
  return cpvcs_obj.state_files_info()
 LOG.debug(f"No Version or Revision associated to {key}")
def get_version_info(version_no:vIWcj)->List[vIWci]:
 version_node=get_version_by_number(version_no)
 if not version_node:
  return[]
 return vIWcm(vIWcd(lambda state_file:state_file.metadata(),version_node.state_files))
def commit(message:vIWci=vIWcb)->Revision:
 curr_expansion_point,head_version=_get_expansion_point_with_head()
 curr_expansion_point_hash=compute_node_hash(curr_expansion_point)
 curr_expansion_point_parent_state_files=vIWcH()
 if curr_expansion_point.parent_ptr!=NIL_PTR:
  referenced_by_version=vIWcb
  curr_expansion_point_parent=object_storage.get_revision_by_key(curr_expansion_point.parent_ptr)
  curr_expansion_point_parent_state_files=curr_expansion_point_parent.state_files
  curr_expansion_point_parent.assoc_commit.head_ptr=curr_expansion_point_hash
  object_storage.upsert_objects(curr_expansion_point_parent)
 else:
  referenced_by_version=head_version.hash_ref
 object_storage.update_revision_key(curr_expansion_point.hash_ref,curr_expansion_point_hash,referenced_by_version)
 curr_expansion_point.hash_ref=curr_expansion_point_hash
 new_expansion_point=Revision(hash_ref=random_hash(),state_files={},parent_ptr=curr_expansion_point_hash,creator=curr_expansion_point.creator,rid=short_uid(),revision_number=curr_expansion_point.revision_number+1)
 delta_log_ptr=_create_delta_log(curr_expansion_point_parent_state_files,curr_expansion_point.state_files)
 assoc_commit=Commit(tail_ptr=curr_expansion_point.hash_ref,head_ptr=new_expansion_point.hash_ref,message=message,delta_log_ptr=delta_log_ptr)
 curr_expansion_point.assoc_commit=assoc_commit
 object_storage.upsert_objects(new_expansion_point,curr_expansion_point)
 config_context.update_ver_log(author=new_expansion_point.creator,ver_no=head_version.version_number,rev_id=new_expansion_point.rid,rev_no=new_expansion_point.revision_number)
 return curr_expansion_point
def get_head()->Version:
 return object_storage.get_version_by_key(config_context._get_head_key())
def _get_max_version()->Version:
 return object_storage.get_version_by_key(config_context.get_max_ver_key())
def get_max_version_no()->vIWcj:
 with vIWcQ(config_context.get_max_ver_path())as fp:
  return vIWcj(os.path.basename(fp.readline()))
def _get_expansion_point_with_head()->Tuple[Revision,Version]:
 head_version=get_head()
 active_revision_root=object_storage.get_revision_by_key(head_version.active_revision_ptr)
 expansion_point=object_storage.get_terminal_revision(active_revision_root)
 return expansion_point,head_version
def _filter_special_cases(state_files:Set[StateFileRef])->Tuple[List[StateFileRef],List[StateFileRef],List[StateFileRef]]:
 regular_refs,s3_bucket_refs,sqs_queue_refs=[],[],[]
 for state_file in state_files:
  if state_file.service=="sqs":
   sqs_queue_refs.append(state_file)
  elif state_file.service=="s3":
   s3_bucket_refs.append(state_file)
  else:
   regular_refs.append(state_file)
 return regular_refs,s3_bucket_refs,sqs_queue_refs
def push(comment:vIWci=vIWcb)->Version:
 if config_context.is_remotly_managed():
  _push_remote()
 expansion_point,head_version=_get_expansion_point_with_head()
 max_version=_get_max_version()
 new_active_revision=Revision(hash_ref=random_hash(),state_files=vIWcH(),parent_ptr=NIL_PTR,creator=expansion_point.creator,rid=short_uid(),revision_number=0)
 if head_version.version_number!=max_version.version_number:
  expansion_points=_filter_special_cases(expansion_point.state_files)
  expansion_point_regular_sf=expansion_points[0]
  expansion_point_s3_sf=expansion_points[1]
  expansion_point_sqs_sf=expansion_points[2]
  max_versions=_filter_special_cases(max_version.state_files)
  max_version_regular_sf=max_versions[0]
  max_version_s3_sf=max_versions[1]
  max_version_sqs_sf=max_versions[2]
  new_version_state_files:Set[StateFileRef]=vIWcH()
  expansion_point_file_paths_refs={os.path.join(ep_sf.rel_path,ep_sf.file_name):ep_sf.hash_ref for ep_sf in expansion_point_regular_sf}
  for state_file in max_version_regular_sf:
   service=state_file.service
   region=state_file.region
   rel_path=state_file.rel_path
   file_name=state_file.file_name
   qualifier=os.path.join(rel_path,file_name)
   match=expansion_point_file_paths_refs.pop(qualifier,vIWcb)
   if match:
    max_ver_file_ref=state_file.hash_ref
    if max_ver_file_ref==match:
     continue
    max_ver_state_file=_get_state_file_path(max_ver_file_ref)
    expansion_point_state_file=_get_state_file_path(match)
    max_ver_state=load_persisted_object(max_ver_state_file)
    expansion_point_state=load_persisted_object(expansion_point_state_file)
    merge_object_state(max_ver_state,expansion_point_state)
    merged_key=_create_state_file_from_in_memory_blob(max_ver_state)
    merged_state_file_ref=StateFileRef(hash_ref=merged_key,rel_path=rel_path,file_name=file_name,size=os.path.getsize(_get_state_file_path(merged_key)),service=service,region=region)
    new_version_state_files.add(merged_state_file_ref)
   else:
    new_version_state_files.add(state_file)
  newly_added_file_refs=vIWcH(expansion_point_file_paths_refs.values())
  newly_added_files=vIWcH(vIWcn(lambda leftover:leftover.hash_ref in newly_added_file_refs,expansion_point_regular_sf))
  new_version_state_files.update(newly_added_files)
  for sqs_sf in max_version_sqs_sf:
   if not sqs_sf.any_congruence(expansion_point_sqs_sf):
    new_version_state_files.add(sqs_sf)
  for s3_sf in max_version_s3_sf:
   if not s3_sf.any_congruence(expansion_point_s3_sf):
    new_version_state_files.add(s3_sf)
  new_version_state_files.update(expansion_point_s3_sf)
  new_version_state_files.update(expansion_point_sqs_sf)
 else:
  new_version_state_files=expansion_point.state_files
 new_version=Version(hash_ref=vIWcb,state_files=new_version_state_files,parent_ptr=max_version.hash_ref,creator=expansion_point.creator,comment=comment,active_revision_ptr=new_active_revision.hash_ref,outgoing_revision_ptrs={new_active_revision.hash_ref},incoming_revision_ptr=expansion_point.hash_ref,version_number=max_version.version_number+1)
 if expansion_point.parent_ptr!=NIL_PTR:
  expansion_point_parent=object_storage.get_revision_by_key(expansion_point.parent_ptr)
  state_from=expansion_point_parent.state_files
 else:
  state_from=vIWcH()
 delta_log_ptr=_create_delta_log(state_from,new_version.state_files)
 expansion_point_commit=Commit(tail_ptr=expansion_point.hash_ref,head_ptr=new_version.hash_ref,message="Finalizing commit",delta_log_ptr=delta_log_ptr)
 expansion_point.state_files=new_version.state_files
 expansion_point.assoc_commit=expansion_point_commit
 new_version_hash=compute_node_hash(new_version)
 new_version.hash_ref=new_version_hash
 head_version.active_revision_ptr=NIL_PTR
 object_storage.upsert_objects(head_version,expansion_point,new_active_revision,new_version)
 _update_head(new_version.version_number,new_version.hash_ref)
 _update_max_ver(new_version.version_number,new_version.hash_ref)
 _add_known_ver(new_version.version_number,new_version.hash_ref)
 _create_state_zip(new_version.version_number,new_version.state_files)
 _create_commit_history(new_version)
 config_context.update_ver_log(author=expansion_point.creator,ver_no=new_version.version_number,rev_id=new_active_revision.rid,rev_no=new_active_revision.revision_number)
 return new_version
def get_version_state_pod(version_no:vIWcj):
 version_path=os.path.join(config_context.get_cpvcs_root_dir(),f"version_{version_no}.zip")
 if os.path.isfile(version_path):
  return version_path
def _create_commit_history(version_node:Version,delete_reference:vIWcV=vIWcz):
 revision_node=object_storage.get_revision_or_version_by_key(version_node.incoming_revision_ptr)
 history_dir=os.path.join(config_context.get_cpvcs_root_dir(),META_ZIP.format(version_no=version_node.version_number))
 mkdir(history_dir)
 while revision_node:
  delta_ptr=revision_node.assoc_commit.delta_log_ptr
  if delta_ptr:
   src=object_storage.get_delta_file_by_key(delta_ptr)
   if not src:
    continue
   dst_name=COMMIT_FILE.format(commit_no=revision_node.revision_number+1)
   dst=os.path.join(config_context.get_cpvcs_root_dir(),history_dir,dst_name)
   shutil.copy(src,dst)
   if delete_reference:
    os.remove(src)
  revision_node=object_storage.get_revision_by_key(revision_node.parent_ptr)
 shutil.make_archive(history_dir,COMPRESSION_FORMAT,root_dir=history_dir)
 rm_rf(history_dir)
def _create_state_zip(version_number:vIWcj,state_file_refs:Set[StateFileRef],delete_files=vIWcz):
 version_dir=os.path.join(config_context.get_cpvcs_root_dir(),f"version_{version_number}")
 for state_file in state_file_refs:
  try:
   dst_path=os.path.join(version_dir,API_STATES_DIR,state_file.rel_path)
   mkdir(dst_path)
   src=object_storage.get_state_file_location_by_key(state_file.hash_ref)
   dst=os.path.join(dst_path,state_file.file_name)
   shutil.copy(src,dst)
   if delete_files:
    os.remove(src)
  except vIWcy as e:
   LOG.warning(f"Failed to locate state file with rel path: {state_file.rel_path}: {e}")
 mkdir(os.path.join(version_dir,"kinesis"))
 mkdir(os.path.join(version_dir,"dynamodb"))
 shutil.make_archive(version_dir,"zip",root_dir=version_dir)
 rm_rf(version_dir)
def set_active_version(version_no:vIWcj,commit_before=vIWcz)->vIWcV:
 known_versions=load_version_references()
 for known_version_no,known_version_key in known_versions:
  if known_version_no==version_no:
   if commit_before:
    commit()
   _set_active_version(known_version_key)
   return vIWcM
 LOG.info(f"Version with number {version_no} not found")
 return vIWcz
def _set_active_version(key:vIWci):
 current_head=get_head()
 if current_head.hash_ref!=key and object_storage.version_exists(key):
  requested_version=object_storage.get_version_by_key(key)
  _update_head(requested_version.version_number,key)
  if requested_version.active_revision_ptr==NIL_PTR:
   new_path_root=Revision(hash_ref=random_hash(),state_files=vIWcH(),parent_ptr=NIL_PTR,creator="Unknown",rid=short_uid(),revision_number=0)
   requested_version.active_revision_ptr=new_path_root.hash_ref
   requested_version.outgoing_revision_ptrs.add(new_path_root.hash_ref)
   object_storage.upsert_objects(new_path_root,requested_version)
def get_version_by_number(version_no:vIWcj)->Version:
 versions=load_version_references()
 version_ref=vIWca((version[1]for version in versions if version[0]==version_no),vIWcb)
 if not version_ref:
  LOG.warning(f"Could not find version number {version_no}")
  return
 return object_storage.get_version_by_key(version_ref)
def load_version_references()->List[Tuple[vIWcj,vIWci]]:
 result={}
 with vIWcQ(config_context.get_known_ver_path(),"r")as vp:
  symlinks=vp.readlines()
  for symlink in symlinks:
   symlink=symlink.rstrip()
   with vIWcQ(symlink,"r")as sp:
    result[vIWcj(os.path.basename(symlink))]=sp.readline()
 return vIWcC(result.items(),key=lambda x:x[0],reverse=vIWcM)
def list_versions()->List[vIWci]:
 version_references=load_version_references()
 result=[object_storage.get_version_by_key(version_key).info_str()for _,version_key in version_references]
 return result
def list_version_commits(version_no:vIWcj)->List[vIWci]:
 if version_no==-1:
  version=_get_max_version()
 else:
  version=get_version_by_number(version_no)
 if not version:
  return[]
 result=[]
 revision=object_storage.get_revision_by_key(version.incoming_revision_ptr)
 while revision:
  assoc_commit=revision.assoc_commit
  revision_no=revision.revision_number
  if revision_no!=0:
   from_node=f"Revision-{revision_no - 1}"
  elif version_no!=0:
   from_node=f"Version-{version_no}"
  else:
   from_node="Empty state"
  to_node=f"Revision-{revision_no}"
  result.append(assoc_commit.info_str(from_node=from_node,to_node=to_node))
  revision=object_storage.get_revision_by_key(revision.parent_ptr)
 return result
def get_commit_diff(version_no:vIWcj,commit_no:vIWcj)->vIWci:
 try:
  _zipfile=zipfile.ZipFile(os.path.join(config_context.get_cpvcs_root_dir(),f"{META_ZIP.format(version_no=version_no)}.{COMPRESSION_FORMAT}"),"r")
  with _zipfile as archive:
   diff=json.loads(archive.read(COMMIT_FILE.format(commit_no=commit_no)))
   return json.dumps(diff)
 except vIWcy as e:
  LOG.debug(f"Commit {commit_no} diff not found for version {version_no}: {e}")
def _update_head(new_head_ver_no,new_head_key)->vIWci:
 with vIWcQ(config_context.get_head_path(),"w")as fp:
  ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=new_head_ver_no),new_head_key)
  fp.write(ver_symlink)
  return ver_symlink
def _update_max_ver(new_max_ver_no,new_max_ver_key)->vIWci:
 with vIWcQ(config_context.get_max_ver_path(),"w")as fp:
  max_ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=new_max_ver_no),new_max_ver_key)
  fp.write(max_ver_symlink)
  return max_ver_symlink
def _add_known_ver(new_ver_no,new_ver_key)->vIWci:
 with vIWcQ(config_context.get_known_ver_path(),"a")as fp:
  new_ver_symlink=config_context.create_version_symlink(VER_SYMLINK.format(ver_no=new_ver_no),new_ver_key)
  fp.write(f"\n{new_ver_symlink}")
  return new_ver_symlink
def _push_remote():
 pass
def _create_delta_log(state_from:Set[StateFileRef],state_to:Set[StateFileRef])->vIWci:
 state_files_from=_filter_special_cases(state_from)
 state_files_from_regular=state_files_from[0]
 state_files_from_s3=state_files_from[1]
 state_files_from_sqs=state_files_from[2]
 state_files_to=_filter_special_cases(state_to)
 state_files_to_regular=state_files_to[0]
 state_files_to_s3=state_files_to[1]
 state_files_to_sqs=state_files_to[2]
 def _create_sf_lookup(state_files:Set[StateFileRef])->Dict[vIWci,StateFileRef]:
  return{os.path.join(sf.rel_path,sf.file_name):sf for sf in state_files}
 result={}
 state_files_to_lookup=_create_sf_lookup(state_files_to_regular)
 def _infer_backend_init(clazz,sf):
  if vIWcs(clazz,vIWcL):
   backend={}
  else:
   constructor=vIWcS(clazz,"__init__",vIWcb)
   sig_args=inspect.getfullargspec(constructor)
   if "region" in sig_args.args:
    backend=clazz(region=sf.region)
   elif "region_name" in sig_args.args:
    backend=clazz(region_name=sf.region)
   else:
    backend=clazz()
  return backend
 for state_file_from in state_files_from_regular:
  result_region=result.setdefault(state_file_from.region,{})
  result_service=result_region.setdefault(state_file_from.service,{})
  result_file=result_service.setdefault(state_file_from.file_name,{})
  if state_file_from.any_congruence(state_files_to_regular):
   key=os.path.join(state_file_from.rel_path,state_file_from.file_name)
   state_file_to=state_files_to_lookup.pop(key)
   diff_json=_create_diff_json(_infer_backend_init,state_file_from,state_file_to)
  else:
   diff_json=_create_diff_json(_infer_backend_init,state_file_from,vIWcb)
  result_file["diff"]=diff_json
 for state_files_to in state_files_to_lookup.values():
  result_region=result.setdefault(state_files_to.region,{})
  result_service=result_region.setdefault(state_files_to.service,{})
  result_file=result_service.setdefault(state_files_to.file_name,{})
  diff_json=_create_diff_json(_infer_backend_init,vIWcb,state_files_to)
  result_file["diff"]=diff_json
 def _handle_special_case_containers(service,sf_from,sf_to):
  region_containers_from={}
  region_containers_to={}
  for container_file_from in sf_from:
   region=container_file_from.region
   region_container=region_containers_from.setdefault(region,{})
   container=load_persisted_object(object_storage.get_state_file_location_by_key(container_file_from.hash_ref))
   if container:
    region_container[container.name]=container
  for container_file_to in sf_to:
   region=container_file_to.region
   region_container=region_containers_to.setdefault(region,{})
   container=load_persisted_object(object_storage.get_state_file_location_by_key(container_file_to.hash_ref))
   if container:
    region_container[container.name]=container
  for region,region_queues_from in region_containers_from.items():
   region_queues_to=region_containers_to.pop(region,{})
   region_diff=DeepDiff(region_queues_from,region_queues_to)
   container_result_region=result.setdefault(region,{})
   container_result_service=container_result_region.setdefault(service,{})
   container_result_service["diff"]=region_diff.to_json()
  for region,region_queues_to in region_containers_to.items():
   region_diff=DeepDiff({},region_queues_to)
   container_result_region=result.setdefault(region,{})
   container_result_service=container_result_region.setdefault(service,{})
   container_result_service["diff"]=region_diff.to_json()
 _handle_special_case_containers("sqs",state_files_from_sqs,state_files_to_sqs)
 _handle_special_case_containers("s3",state_files_from_s3,state_files_to_s3)
 tmp_dest=os.path.join(config_context.get_delta_log_path(),random_hash())
 with vIWcQ(tmp_dest,"w")as fp:
  json.dump(result,fp,indent=4)
 key=compute_file_hash(tmp_dest)
 dest=os.path.join(config_context.get_delta_log_path(),key)
 os.rename(tmp_dest,dest)
 return key
def _create_diff_json(_infer_backend_init,sf1:StateFileRef,sf2:StateFileRef):
 if sf1 and sf2:
  if sf1.hash_ref==sf2.hash_ref:
   return "No Changes"
  else:
   backend1=load_persisted_object(config_context.get_obj_file_path(sf1.hash_ref))
   backend2=load_persisted_object(config_context.get_obj_file_path(sf2.hash_ref))
   diff=DeepDiff(backend1,backend2)
   return diff.to_json()
 if not sf1:
  backend2=load_persisted_object(config_context.get_obj_file_path(sf2.hash_ref))
  clazz=vIWcN(backend2)
  backend1=_infer_backend_init(clazz,sf2)
 else:
  backend1=load_persisted_object(config_context.get_obj_file_path(sf1.hash_ref))
  clazz=vIWcN(backend1)
  backend2=_infer_backend_init(clazz,sf1)
 diff=DeepDiff(backend1,backend2)
 return diff.to_json()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
