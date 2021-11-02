from datetime import datetime
yGueH=str
yGueo=int
yGueY=super
yGuet=False
yGueg=isinstance
yGueD=hash
yGueN=True
yGuen=list
yGueF=map
yGueP=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:yGueH):
  self.hash_ref:yGueH=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:yGueH,rel_path:yGueH,file_name:yGueH,size:yGueo,service:yGueH,region:yGueH):
  yGueY().__init__(hash_ref)
  self.rel_path:yGueH=rel_path
  self.file_name:yGueH=file_name
  self.size:yGueo=size
  self.service:yGueH=service
  self.region:yGueH=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,yGueD=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return yGuet
  if not yGueg(other,StateFileRef):
   return yGuet
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return yGueD((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return yGuet
  if not yGueg(other,StateFileRef):
   return yGuet
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return yGueN
  return yGuet
 def metadata(self)->yGueH:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:yGueH,state_files:Set[StateFileRef],parent_ptr:yGueH):
  yGueY().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:yGueH=parent_ptr
 def state_files_info(self)->yGueH:
  return "\n".join(yGuen(yGueF(lambda state_file:yGueH(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:yGueH,head_ptr:yGueH,message:yGueH,timestamp:yGueH=yGueH(datetime.now().timestamp()),delta_log_ptr:yGueH=yGueP):
  self.tail_ptr:yGueH=tail_ptr
  self.head_ptr:yGueH=head_ptr
  self.message:yGueH=message
  self.timestamp:yGueH=timestamp
  self.delta_log_ptr:yGueH=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:yGueH,to_node:yGueH)->yGueH:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:yGueH,state_files:Set[StateFileRef],parent_ptr:yGueH,creator:yGueH,rid:yGueH,revision_number:yGueo,assoc_commit:Commit=yGueP):
  yGueY().__init__(hash_ref,state_files,parent_ptr)
  self.creator:yGueH=creator
  self.rid:yGueH=rid
  self.revision_number:yGueo=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(yGueD=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(yGueF(lambda state_file:yGueH(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:yGueH,state_files:Set[StateFileRef],parent_ptr:yGueH,creator:yGueH,comment:yGueH,active_revision_ptr:yGueH,outgoing_revision_ptrs:Set[yGueH],incoming_revision_ptr:yGueH,version_number:yGueo):
  yGueY().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(yGueD=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(yGueF(lambda stat_file:yGueH(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
