from datetime import datetime
jrBMm=str
jrBMR=int
jrBMl=super
jrBME=False
jrBMF=isinstance
jrBMU=hash
jrBMH=True
jrBMh=list
jrBMN=map
jrBMu=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:jrBMm):
  self.hash_ref:jrBMm=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:jrBMm,rel_path:jrBMm,file_name:jrBMm,size:jrBMR,service:jrBMm,region:jrBMm):
  jrBMl().__init__(hash_ref)
  self.rel_path:jrBMm=rel_path
  self.file_name:jrBMm=file_name
  self.size:jrBMR=size
  self.service:jrBMm=service
  self.region:jrBMm=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,jrBMU=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return jrBME
  if not jrBMF(other,StateFileRef):
   return jrBME
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return jrBMU((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return jrBME
  if not jrBMF(other,StateFileRef):
   return jrBME
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return jrBMH
  return jrBME
 def metadata(self)->jrBMm:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:jrBMm,state_files:Set[StateFileRef],parent_ptr:jrBMm):
  jrBMl().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:jrBMm=parent_ptr
 def state_files_info(self)->jrBMm:
  return "\n".join(jrBMh(jrBMN(lambda state_file:jrBMm(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:jrBMm,head_ptr:jrBMm,message:jrBMm,timestamp:jrBMm=jrBMm(datetime.now().timestamp()),delta_log_ptr:jrBMm=jrBMu):
  self.tail_ptr:jrBMm=tail_ptr
  self.head_ptr:jrBMm=head_ptr
  self.message:jrBMm=message
  self.timestamp:jrBMm=timestamp
  self.delta_log_ptr:jrBMm=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:jrBMm,to_node:jrBMm)->jrBMm:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:jrBMm,state_files:Set[StateFileRef],parent_ptr:jrBMm,creator:jrBMm,rid:jrBMm,revision_number:jrBMR,assoc_commit:Commit=jrBMu):
  jrBMl().__init__(hash_ref,state_files,parent_ptr)
  self.creator:jrBMm=creator
  self.rid:jrBMm=rid
  self.revision_number:jrBMR=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(jrBMU=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(jrBMN(lambda state_file:jrBMm(state_file),self.state_files))if self.state_files else "",assoc_commit=jrBMm(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:jrBMm,state_files:Set[StateFileRef],parent_ptr:jrBMm,creator:jrBMm,comment:jrBMm,active_revision_ptr:jrBMm,outgoing_revision_ptrs:Set[jrBMm],incoming_revision_ptr:jrBMm,version_number:jrBMR):
  jrBMl().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(jrBMU=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(jrBMN(lambda stat_file:jrBMm(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
