from datetime import datetime
CwJsI=str
CwJso=int
CwJsN=super
CwJsv=False
CwJsR=isinstance
CwJsL=hash
CwJsj=True
CwJsm=list
CwJsp=map
CwJsE=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:CwJsI):
  self.hash_ref:CwJsI=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:CwJsI,rel_path:CwJsI,file_name:CwJsI,size:CwJso,service:CwJsI,region:CwJsI):
  CwJsN(StateFileRef,self).__init__(hash_ref)
  self.rel_path:CwJsI=rel_path
  self.file_name:CwJsI=file_name
  self.size:CwJso=size
  self.service:CwJsI=service
  self.region:CwJsI=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return CwJsv
  if not CwJsR(other,StateFileRef):
   return CwJsv
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return CwJsL((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return CwJsv
  if not CwJsR(other,StateFileRef):
   return CwJsv
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return CwJsj
  return CwJsv
 def metadata(self)->CwJsI:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:CwJsI,state_files:Set[StateFileRef],parent_ptr:CwJsI):
  CwJsN(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:CwJsI=parent_ptr
 def state_files_info(self)->CwJsI:
  return "\n".join(CwJsm(CwJsp(lambda state_file:CwJsI(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:CwJsI,head_ptr:CwJsI,message:CwJsI,timestamp:CwJsI=CwJsI(datetime.now().timestamp()),delta_log_ptr:CwJsI=CwJsE):
  self.tail_ptr:CwJsI=tail_ptr
  self.head_ptr:CwJsI=head_ptr
  self.message:CwJsI=message
  self.timestamp:CwJsI=timestamp
  self.delta_log_ptr:CwJsI=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:CwJsI,to_node:CwJsI)->CwJsI:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:CwJsI,state_files:Set[StateFileRef],parent_ptr:CwJsI,creator:CwJsI,rid:CwJsI,revision_number:CwJso,assoc_commit:Commit=CwJsE):
  CwJsN(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:CwJsI=creator
  self.rid:CwJsI=rid
  self.revision_number:CwJso=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(CwJsp(lambda state_file:CwJsI(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:CwJsI,state_files:Set[StateFileRef],parent_ptr:CwJsI,creator:CwJsI,comment:CwJsI,active_revision_ptr:CwJsI,outgoing_revision_ptrs:Set[CwJsI],incoming_revision_ptr:CwJsI,version_number:CwJso):
  CwJsN(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(CwJsp(lambda stat_file:CwJsI(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
