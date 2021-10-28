""" Method to invoke http API"""
import requests

def call_python_api(http_url, process_name, data_input):
    """ Receive json input and send it to FastAPI, then return json result """
    header_input = {}
    header_input["Content-Type"] = "application/json"
    response_from_api = requests.post(http_url+process_name,
        headers = header_input,
        timeout = 15,
        json = data_input
        )   
    return response_from_api.json()