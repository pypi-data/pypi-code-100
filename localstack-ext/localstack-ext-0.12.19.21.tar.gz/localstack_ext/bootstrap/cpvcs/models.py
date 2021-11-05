from datetime import datetime
Sgqsj=str
SgqsR=int
SgqsK=super
Sgqsu=False
Sgqso=isinstance
SgqsV=hash
Sgqse=True
SgqsQ=list
Sgqsz=map
SgqsO=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:Sgqsj):
  self.hash_ref:Sgqsj=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:Sgqsj,rel_path:Sgqsj,file_name:Sgqsj,size:SgqsR,service:Sgqsj,region:Sgqsj):
  SgqsK(StateFileRef,self).__init__(hash_ref)
  self.rel_path:Sgqsj=rel_path
  self.file_name:Sgqsj=file_name
  self.size:SgqsR=size
  self.service:Sgqsj=service
  self.region:Sgqsj=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return Sgqsu
  if not Sgqso(other,StateFileRef):
   return Sgqsu
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return SgqsV((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return Sgqsu
  if not Sgqso(other,StateFileRef):
   return Sgqsu
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return Sgqse
  return Sgqsu
 def metadata(self)->Sgqsj:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:Sgqsj,state_files:Set[StateFileRef],parent_ptr:Sgqsj):
  SgqsK(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:Sgqsj=parent_ptr
 def state_files_info(self)->Sgqsj:
  return "\n".join(SgqsQ(Sgqsz(lambda state_file:Sgqsj(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:Sgqsj,head_ptr:Sgqsj,message:Sgqsj,timestamp:Sgqsj=Sgqsj(datetime.now().timestamp()),delta_log_ptr:Sgqsj=SgqsO):
  self.tail_ptr:Sgqsj=tail_ptr
  self.head_ptr:Sgqsj=head_ptr
  self.message:Sgqsj=message
  self.timestamp:Sgqsj=timestamp
  self.delta_log_ptr:Sgqsj=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:Sgqsj,to_node:Sgqsj)->Sgqsj:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:Sgqsj,state_files:Set[StateFileRef],parent_ptr:Sgqsj,creator:Sgqsj,rid:Sgqsj,revision_number:SgqsR,assoc_commit:Commit=SgqsO):
  SgqsK(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:Sgqsj=creator
  self.rid:Sgqsj=rid
  self.revision_number:SgqsR=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(Sgqsz(lambda state_file:Sgqsj(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:Sgqsj,state_files:Set[StateFileRef],parent_ptr:Sgqsj,creator:Sgqsj,comment:Sgqsj,active_revision_ptr:Sgqsj,outgoing_revision_ptrs:Set[Sgqsj],incoming_revision_ptr:Sgqsj,version_number:SgqsR):
  SgqsK(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(Sgqsz(lambda stat_file:Sgqsj(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
