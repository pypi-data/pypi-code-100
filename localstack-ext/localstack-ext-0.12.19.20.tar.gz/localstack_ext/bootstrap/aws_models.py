from localstack.utils.aws import aws_models
KcaML=super
KcaMz=None
KcaMJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KcaML(LambdaLayer,self).__init__(arn)
  self.cwd=KcaMz
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KcaMJ.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(RDSDatabase,self).__init__(KcaMJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(RDSCluster,self).__init__(KcaMJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(AppSyncAPI,self).__init__(KcaMJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(AmplifyApp,self).__init__(KcaMJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(ElastiCacheCluster,self).__init__(KcaMJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(TransferServer,self).__init__(KcaMJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(CloudFrontDistribution,self).__init__(KcaMJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KcaMJ,env=KcaMz):
  KcaML(CodeCommitRepository,self).__init__(KcaMJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
