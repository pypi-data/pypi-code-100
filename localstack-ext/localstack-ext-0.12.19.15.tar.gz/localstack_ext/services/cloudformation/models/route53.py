from localstack.services.cloudformation.service_models import REF_ID_ATTRS,GenericBaseModel
fWoPT=str
fWoPw=staticmethod
fWoPm=None
fWoPd=super
from localstack.utils.aws import aws_stack
from localstack.utils.common import select_attributes,short_uid
def canonicalize_name(name:fWoPT)->fWoPT:
 if name[-1]!=".":
  return f"{name}."
 return name
class Route53HostedZone(GenericBaseModel):
 @fWoPw
 def cloudformation_type():
  return "AWS::Route53::HostedZone"
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("route53")
  result=client.list_hosted_zones()["HostedZones"]
  canonical_name=canonicalize_name(self.props.get("Name"))
  result=[z for z in result if z["Name"]==canonical_name]
  return(result or[fWoPm])[0]
 def get_physical_resource_id(self,attribute=fWoPm,**kwargs):
  return self.props.get("Id")
 def get_cfn_attribute(self,attribute_name):
  if attribute_name=="NameServers":
   return[self.props.get("Name")]
  if attribute_name in REF_ID_ATTRS:
   return self.get_physical_resource_id()
  return fWoPd(Route53HostedZone,self).get_cfn_attribute(attribute_name)
 @fWoPw
 def get_deploy_templates():
  def _get_params(resource_props,resources,resource_id,*args,**kwargs):
   resource=Route53HostedZone(resources[resource_id])
   props=resource.props
   result=select_attributes(props,["HostedZoneConfig","Name"])
   vpcs=props.get("VPCs",[])
   result["VPC"]=vpcs and vpcs[0]or{}
   result["CallerReference"]=short_uid()
   return result
  def _get_id(resource_props,resources,resource_id,*args,**kwargs):
   resource=Route53HostedZone(resources[resource_id])
   return resource.props.get("Id")
  return{"create":{"function":"create_hosted_zone","parameters":_get_params},"delete":{"function":"delete_hosted_zone","parameters":{"Id":_get_id}}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
