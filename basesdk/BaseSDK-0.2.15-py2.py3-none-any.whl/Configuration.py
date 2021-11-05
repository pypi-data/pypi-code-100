from BaseSDK.Utils import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self, context):
        if context == 'dev':
            self.url = 'http://192.168.0.111:31585/base-api'

        if context == 'dev-k8s':
            self.url = 'http://apisix-gateway-headless.apisix:9080/base-api'