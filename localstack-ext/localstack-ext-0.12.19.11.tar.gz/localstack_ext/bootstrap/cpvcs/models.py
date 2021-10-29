from datetime import datetime
WlUPN=str
WlUPQ=int
WlUPS=super
WlUPH=False
WlUPM=isinstance
WlUPn=hash
WlUPh=True
WlUPG=list
WlUPX=map
WlUPr=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:WlUPN):
  self.hash_ref:WlUPN=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:WlUPN,rel_path:WlUPN,file_name:WlUPN,size:WlUPQ,service:WlUPN,region:WlUPN):
  WlUPS().__init__(hash_ref)
  self.rel_path:WlUPN=rel_path
  self.file_name:WlUPN=file_name
  self.size:WlUPQ=size
  self.service:WlUPN=service
  self.region:WlUPN=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,WlUPn=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return WlUPH
  if not WlUPM(other,StateFileRef):
   return WlUPH
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return WlUPn((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other):
  if not other:
   return WlUPH
  if not WlUPM(other,StateFileRef):
   return WlUPH
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others):
  for other in others:
   if self.congruent(other):
    return WlUPh
  return WlUPH
 def metadata(self)->WlUPN:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:WlUPN,state_files:Set[StateFileRef],parent_ptr:WlUPN):
  WlUPS().__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:WlUPN=parent_ptr
 def state_files_info(self)->WlUPN:
  return "\n".join(WlUPG(WlUPX(lambda state_file:WlUPN(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:WlUPN,head_ptr:WlUPN,message:WlUPN,timestamp:WlUPN=WlUPN(datetime.now().timestamp()),delta_log_ptr:WlUPN=WlUPr):
  self.tail_ptr:WlUPN=tail_ptr
  self.head_ptr:WlUPN=head_ptr
  self.message:WlUPN=message
  self.timestamp:WlUPN=timestamp
  self.delta_log_ptr:WlUPN=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:WlUPN,to_node:WlUPN)->WlUPN:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:WlUPN,state_files:Set[StateFileRef],parent_ptr:WlUPN,creator:WlUPN,rid:WlUPN,revision_number:WlUPQ,assoc_commit:Commit=WlUPr):
  WlUPS().__init__(hash_ref,state_files,parent_ptr)
  self.creator:WlUPN=creator
  self.rid:WlUPN=rid
  self.revision_number:WlUPQ=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(WlUPn=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(WlUPX(lambda state_file:WlUPN(state_file),self.state_files))if self.state_files else "",assoc_commit=WlUPN(self.assoc_commit))
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:WlUPN,state_files:Set[StateFileRef],parent_ptr:WlUPN,creator:WlUPN,comment:WlUPN,active_revision_ptr:WlUPN,outgoing_revision_ptrs:Set[WlUPN],incoming_revision_ptr:WlUPN,version_number:WlUPQ):
  WlUPS().__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(WlUPn=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(WlUPX(lambda stat_file:WlUPN(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
