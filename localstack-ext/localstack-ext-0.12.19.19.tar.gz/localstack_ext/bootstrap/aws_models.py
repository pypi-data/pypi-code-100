from localstack.utils.aws import aws_models
okjnW=super
okjnM=None
okjnA=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  okjnW(LambdaLayer,self).__init__(arn)
  self.cwd=okjnM
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.okjnA.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(RDSDatabase,self).__init__(okjnA,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(RDSCluster,self).__init__(okjnA,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(AppSyncAPI,self).__init__(okjnA,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(AmplifyApp,self).__init__(okjnA,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(ElastiCacheCluster,self).__init__(okjnA,env=env)
class TransferServer(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(TransferServer,self).__init__(okjnA,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(CloudFrontDistribution,self).__init__(okjnA,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,okjnA,env=okjnM):
  okjnW(CodeCommitRepository,self).__init__(okjnA,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
