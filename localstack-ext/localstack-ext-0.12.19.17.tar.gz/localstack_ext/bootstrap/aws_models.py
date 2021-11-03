from localstack.utils.aws import aws_models
QBdzE=super
QBdzT=None
QBdzf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  QBdzE(LambdaLayer,self).__init__(arn)
  self.cwd=QBdzT
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.QBdzf.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(RDSDatabase,self).__init__(QBdzf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(RDSCluster,self).__init__(QBdzf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(AppSyncAPI,self).__init__(QBdzf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(AmplifyApp,self).__init__(QBdzf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(ElastiCacheCluster,self).__init__(QBdzf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(TransferServer,self).__init__(QBdzf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(CloudFrontDistribution,self).__init__(QBdzf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,QBdzf,env=QBdzT):
  QBdzE(CodeCommitRepository,self).__init__(QBdzf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
