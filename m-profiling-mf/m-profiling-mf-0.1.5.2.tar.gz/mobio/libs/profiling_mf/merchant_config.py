import requests
# from mobio.libs.Singleton import Singleton
from mobio.libs.profiling_mf import CommonMerchant


# @Singleton
class MerchantConfig:
    JWT_SECRET_KEY = 'jwt_secret_key'
    JWT_ALGORITHM = 'jwt_algorithm'
    PROFILING_HOST = 'profiling_host'
    PROFILING_TOKEN = 'p_t'

    def __init__(self):
        self.configs = {}
        self.current_merchant = ''

    def get_merchant_config(self, merchant_id):
        if merchant_id not in self.configs:
            result = self.__request_get_merchant_auth(merchant_id)
            if result:
                self.configs[merchant_id] = result
        return self.configs[merchant_id]

    def __request_get_merchant_auth(self, merchant_id):
        adm_url = CommonMerchant.ADMIN_HOST + '/adm/v1.0/merchants/{}/configs'
        adm_url = adm_url.format(merchant_id)
        response = requests.get(adm_url)
        response.raise_for_status()

        result = response.json()

        profiling_host = result['data']['profiling_host']
        if profiling_host.endswith('/'):
            profiling_host = profiling_host[:-1]
        return {
            MerchantConfig.JWT_ALGORITHM: result['data']['jwt_algorithm'],
            MerchantConfig.JWT_SECRET_KEY: result['data']['jwt_secret_key'],
            MerchantConfig.PROFILING_HOST: profiling_host,
            MerchantConfig.PROFILING_TOKEN: 'Basic ' + result['data']['p_t']

        }

    def set_current_merchant(self, merchant_id):
        self.get_merchant_config(merchant_id)
        if merchant_id != self.current_merchant:
            self.current_merchant = merchant_id

    def get_current_config(self):
        if not self.current_merchant:
            raise Exception("Please set merchant first")
        return self.configs[self.current_merchant]
