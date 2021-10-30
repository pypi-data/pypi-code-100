from localstack.utils.aws import aws_models
dUXBt=super
dUXBm=None
dUXBu=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dUXBt(LambdaLayer,self).__init__(arn)
  self.cwd=dUXBm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dUXBu.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(RDSDatabase,self).__init__(dUXBu,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(RDSCluster,self).__init__(dUXBu,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(AppSyncAPI,self).__init__(dUXBu,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(AmplifyApp,self).__init__(dUXBu,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(ElastiCacheCluster,self).__init__(dUXBu,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(TransferServer,self).__init__(dUXBu,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(CloudFrontDistribution,self).__init__(dUXBu,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dUXBu,env=dUXBm):
  dUXBt(CodeCommitRepository,self).__init__(dUXBu,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
