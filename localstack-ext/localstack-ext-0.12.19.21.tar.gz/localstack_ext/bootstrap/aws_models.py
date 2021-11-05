from localstack.utils.aws import aws_models
hwHlx=super
hwHlT=None
hwHlP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hwHlx(LambdaLayer,self).__init__(arn)
  self.cwd=hwHlT
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hwHlP.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(RDSDatabase,self).__init__(hwHlP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(RDSCluster,self).__init__(hwHlP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(AppSyncAPI,self).__init__(hwHlP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(AmplifyApp,self).__init__(hwHlP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(ElastiCacheCluster,self).__init__(hwHlP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(TransferServer,self).__init__(hwHlP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(CloudFrontDistribution,self).__init__(hwHlP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hwHlP,env=hwHlT):
  hwHlx(CodeCommitRepository,self).__init__(hwHlP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
