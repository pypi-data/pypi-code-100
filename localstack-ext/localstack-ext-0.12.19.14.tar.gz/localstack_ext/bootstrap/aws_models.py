from localstack.utils.aws import aws_models
puOdv=super
puOdI=None
puOdU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  puOdv(LambdaLayer,self).__init__(arn)
  self.cwd=puOdI
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.puOdU.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(RDSDatabase,self).__init__(puOdU,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(RDSCluster,self).__init__(puOdU,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(AppSyncAPI,self).__init__(puOdU,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(AmplifyApp,self).__init__(puOdU,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(ElastiCacheCluster,self).__init__(puOdU,env=env)
class TransferServer(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(TransferServer,self).__init__(puOdU,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(CloudFrontDistribution,self).__init__(puOdU,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,puOdU,env=puOdI):
  puOdv(CodeCommitRepository,self).__init__(puOdU,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
