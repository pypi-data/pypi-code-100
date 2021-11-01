from datetime import datetime
tAuhN=str
tAuhB=int
tAuhX=super
tAuhf=False
tAuhz=isinstance
tAuhy=hash
tAuhx=True
tAuhU=list
tAuhP=map
tAuhs=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:tAuhN):
  self.hash_ref:tAuhN=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:tAuhN,rel_path:tAuhN,file_name:tAuhN,size:tAuhB,service:tAuhN,region:tAuhN):
  tAuhX().__init__(hash_ref)
  self.rel_path:tAuhN=rel_path
  self.file_name:tAuhN=file_name
  self.size:tAuhB=size
  self.service:tAuhN=service
  self.region:tAuhN=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,tAuhy=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return tAuhf
  if not tAuhz(other,StateFileRef):
   return tAuhf
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return tAuhy((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return tAuhf
  if not tAuhz(other,StateFileRef):
   return tAuhf
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return tAuhx
  return tAuhf
 def metadata(self)->tAuhN:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:tAuhN,state_files:Set[StateFileRef],parent_ptr:tAuhN):
  tAuhX().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:tAuhN=parent_ptr
 def state_files_info(self)->tAuhN:
  return "\n".join(tAuhU(tAuhP(lambda state_file:tAuhN(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:tAuhN,head_ptr:tAuhN,message:tAuhN,timestamp:tAuhN=tAuhN(datetime.now().timestamp()),delta_log_ptr:tAuhN=tAuhs):
  self.tail_ptr:tAuhN=tail_ptr
  self.head_ptr:tAuhN=head_ptr
  self.message:tAuhN=message
  self.timestamp:tAuhN=timestamp
  self.delta_log_ptr:tAuhN=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:tAuhN,to_node:tAuhN)->tAuhN:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:tAuhN,state_files:Set[StateFileRef],parent_ptr:tAuhN,creator:tAuhN,rid:tAuhN,revision_number:tAuhB,assoc_commit:Commit=tAuhs):
  tAuhX().__init__(hash_ref,state_files,parent_ptr)
  self.creator:tAuhN=creator
  self.rid:tAuhN=rid
  self.revision_number:tAuhB=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(tAuhy=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(tAuhP(lambda state_file:tAuhN(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:tAuhN,state_files:Set[StateFileRef],parent_ptr:tAuhN,creator:tAuhN,comment:tAuhN,active_revision_ptr:tAuhN,outgoing_revision_ptrs:Set[tAuhN],incoming_revision_ptr:tAuhN,version_number:tAuhB):
  tAuhX().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(tAuhy=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(tAuhP(lambda stat_file:tAuhN(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
