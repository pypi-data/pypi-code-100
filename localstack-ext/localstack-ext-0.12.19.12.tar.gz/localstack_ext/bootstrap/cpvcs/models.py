from datetime import datetime
ivSlI=str
ivSlR=int
ivSlO=super
ivSlF=False
ivSlH=isinstance
ivSlN=hash
ivSlx=True
ivSlU=list
ivSlG=map
ivSlX=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:ivSlI):
  self.hash_ref:ivSlI=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:ivSlI,rel_path:ivSlI,file_name:ivSlI,size:ivSlR,service:ivSlI,region:ivSlI):
  ivSlO().__init__(hash_ref)
  self.rel_path:ivSlI=rel_path
  self.file_name:ivSlI=file_name
  self.size:ivSlR=size
  self.service:ivSlI=service
  self.region:ivSlI=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,ivSlN=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return ivSlF
  if not ivSlH(other,StateFileRef):
   return ivSlF
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return ivSlN((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return ivSlF
  if not ivSlH(other,StateFileRef):
   return ivSlF
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return ivSlx
  return ivSlF
 def metadata(self)->ivSlI:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:ivSlI,state_files:Set[StateFileRef],parent_ptr:ivSlI):
  ivSlO().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:ivSlI=parent_ptr
 def state_files_info(self)->ivSlI:
  return "\n".join(ivSlU(ivSlG(lambda state_file:ivSlI(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:ivSlI,head_ptr:ivSlI,message:ivSlI,timestamp:ivSlI=ivSlI(datetime.now().timestamp()),delta_log_ptr:ivSlI=ivSlX):
  self.tail_ptr:ivSlI=tail_ptr
  self.head_ptr:ivSlI=head_ptr
  self.message:ivSlI=message
  self.timestamp:ivSlI=timestamp
  self.delta_log_ptr:ivSlI=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:ivSlI,to_node:ivSlI)->ivSlI:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:ivSlI,state_files:Set[StateFileRef],parent_ptr:ivSlI,creator:ivSlI,rid:ivSlI,revision_number:ivSlR,assoc_commit:Commit=ivSlX):
  ivSlO().__init__(hash_ref,state_files,parent_ptr)
  self.creator:ivSlI=creator
  self.rid:ivSlI=rid
  self.revision_number:ivSlR=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(ivSlN=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(ivSlG(lambda state_file:ivSlI(state_file),self.state_files))if self.state_files else "",assoc_commit=ivSlI(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:ivSlI,state_files:Set[StateFileRef],parent_ptr:ivSlI,creator:ivSlI,comment:ivSlI,active_revision_ptr:ivSlI,outgoing_revision_ptrs:Set[ivSlI],incoming_revision_ptr:ivSlI,version_number:ivSlR):
  ivSlO().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(ivSlN=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(ivSlG(lambda stat_file:ivSlI(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
