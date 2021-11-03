from localstack.utils.aws import aws_models
EPipl=super
EPipz=None
EPipy=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EPipl(LambdaLayer,self).__init__(arn)
  self.cwd=EPipz
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EPipy.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(RDSDatabase,self).__init__(EPipy,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(RDSCluster,self).__init__(EPipy,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(AppSyncAPI,self).__init__(EPipy,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(AmplifyApp,self).__init__(EPipy,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(ElastiCacheCluster,self).__init__(EPipy,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(TransferServer,self).__init__(EPipy,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(CloudFrontDistribution,self).__init__(EPipy,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EPipy,env=EPipz):
  EPipl(CodeCommitRepository,self).__init__(EPipy,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
