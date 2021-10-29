from localstack.utils.aws import aws_models
IFOgM=super
IFOgS=None
IFOgW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  IFOgM(LambdaLayer,self).__init__(arn)
  self.cwd=IFOgS
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.IFOgW.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(RDSDatabase,self).__init__(IFOgW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(RDSCluster,self).__init__(IFOgW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(AppSyncAPI,self).__init__(IFOgW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(AmplifyApp,self).__init__(IFOgW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(ElastiCacheCluster,self).__init__(IFOgW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(TransferServer,self).__init__(IFOgW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(CloudFrontDistribution,self).__init__(IFOgW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,IFOgW,env=IFOgS):
  IFOgM(CodeCommitRepository,self).__init__(IFOgW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
