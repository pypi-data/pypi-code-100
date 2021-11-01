import base64
srDRI=None
srDRq=Exception
srDRo=True
srDRW=str
srDRp=len
srDRM=False
srDRC=int
srDRz=range
srDRi=object
import glob
import json
import logging
import os
import re
import sys
import traceback
import pyaes
from localstack import config as localstack_config
from localstack.constants import ENV_PRO_ACTIVATED
from localstack.utils.common import load_file,md5,now_utc,parallelize
from localstack.utils.common import safe_requests as requests
from localstack.utils.common import save_file,str_insert,str_remove,to_bytes,to_str
from localstack_ext import __version__,config
from localstack_ext.config import PROTECTED_FOLDERS,ROOT_FOLDER
ENV_PREPARED={}
MAX_KEY_CACHE_DURATION_SECS=60*60*24
LOG=logging.getLogger(__name__)
ENV_LOCALSTACK_API_KEY="LOCALSTACK_API_KEY"
TEST_AUTH_HEADERS=srDRI
class KeyActivationError(srDRq):
 def __init__(self,message:srDRW=srDRI):
  self.message=message
class CachedKeyError(KeyActivationError):
 pass
class InvalidKeyError(KeyActivationError):
 pass
def read_api_key(raise_if_missing=srDRo):
 key=(os.environ.get(ENV_LOCALSTACK_API_KEY)or "").strip()
 if not key and raise_if_missing:
  raise srDRq("Unable to retrieve API key. Please configure $%s in your environment"%ENV_LOCALSTACK_API_KEY)
 return key
def truncate_api_key(api_key:srDRW):
 return '"%s..."(%s)'%(api_key[:3],srDRp(api_key))
def fetch_key():
 api_key=read_api_key()
 if api_key=="test":
  return "test"
 data={"api_key":api_key,"version":__version__}
 try:
  logging.getLogger("py.warnings").setLevel(logging.ERROR)
  result=requests.post("%s/activate"%config.API_URL,json.dumps(data),verify=srDRM)
  if result.status_code>=400:
   content=result.content
   content_type=result.headers.get("Content-Type")
   if result.status_code==403:
    message=json.loads(to_str(content))["message"]
    raise InvalidKeyError("Activation key %s is invalid or expired! Reason: %s"%(truncate_api_key(api_key),message))
   raise KeyActivationError('Received error activating key (code %s): ctype "%s" - %s'%(result.status_code,content_type,content))
  key_base64=json.loads(to_str(result.content))["key"]
  cache_key_locally(api_key,key_base64)
 except InvalidKeyError:
  raise
 except srDRq as e:
  if log_license_issues():
   api_key=srDRW(api_key_configured()or "")
   LOG.warning("Error activating API key %s: %s %s"%(truncate_api_key(api_key),e,traceback.format_exc()))
   LOG.warning("Looking for cached key as fallback...")
  key_base64=load_cached_key(api_key)
 finally:
  logging.getLogger("py.warnings").setLevel(logging.WARNING)
 decoded_key=to_str(base64.b64decode(key_base64))
 return decoded_key
def cache_key_locally(api_key,key_b64):
 configs=localstack_config.load_config_file()
 timestamp=srDRW(srDRC(now_utc()))
 key_raw=to_str(base64.b64decode(key_b64))
 for i in srDRz(srDRp(timestamp)):
  key_raw=str_insert(key_raw,i*2,timestamp[i])
 key_b64=to_str(base64.b64encode(to_bytes(key_raw)))
 configs["cached_key"]={"timestamp":srDRC(timestamp),"key_hash":md5(api_key),"key":key_b64}
 save_file(localstack_config.CONFIG_FILE_PATH,json.dumps(configs))
 return configs
def load_cached_key(api_key):
 configs=localstack_config.load_config_file()
 cached_key=configs.get("cached_key")
 if not cached_key:
  raise CachedKeyError("Could not find cached key")
 if cached_key.get("key_hash")!=md5(api_key):
  raise CachedKeyError("Cached key was created for a different API key")
 now=now_utc()
 if(now-cached_key["timestamp"])>MAX_KEY_CACHE_DURATION_SECS:
  raise CachedKeyError("Cached key expired")
 timestamp=srDRW(cached_key["timestamp"])
 key_raw=to_str(base64.b64decode(cached_key["key"]))
 for i in srDRz(srDRp(timestamp)):
  assert key_raw[i]==timestamp[i]
  key_raw=str_remove(key_raw,i)
 key_b64=to_str(base64.b64encode(to_bytes(key_raw)))
 return key_b64
def generate_aes_cipher(key):
 key=to_bytes(key)
 return pyaes.AESModeOfOperationCBC(key,iv="\0"*16)
def decrypt_file(source,target,key):
 cipher=generate_aes_cipher(key)
 raw=load_file(source,mode="rb")
 decrypter=pyaes.Decrypter(cipher)
 decrypted=decrypter.feed(raw)
 decrypted+=decrypter.feed()
 decrypted=decrypted.partition(b"\0")[0]
 decrypted=to_str(decrypted)
 save_file(target,content=decrypted)
def decrypt_files(key):
 files=[]
 for folder in PROTECTED_FOLDERS:
  for subpath in("*.py.enc","**/*.py.enc"):
   for f in glob.glob("%s/localstack_ext/%s/%s"%(ROOT_FOLDER,folder,subpath)):
    files.append(f)
 def _decrypt(f):
  target=f[:-4]
  if not os.path.exists(target):
   decrypt_file(f,target,key)
 parallelize(_decrypt,files)
def cleanup_environment():
 if not localstack_config.is_in_docker:
  return
 excepted_files=r".*/services/((edge)|(dns_server)|(__init__))\.py"
 for folder in PROTECTED_FOLDERS:
  for subpath in("*.py.enc","**/*.py.enc"):
   for f in glob.glob("%s/localstack_ext/%s/%s"%(ROOT_FOLDER,folder,subpath)):
    target=f[:-4]
    if not re.match(excepted_files,target):
     for delete_file in(target,"%sc"%target):
      if os.path.exists(delete_file):
       os.remove(delete_file)
def check_require_pro():
 if config.REQUIRE_PRO:
  LOG.error("Unable to activate API key, but $REQUIRE_PRO is configured - quitting.")
  sys.exit(1)
def prepare_environment():
 class OnClose(srDRi):
  def __exit__(self,*args,**kwargs):
   if not ENV_PREPARED.get("finalized"):
    cleanup_environment()
   ENV_PREPARED["finalized"]=srDRo
  def __enter__(self,*args,**kwargs):
   pass
 if not ENV_PREPARED.get("finalized"):
  try:
   key=fetch_key()
   if not key:
    raise srDRq("Unable to fetch and validate API key from environment")
   if key!="test":
    decrypt_files(key)
    LOG.info("Successfully activated API key")
   else:
    LOG.info("Using test API key")
   os.environ[ENV_PRO_ACTIVATED]="1"
  except KeyActivationError as e:
   if log_license_issues():
    LOG.warning(e.message)
   check_require_pro()
  except srDRq as e:
   if log_license_issues():
    LOG.warning("Unable to activate API key: %s %s"%(e,traceback.format_exc()))
   check_require_pro()
 return OnClose()
def log_license_issues():
 return api_key_configured()and localstack_config.is_env_not_false("LOG_LICENSE_ISSUES")
def api_key_configured():
 return read_api_key(raise_if_missing=srDRM)
def is_logged_in():
 configs=localstack_config.load_config_file()
 login_info=configs.get("login")
 if not login_info:
  return srDRM
 return srDRo
def get_auth_headers():
 if TEST_AUTH_HEADERS:
  return TEST_AUTH_HEADERS
 configs=localstack_config.load_config_file()
 login_info=configs.get("login")
 if login_info:
  auth_token=login_info["token"]
  if not auth_token.startswith("%s "%login_info["provider"]):
   auth_token="%s %s"%(login_info["provider"],auth_token)
  return{"authorization":auth_token}
 api_key=read_api_key(raise_if_missing=srDRM)
 if api_key:
  return{"ls-api-key":api_key,"ls-version":__version__}
 raise srDRq("Please log in first")
# Created by pyminifier (https://github.com/liftoff/pyminifier)
