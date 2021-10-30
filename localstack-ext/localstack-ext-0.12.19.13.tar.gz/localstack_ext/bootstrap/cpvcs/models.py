from datetime import datetime
mpUMY=str
mpUMi=int
mpUMq=super
mpUMC=False
mpUMS=isinstance
mpUMT=hash
mpUMh=True
mpUMs=list
mpUMd=map
mpUMl=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:mpUMY):
  self.hash_ref:mpUMY=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:mpUMY,rel_path:mpUMY,file_name:mpUMY,size:mpUMi,service:mpUMY,region:mpUMY):
  mpUMq().__init__(hash_ref)
  self.rel_path:mpUMY=rel_path
  self.file_name:mpUMY=file_name
  self.size:mpUMi=size
  self.service:mpUMY=service
  self.region:mpUMY=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,mpUMT=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return mpUMC
  if not mpUMS(other,StateFileRef):
   return mpUMC
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return mpUMT((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return mpUMC
  if not mpUMS(other,StateFileRef):
   return mpUMC
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return mpUMh
  return mpUMC
 def metadata(self)->mpUMY:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:mpUMY,state_files:Set[StateFileRef],parent_ptr:mpUMY):
  mpUMq().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:mpUMY=parent_ptr
 def state_files_info(self)->mpUMY:
  return "\n".join(mpUMs(mpUMd(lambda state_file:mpUMY(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:mpUMY,head_ptr:mpUMY,message:mpUMY,timestamp:mpUMY=mpUMY(datetime.now().timestamp()),delta_log_ptr:mpUMY=mpUMl):
  self.tail_ptr:mpUMY=tail_ptr
  self.head_ptr:mpUMY=head_ptr
  self.message:mpUMY=message
  self.timestamp:mpUMY=timestamp
  self.delta_log_ptr:mpUMY=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:mpUMY,to_node:mpUMY)->mpUMY:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:mpUMY,state_files:Set[StateFileRef],parent_ptr:mpUMY,creator:mpUMY,rid:mpUMY,revision_number:mpUMi,assoc_commit:Commit=mpUMl):
  mpUMq().__init__(hash_ref,state_files,parent_ptr)
  self.creator:mpUMY=creator
  self.rid:mpUMY=rid
  self.revision_number:mpUMi=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(mpUMT=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(mpUMd(lambda state_file:mpUMY(state_file),self.state_files))if self.state_files else "",assoc_commit=mpUMY(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:mpUMY,state_files:Set[StateFileRef],parent_ptr:mpUMY,creator:mpUMY,comment:mpUMY,active_revision_ptr:mpUMY,outgoing_revision_ptrs:Set[mpUMY],incoming_revision_ptr:mpUMY,version_number:mpUMi):
  mpUMq().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(mpUMT=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(mpUMd(lambda stat_file:mpUMY(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
