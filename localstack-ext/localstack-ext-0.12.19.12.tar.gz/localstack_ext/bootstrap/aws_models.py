from localstack.utils.aws import aws_models
vESoM=super
vESoH=None
vESox=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vESoM(LambdaLayer,self).__init__(arn)
  self.cwd=vESoH
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vESox.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(RDSDatabase,self).__init__(vESox,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(RDSCluster,self).__init__(vESox,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(AppSyncAPI,self).__init__(vESox,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(AmplifyApp,self).__init__(vESox,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(ElastiCacheCluster,self).__init__(vESox,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(TransferServer,self).__init__(vESox,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(CloudFrontDistribution,self).__init__(vESox,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vESox,env=vESoH):
  vESoM(CodeCommitRepository,self).__init__(vESox,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
