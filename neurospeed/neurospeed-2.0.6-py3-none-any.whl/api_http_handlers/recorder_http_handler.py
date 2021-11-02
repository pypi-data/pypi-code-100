# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:45:53 2021

@author: Eli Shamis
"""

from neurospeed.utils.http_service import HttpService

class UserRoom_Recorder_Handler:
    
    def __init__(self, customer_auth_handler):
        # create recorder http api instance
        self._recorder_api = self.Recorder_HttpApi(customer_auth_handler)
        
    # there can only be one recorder at a time per USER.
    # previous active recorder must be stopped in order to create another one
    # data still can be exported from stopped recorder, but recorder itself cannot be activated again
    def create_recorder(self, username):
        create_recorder = {
            "username": username,
        }
        response = self._recorder_api.create_recorder(create_recorder)
        
        return response
    
    def update_recorder(self, recorder_id, status):
        update_recorder_payload = {
            "status": status,
        }
        params  = {"id": recorder_id} 
        response = self._recorder_api.update_recorder(params, update_recorder_payload)
        
        return response
    
    def list_recorders(self, username ):
        params  = {
            "username": username
        }
        response = self._recorder_api.list_recorders(params)
        return response
    
    def get_recorder(self, recorder_id):
        response = self._recorder_api.get_recorder(recorder_id)
        
        return response
        
    def delete_recorder(self, recorder_id):
        params  = {
            "recorder_id": recorder_id
        }
        response = self._recorder_api.delete_recorder(params)
        return response
        
        
    class Recorder_HttpApi:
        
        def __init__(self, auth_handler):
            self._recorder_endpoint = '/gateway/recorder'
            self._http_service = HttpService()
            
            self._headers =  {
                "Authorization": "Bearer " + auth_handler.get_access_token()
            }
            
        def create_recorder(self, payload):
            endpoint = self._recorder_endpoint
            response = self._http_service.POST_request(endpoint, payload, self._headers)
            
            return response
        
        def update_recorder(self, params, payload):
            endpoint = self._recorder_endpoint
            response = self._http_service.PUT_request(endpoint, payload, params, self._headers )
            
            return response
        
        def list_recorders(self, params ):
            endpoint = self._recorder_endpoint
            response = self._http_service.GET_request(endpoint, params, self._headers)
            
            return response
        
        def get_recorder(self, recorder_id):

            endpoint = self._recorder_endpoint + "/" + str(recorder_id)
            response = self._http_service.GET_request(endpoint, {}, self._headers)
            
            return response
            
        def delete_recorder(self, params):
            endpoint = self._recorder_endpoint
            response = self._http_service.DELETE_request(endpoint, params, self._headers)
            
            return response