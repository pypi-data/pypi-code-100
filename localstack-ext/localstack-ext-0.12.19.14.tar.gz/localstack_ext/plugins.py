import logging
kHIBK=Exception
kHIBE=any
kHIBq=str
kHIBA=None
kHIBT=False
kHIBx=bool
import os
import traceback
from localstack import config as localstack_config
from localstack.constants import LOCALSTACK_INFRA_PROCESS,LOCALSTACK_WEB_PROCESS,TRUE_STRINGS
from localstack.utils import common
from localstack.utils.bootstrap import API_DEPENDENCIES,get_enabled_apis,is_api_enabled
from localstack_ext import config as config_ext
from localstack_ext.bootstrap import install,licensing,local_daemon
LOG=logging.getLogger(__name__)
EXTERNAL_PORT_APIS=("apigateway","apigatewayv2","athena","cloudfront","codecommit","ecs","ecr","elasticache","mediastore","rds","transfer","kafka","neptune","azure")
API_DEPENDENCIES.update({"amplify":["s3","appsync","cognito"],"apigateway":["apigatewayv2"],"athena":["emr"],"docdb":["rds"],"ecs":["ecr"],"elasticache":["ec2"],"elb":["elbv2"],"emr":["athena","s3"],"glacier":["s3"],"glue":["rds"],"iot":["iot-analytics","iot-data","iotwireless"],"kinesisanalytics":["kinesis","dynamodb"],"neptune":["rds"],"rds":["rds-data"],"redshift":["redshift-data"],"timestream":["timestream-write","timestream-query"],"transfer":["s3"]})
get_enabled_apis.cache_clear()
def register_localstack_plugins():
 _setup_logging()
 is_infra_process=os.environ.get(LOCALSTACK_INFRA_PROCESS)in TRUE_STRINGS
 is_api_key_configured=api_key_configured()
 if is_infra_process:
  install.install_libs()
  if is_api_key_configured:
   install.setup_ssl_cert()
 if os.environ.get(LOCALSTACK_WEB_PROCESS):
  return{}
 with licensing.prepare_environment():
  try:
   from localstack_ext.services import dns_server
   dns_server.setup_network_configuration()
  except kHIBK:
   return
  if is_infra_process:
   load_plugin_files()
  try:
   if is_api_key_configured and not is_infra_process and is_api_enabled("ec2"):
    local_daemon.start_in_background()
  except kHIBK as e:
   LOG.warning("Unable to start local daemon process: %s"%e)
  if is_api_key_configured:
   if os.environ.get("EDGE_PORT")and not localstack_config.EDGE_PORT_HTTP:
    LOG.warning(("!! Configuring EDGE_PORT={p} without setting EDGE_PORT_HTTP may lead "+"to issues; better leave the defaults, or set EDGE_PORT=443 and EDGE_PORT_HTTP={p}").format(p=localstack_config.EDGE_PORT))
   else:
    port=localstack_config.EDGE_PORT
    localstack_config.EDGE_PORT=443
    localstack_config.EDGE_PORT_HTTP=port
 docker_flags=[]
 if config_ext.use_custom_dns():
  if not common.is_port_open(dns_server.DNS_PORT,protocols="tcp"):
   docker_flags+=["-p {a}:{p}:{p}".format(a=config_ext.DNS_ADDRESS,p=dns_server.DNS_PORT)]
  if not common.is_port_open(dns_server.DNS_PORT,protocols="udp"):
   docker_flags+=["-p {a}:{p}:{p}/udp".format(a=config_ext.DNS_ADDRESS,p=dns_server.DNS_PORT)]
 if kHIBE([is_api_enabled(api)for api in EXTERNAL_PORT_APIS]):
  docker_flags+=["-p {start}-{end}:{start}-{end}".format(start=config_ext.SERVICE_INSTANCES_PORTS_START,end=config_ext.SERVICE_INSTANCES_PORTS_END)]
 if is_api_enabled("eks"):
  kube_config=os.path.expanduser("~/.kube/config")
  if os.path.exists(kube_config):
   docker_flags+=["-v %s:/root/.kube/config"%kube_config]
 if is_api_enabled("azure"):
  docker_flags+=["-p {port}:{port}".format(port=5671)]
 if os.environ.get("AZURE"):
  docker_flags+=["-p {p}:{p}".format(p=config_ext.PORT_AZURE)]
 result={"docker":{"run_flags":" ".join(docker_flags)}}
 return result
def load_plugin_files():
 try:
  from localstack_ext.bootstrap.dashboard import dashboard_extended
  from localstack_ext.services import edge
  from localstack_ext.utils import persistence as persistence_ext
  from localstack_ext.utils.aws import aws_utils
  persistence_ext.enable_extended_persistence()
  dashboard_extended.patch_dashboard()
  edge.patch_start_edge()
  patch_start_infra()
  aws_utils.patch_aws_utils()
  set_default_providers_to_pro()
 except kHIBK as e:
  if "No module named" not in kHIBq(e):
   print("ERROR: %s %s"%(e,traceback.format_exc()))
def set_default_providers_to_pro():
 from localstack.services.plugins import SERVICE_PLUGINS
 pro_services=SERVICE_PLUGINS.apis_with_provider("pro")
 localstack_config.SERVICE_PROVIDER_CONFIG.bulk_set_provider_if_not_exists(pro_services,"pro")
 for service in pro_services:
  try:
   LOG.debug("loading service plugin for %s",service)
   SERVICE_PLUGINS.get_service_container(service)
  except kHIBK as e:
   LOG.error("error while loading service %s: %s",service,e)
def patch_start_infra():
 from localstack.services import infra
 try:
  from localstack_ext.utils.aws.metadata_service import start_metadata_service
 except kHIBK:
  start_metadata_service=kHIBA
 def do_start_infra(asynchronous,apis,is_in_docker,*args,**kwargs):
  if common.in_docker():
   try:
    start_metadata_service and start_metadata_service()
   except kHIBK:
    pass
  enforce_before=config_ext.ENFORCE_IAM
  try:
   config_ext.ENFORCE_IAM=kHIBT
   return do_start_infra_orig(asynchronous,apis,is_in_docker,*args,**kwargs)
  finally:
   config_ext.ENFORCE_IAM=enforce_before
 do_start_infra_orig=infra.do_start_infra
 infra.do_start_infra=do_start_infra
def _setup_logging():
 log_level=logging.DEBUG if localstack_config.DEBUG else logging.INFO
 logging.getLogger("localstack_ext").setLevel(log_level)
 logging.getLogger("botocore").setLevel(logging.INFO)
 logging.getLogger("kubernetes").setLevel(logging.INFO)
 logging.getLogger("pyftpdlib").setLevel(logging.INFO)
 logging.getLogger("pyhive").setLevel(logging.INFO)
 logging.getLogger("websockets").setLevel(logging.INFO)
 logging.getLogger("asyncio").setLevel(logging.INFO)
 logging.getLogger("hpack").setLevel(logging.INFO)
 logging.getLogger("jnius.reflect").setLevel(logging.INFO)
 logging.getLogger("dulwich").setLevel(logging.ERROR)
 logging.getLogger("kazoo").setLevel(logging.ERROR)
 logging.getLogger("postgresql_proxy").setLevel(logging.WARNING)
 logging.getLogger("intercept").setLevel(logging.WARNING)
 logging.getLogger("root").setLevel(logging.WARNING)
 logging.getLogger("").setLevel(logging.WARNING)
def api_key_configured():
 return kHIBx(os.environ.get("LOCALSTACK_API_KEY"))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
