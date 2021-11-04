from datetime import datetime
UeyDI=str
UeyDF=int
UeyDl=super
UeyDa=False
UeyDC=isinstance
UeyDL=hash
UeyDT=True
UeyDW=list
UeyDw=map
UeyDg=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:UeyDI):
  self.hash_ref:UeyDI=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:UeyDI,rel_path:UeyDI,file_name:UeyDI,size:UeyDF,service:UeyDI,region:UeyDI):
  UeyDl(StateFileRef,self).__init__(hash_ref)
  self.rel_path:UeyDI=rel_path
  self.file_name:UeyDI=file_name
  self.size:UeyDF=size
  self.service:UeyDI=service
  self.region:UeyDI=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return UeyDa
  if not UeyDC(other,StateFileRef):
   return UeyDa
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return UeyDL((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return UeyDa
  if not UeyDC(other,StateFileRef):
   return UeyDa
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return UeyDT
  return UeyDa
 def metadata(self)->UeyDI:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:UeyDI,state_files:Set[StateFileRef],parent_ptr:UeyDI):
  UeyDl(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:UeyDI=parent_ptr
 def state_files_info(self)->UeyDI:
  return "\n".join(UeyDW(UeyDw(lambda state_file:UeyDI(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:UeyDI,head_ptr:UeyDI,message:UeyDI,timestamp:UeyDI=UeyDI(datetime.now().timestamp()),delta_log_ptr:UeyDI=UeyDg):
  self.tail_ptr:UeyDI=tail_ptr
  self.head_ptr:UeyDI=head_ptr
  self.message:UeyDI=message
  self.timestamp:UeyDI=timestamp
  self.delta_log_ptr:UeyDI=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:UeyDI,to_node:UeyDI)->UeyDI:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:UeyDI,state_files:Set[StateFileRef],parent_ptr:UeyDI,creator:UeyDI,rid:UeyDI,revision_number:UeyDF,assoc_commit:Commit=UeyDg):
  UeyDl(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:UeyDI=creator
  self.rid:UeyDI=rid
  self.revision_number:UeyDF=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(UeyDw(lambda state_file:UeyDI(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:UeyDI,state_files:Set[StateFileRef],parent_ptr:UeyDI,creator:UeyDI,comment:UeyDI,active_revision_ptr:UeyDI,outgoing_revision_ptrs:Set[UeyDI],incoming_revision_ptr:UeyDI,version_number:UeyDF):
  UeyDl(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(UeyDw(lambda stat_file:UeyDI(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
