from localstack.utils.aws import aws_models
GuRqP=super
GuRqM=None
GuRqW=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GuRqP(LambdaLayer,self).__init__(arn)
  self.cwd=GuRqM
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GuRqW.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(RDSDatabase,self).__init__(GuRqW,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(RDSCluster,self).__init__(GuRqW,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(AppSyncAPI,self).__init__(GuRqW,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(AmplifyApp,self).__init__(GuRqW,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(ElastiCacheCluster,self).__init__(GuRqW,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(TransferServer,self).__init__(GuRqW,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(CloudFrontDistribution,self).__init__(GuRqW,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GuRqW,env=GuRqM):
  GuRqP(CodeCommitRepository,self).__init__(GuRqW,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
