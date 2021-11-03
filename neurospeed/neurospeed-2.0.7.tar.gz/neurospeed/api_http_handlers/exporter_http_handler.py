# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:02:51 2021

@author: Eli Shamis
"""

import json
import copy
from neurospeed.utils.http_service import HttpService


class UserRoom_Recorder_Exporter_Handler:
    
    def __init__(self, customer_auth_handler):
        # create exporter http api instance
        self._exporter_api = self.Exporter_HttpApi(customer_auth_handler)
        
    def create_exporter(self, recorder_id, config):
        create_exporter_payload = {
            "recorder_id": recorder_id,
            "exporter_config": config
        }
        payload_json = json.dumps(create_exporter_payload)
        response = self._exporter_api.create_exporter(payload_json)
        
        return response
    
    def get_exported_url(self, exporter_id):
        params  = {
            "exporter_id": exporter_id
        }
        response = self._exporter_api.get_exported_url(params)
        
        return response
    
    def list_exporters(self, username):
        params  = {
            "username": username
        }
        response = self._exporter_api.list_exporters(params)
        return response
    
    def get_exporter(self, exporter_id):
        response = self._exporter_api.get_exporter(exporter_id)
        
        return response
        
    def delete_exporter(self, exporter_id):
        params  = {
            "exporter_id": exporter_id
        }
        response = self._exporter_api.delete_exporter(params)
        return response
        
    class Exporter_HttpApi:
        
        def __init__(self, auth_handler):
            # create http service instance
            self._exporter_endpoint = '/gateway/exporter'
            self._http_service = HttpService()
            self._headers =  {
                "Authorization": "Bearer " + auth_handler.get_access_token()
            }
            
            
        def create_exporter(self, payload):
            endpoint = self._exporter_endpoint
            headers_copy = copy.deepcopy(self._headers)
            headers_copy["content-type"] = "application/json"
            response = self._http_service.POST_request(endpoint, payload, headers_copy )
            
            return response
        
        def list_exporters(self, params ):
            endpoint = self._exporter_endpoint
            response = self._http_service.GET_request(endpoint, params, self._headers)
            
            return response
    
        def get_exported_url(self, params):
            endpoint = self._exporter_endpoint + "/url"

            response = self._http_service.GET_request(endpoint, params , self._headers)
            
            return response
        
        def get_exporter(self, exporter_id):
            endpoint = self._exporter_endpoint + "/" + str(exporter_id)
            response = self._http_service.GET_request(endpoint, {}, self._headers)
            
            return response
            
        def delete_exporter(self, params):
            endpoint = self._exporter_endpoint
            response = self._http_service.DELETE_request(endpoint, params, self._headers)
            
            return response