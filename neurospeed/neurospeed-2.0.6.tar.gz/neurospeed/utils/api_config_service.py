

from neurospeed.utils.helper_service import UtilService as utils
from pathlib import Path
import os

class ApiConfig:

    def __init__(self):
        self._contex = "ApiConfig - "
        self._config_path =  os.path.join(str(Path(__file__).parent.parent) ,"config","api_config.json")
        self._api_config = utils.load_config_file(self._config_path)
        self._api_http_url =  self._api_config["api_address_prod"]  if self._api_config["is_prod"] == "True"  else  self._api_config["api_address_local"] 
        self._pipeline_url =  self._api_config["pipeline_address_prod"]  if self._api_config["is_prod"] == "True"  else  self._api_config["pipeline_address_local"] 
        
       # print("{} NeuroSpeed API HTTP URL: {} ".format(self._contex, self._api_http_url))
       # print("{} NeuroSpeed API SOCKET URL: {} ".format(self._contex, self._pipeline_url))
        
    def get_http_url(self):
        return self._api_http_url
    
    def get_socket_url(self):
        return self._pipeline_url
        