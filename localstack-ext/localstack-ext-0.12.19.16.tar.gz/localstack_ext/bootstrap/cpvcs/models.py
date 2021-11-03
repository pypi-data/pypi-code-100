from datetime import datetime
WTLVU=str
WTLVp=int
WTLVx=super
WTLVS=False
WTLVc=isinstance
WTLVI=hash
WTLVQ=True
WTLVa=list
WTLVy=map
WTLVo=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:WTLVU):
  self.hash_ref:WTLVU=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:WTLVU,rel_path:WTLVU,file_name:WTLVU,size:WTLVp,service:WTLVU,region:WTLVU):
  WTLVx(StateFileRef,self).__init__(hash_ref)
  self.rel_path:WTLVU=rel_path
  self.file_name:WTLVU=file_name
  self.size:WTLVp=size
  self.service:WTLVU=service
  self.region:WTLVU=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,WTLVI=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return WTLVS
  if not WTLVc(other,StateFileRef):
   return WTLVS
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return WTLVI((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return WTLVS
  if not WTLVc(other,StateFileRef):
   return WTLVS
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return WTLVQ
  return WTLVS
 def metadata(self)->WTLVU:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:WTLVU,state_files:Set[StateFileRef],parent_ptr:WTLVU):
  WTLVx(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:WTLVU=parent_ptr
 def state_files_info(self)->WTLVU:
  return "\n".join(WTLVa(WTLVy(lambda state_file:WTLVU(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:WTLVU,head_ptr:WTLVU,message:WTLVU,timestamp:WTLVU=WTLVU(datetime.now().timestamp()),delta_log_ptr:WTLVU=WTLVo):
  self.tail_ptr:WTLVU=tail_ptr
  self.head_ptr:WTLVU=head_ptr
  self.message:WTLVU=message
  self.timestamp:WTLVU=timestamp
  self.delta_log_ptr:WTLVU=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:WTLVU,to_node:WTLVU)->WTLVU:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:WTLVU,state_files:Set[StateFileRef],parent_ptr:WTLVU,creator:WTLVU,rid:WTLVU,revision_number:WTLVp,assoc_commit:Commit=WTLVo):
  WTLVx(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:WTLVU=creator
  self.rid:WTLVU=rid
  self.revision_number:WTLVp=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(WTLVI=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(WTLVy(lambda state_file:WTLVU(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:WTLVU,state_files:Set[StateFileRef],parent_ptr:WTLVU,creator:WTLVU,comment:WTLVU,active_revision_ptr:WTLVU,outgoing_revision_ptrs:Set[WTLVU],incoming_revision_ptr:WTLVU,version_number:WTLVp):
  WTLVx(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(WTLVI=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(WTLVy(lambda stat_file:WTLVU(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
