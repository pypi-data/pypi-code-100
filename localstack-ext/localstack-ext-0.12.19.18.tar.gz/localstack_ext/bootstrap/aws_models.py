from localstack.utils.aws import aws_models
EOyru=super
EOyra=None
EOyri=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EOyru(LambdaLayer,self).__init__(arn)
  self.cwd=EOyra
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EOyri.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(RDSDatabase,self).__init__(EOyri,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(RDSCluster,self).__init__(EOyri,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(AppSyncAPI,self).__init__(EOyri,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(AmplifyApp,self).__init__(EOyri,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(ElastiCacheCluster,self).__init__(EOyri,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(TransferServer,self).__init__(EOyri,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(CloudFrontDistribution,self).__init__(EOyri,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EOyri,env=EOyra):
  EOyru(CodeCommitRepository,self).__init__(EOyri,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
