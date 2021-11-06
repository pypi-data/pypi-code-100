import json
import requests
import threading
from .setting import Base

api_list = {
    'request': '/request/store/',
    'exception': '/exception/store/',
    'request_update': '/request/edit/',
}


def reqApi(data, type, config=None):
    try:
        if not Base.is_valid():
            return
        if not api_list[type]:
            return

        data['token'] = Base.api_key
        data['project'] = Base.project_key
        url = Base.server_url+api_list[type]
        data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        if config and config['pk']:
            url += str(config['pk'])+'/'
        threading.Thread(
            target=reqApiBase,
            args=(url, data, headers)
        ).start().join()
        return
    except:
        pass


def reqApiBase(url, data, headers):
    try:
        requests.post(url, data=data, headers=headers, timeout=1)
    except:
        pass
