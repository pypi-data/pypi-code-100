from localstack.services.cloudformation.service_models import REF_ATTRS,GenericBaseModel
oVpbi=staticmethod
oVpbr=super
from localstack.utils.aws import aws_stack
from localstack.utils.common import clone
class GlueTrigger(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Trigger"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   return self.props.get("Name")
  return oVpbr(GlueTrigger,self).get_cfn_attribute(attribute_name)
class GlueWorkflow(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Workflow"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   return self.props.get("Name")
  return oVpbr(GlueWorkflow,self).get_cfn_attribute(attribute_name)
class GlueJob(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Job"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   return self.props["Name"]
  return oVpbr(GlueJob,self).get_cfn_attribute(attribute_name)
class GlueCrawler(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Crawler"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   return self.props["Name"]
  return oVpbr(GlueCrawler,self).get_cfn_attribute(attribute_name)
 def fetch_state(self,stack_name,resources):
  crawler_name=self.props.get("Name")or self.resource_id
  crawler_name=self.resolve_refs_recursively(stack_name,crawler_name,resources)
  client=aws_stack.connect_to_service("glue")
  return client.get_crawler(Name=crawler_name)["Crawler"]
 @oVpbi
 def get_deploy_templates():
  def lambda_get_crawler_config(params,**kwargs):
   config=clone(params)
   if "Schedule" in config:
    config["Schedule"]=config["Schedule"]["ScheduleExpression"]
   config["Role"]=config.get("Role")or "_unknown_"
   return config
  return{"create":{"function":"create_crawler","parameters":lambda_get_crawler_config}}
class GlueDatabase(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Database"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   return self.props.get("DatabaseInput",{}).get("Name")
  return oVpbr(GlueDatabase,self).get_cfn_attribute(attribute_name)
class GlueClassifier(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Classifier"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   result=(self.props.get("GrokClassifier",{}).get("Name")or self.props.get("CsvClassifier",{}).get("Name")or self.props.get("JsonClassifier",{}).get("Name")or self.props.get("XMLClassifier",{}).get("Name"))
   if result:
    return result
  return oVpbr(GlueCrawler,self).get_cfn_attribute(attribute_name)
class GlueTable(GenericBaseModel):
 @oVpbi
 def cloudformation_type():
  return "AWS::Glue::Table"
 def get_cfn_attribute(self,attribute_name):
  if attribute_name in REF_ATTRS:
   return self.props.get("TableInput",{}).get("Name")
  return oVpbr(GlueTable,self).get_cfn_attribute(attribute_name)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
