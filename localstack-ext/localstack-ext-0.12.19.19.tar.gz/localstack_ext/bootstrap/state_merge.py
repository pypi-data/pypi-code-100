import contextlib
lueAo=None
lueAN=isinstance
lueAJ=list
lueAp=True
lueAk=type
lueAG=Exception
lueAF=str
lueAn=dict
lueAD=getattr
lueAT=len
lueAz=range
lueAb=tuple
lueAd=map
lueAB=bool
lueAc=False
lueAK=open
import inspect
import json
import logging
import os
import sqlite3
from typing import Any,Dict,Set,Type
from localstack.utils.common import ArbitraryAccessObj
from moto.s3.models import FakeBucket
from moto.sqs.models import Queue
from localstack_ext.bootstrap.state_utils import(check_already_visited,get_object_dict,is_composite_type)
LOG=logging.getLogger(__name__)
DDB_PREDEF_TABLES=("dm","cf","sm","ss","tr","us")
def _merge_helper(current,injecting,merge_strategy=lueAo,visited:Set=lueAo):
 if lueAN(current,lueAJ)and lueAN(injecting,lueAJ):
  current.extend(injecting)
  return
 if not is_composite_type(current)or not is_composite_type(injecting):
  return
 cycle,visited=check_already_visited(injecting,visited)
 if cycle:
  return
 cur_dict=get_object_dict(current)
 inj_dict=get_object_dict(injecting)
 for field_name,inj_field_value in inj_dict.items():
  cur_field_value=cur_dict.get(field_name)
  if cur_field_value is not lueAo:
   if is_composite_type(cur_field_value):
    _merge_helper(cur_field_value,inj_field_value,merge_strategy=merge_strategy,visited=visited)
   elif cur_field_value!=inj_field_value:
    LOG.debug("Overwriting existing value with new state: '%s' <> '%s'"%(cur_field_value,inj_field_value))
    cur_dict[field_name]=inj_field_value
  else:
   cur_dict[field_name]=inj_field_value
 return cur_dict
def merge_object_state(current,injecting,merge_strategy=lueAo):
 if not current or not injecting:
  return current
 is_special_case=handle_special_case(current,injecting)
 if is_special_case:
  return current
 _merge_helper(current,injecting)
 add_missing_attributes(current)
 return current
def handle_special_case(current,injecting):
 if lueAN(injecting,Queue):
  current.queues[injecting.name]=injecting
  return lueAp
 elif lueAN(injecting,FakeBucket):
  current["global"].buckets[injecting.name]=injecting
  return lueAp
def add_missing_attributes(obj:Any,safe:lueAB=lueAp,visited:Set=lueAo):
 try:
  obj_dict=get_object_dict(obj)
  if obj_dict is lueAo:
   return
  cycle,visited=check_already_visited(obj,visited)
  if cycle:
   return
  for attr_value in obj_dict.values():
   add_missing_attributes(attr_value,safe=safe,visited=visited)
  class_inst_attrs=infer_class_attributes(lueAk(obj))
  for key,value in class_inst_attrs.items():
   if key not in obj_dict:
    LOG.debug("Add missing attribute '%s' to state object of type %s"%(key,lueAk(obj)))
    obj_dict[key]=value
 except lueAG as e:
  if not safe:
   raise
  LOG.warning("Unable to add missing attributes to persistence state object %s: %s",(obj,e))
def infer_class_attributes(clazz:Type)->Dict[lueAF,Any]:
 if clazz in[lueAJ,lueAn]or not inspect.isclass(clazz)or clazz.__name__=="function":
  return{}
 constructor=lueAD(clazz,"__init__",lueAo)
 if not constructor:
  return{}
 try:
  sig_args=inspect.getfullargspec(constructor)
  def get_default_arg_value(arg_name,arg_index=-1):
   arg_defaults=sig_args.defaults or[]
   num_non_default_args=lueAT(sig_args.args or[])-lueAT(arg_defaults)
   offset=arg_index-num_non_default_args
   if offset in lueAz(lueAT(arg_defaults)):
    return arg_defaults[offset]
   kwargs_defaults=sig_args.kwonlydefaults or{}
   if arg_name in kwargs_defaults:
    return kwargs_defaults[arg_name]
   return ArbitraryAccessObj()
  args=[]
  kwargs={}
  for arg_idx in lueAz(1,lueAT(sig_args.args)):
   args.append(get_default_arg_value(sig_args.args[arg_idx],arg_index=arg_idx))
  for arg in sig_args.kwonlyargs:
   kwargs[arg]=get_default_arg_value(arg)
  instance=clazz(*args,**kwargs)
  result=lueAn(instance.__dict__)
  return result
 except lueAG:
  return{}
def merge_sqllite_dbs(file_dest:lueAF,file_src:lueAF)->lueAo:
 def _merge_table(table_name:lueAF,cursor_a,cursor_b)->lueAo:
  tmp_table_name=f"'{table_name}_new'"
  table_name=f"'{table_name}'"
  select_query=f"SELECT * FROM {table_name}"
  if table_name=="'cf'":
   return
  schema=lueAb(lueAd(lambda x:x[1],cursor_b.execute(f"PRAGMA table_info({table_name})")))
  params=f"({('?,' * len(schema))[:-1]})"
  insert_str=f"INSERT INTO {tmp_table_name} {str(schema)} values {params}"
  if table_name=="'dm'":
   excl_tables=(lueAF(lueAJ(lueAd(lambda x:x[0],cursor_a.execute(f"SELECT TableName FROM {table_name}")))).replace("[","(",1).replace("]",")",1))
   select_query+=f"AS O_T WHERE O_T.TableName NOT IN {excl_tables}"
  cursor_a.execute(f"CREATE TABLE IF NOT EXISTS {tmp_table_name} AS SELECT * FROM {table_name}")
  for row in cursor_b.execute(select_query):
   cursor_a.execute(insert_str,row)
  cursor_a.execute(f"DROP TABLE IF EXISTS {table_name}")
  cursor_a.execute(f"ALTER TABLE {tmp_table_name} RENAME TO {table_name}")
 with contextlib.closing(sqlite3.connect(file_dest))as db_src,contextlib.closing(sqlite3.connect(file_src))as db_target:
  cursor_dest=db_src.cursor()
  cursor_src=db_target.cursor()
  table_names=lueAJ(lueAd(lambda x:x[0],cursor_dest.execute("SELECT name FROM sqlite_master WHERE type='table'")))
  for current_table in table_names:
   try:
    _merge_table(current_table,cursor_dest,cursor_src)
   except sqlite3.OperationalError as e:
    LOG.warning(f"Failed to merge table {current_table}: {e}")
    cursor_dest.execute(f"DROP TABLE IF EXISTS '{current_table}'")
    db_src.rollback()
    return
  db_src.commit()
  LOG.debug(f"Successfully merged db at {file_src} into {file_dest}")
def merge_kinesis_state(path_dest:lueAF,path_src:lueAF)->lueAB:
 state_file="kinesis-data.json"
 datadir_statefile=os.path.join(path_dest,state_file)
 tmp_dir_statefile=os.path.join(path_src,state_file)
 if not os.path.isfile(datadir_statefile):
  LOG.info(f"Could not find statefile in path destination {path_dest}")
  return lueAc
 if not os.path.isfile(tmp_dir_statefile):
  LOG.info(f"Could not find statefile in path source {path_src}")
  return lueAc
 with lueAK(datadir_statefile)as datadir_kinesis_file,lueAK(tmp_dir_statefile)as tmp_dir_kinesis_file:
  datadir_kinesis_json=json.load(datadir_kinesis_file)
  tmp_dir_kinesis_json=json.load(tmp_dir_kinesis_file)
  datadir_streams=datadir_kinesis_json.get("streams",[])
  tmp_dir_streams=tmp_dir_kinesis_json.get("streams",[])
  if lueAT(tmp_dir_streams)>0:
   datadir_stream_names=datadir_streams.keys()
   for stream in tmp_dir_streams:
    if stream not in datadir_stream_names:
     datadir_streams[stream]=tmp_dir_streams.get(stream)
     LOG.debug(f"Copied state from stream {stream}")
   with lueAK(datadir_statefile,"w")as mutated_datadir_kinesis_file:
    mutated_datadir_kinesis_file.write(json.dumps(datadir_kinesis_json))
   return lueAp
 return lueAc
# Created by pyminifier (https://github.com/liftoff/pyminifier)
