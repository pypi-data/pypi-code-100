from localstack.utils.aws import aws_models
nuWEM=super
nuWEA=None
nuWED=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nuWEM(LambdaLayer,self).__init__(arn)
  self.cwd=nuWEA
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nuWED.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(RDSDatabase,self).__init__(nuWED,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(RDSCluster,self).__init__(nuWED,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(AppSyncAPI,self).__init__(nuWED,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(AmplifyApp,self).__init__(nuWED,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(ElastiCacheCluster,self).__init__(nuWED,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(TransferServer,self).__init__(nuWED,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(CloudFrontDistribution,self).__init__(nuWED,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nuWED,env=nuWEA):
  nuWEM(CodeCommitRepository,self).__init__(nuWED,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
