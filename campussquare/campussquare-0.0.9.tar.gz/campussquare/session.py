import os
import http.cookiejar
import requests
import bs4
import re
import threading
import time
import json
import sys
from campussquare.errors import CampusSquareFlowError

from campussquare.util import debug_response, get_flow_execution_key


class CampusSquareSession():
    def __init__(self,
                 campussquare_url: str,
                 initial_flow_execution_key: str,
                 cookies: http.cookiejar.CookieJar,
                 debug: bool = False,
                 credential_path: str = None,
                 refresh_interval_sec: int = 600) -> None:

        self.url = campussquare_url
        self.credential_path = credential_path or '.campussquare.json'
        self.debug = debug

        # setup session
        self.session = requests.Session()
        self.session.cookies = cookies

        # setup flowExecutionKey
        self.__flow_execution_keys = {}
        self._set_flow_execution_key(initial_flow_execution_key or self._load_flow_execution_key())

        # key refreshing
        topmenu_flow_execution_key = self._get_topmenu_flow_execution_key()
        self._set_flow_execution_key(topmenu_flow_execution_key, 'topmenu')

        def _refresh():
            while True:
                time.sleep(refresh_interval_sec)
                self._refresh()
        threading.Thread(target=_refresh, daemon=True).start()

    def _set_flow_execution_key(self, key, namespace='default'):
        self.__flow_execution_keys[namespace] = key or ''
        with open(self.credential_path, 'wt', encoding='utf-8') as f:
            json.dump(self.__flow_execution_keys, f, indent=4)

    def get_flow_execution_key(self, namespace='default'):
        return self.__flow_execution_keys.get(namespace)

    def _load_flow_execution_key(self):
        if os.path.exists(self.credential_path):
            with open(self.credential_path, 'rt', encoding='utf-8') as f:
                obj = json.load(f)
            flow_execution_key = obj.get('default')
            if not flow_execution_key:
                raise RuntimeError('default flowExecutionKey not found')
            return flow_execution_key
        else:
            raise RuntimeError('credential file not found')

    def do_get(self, url: str, namespace='default'):
        res = self.session.get(url, headers={
            'Referer': f'{self.url}?_flowExecutionKey={self.get_flow_execution_key(namespace)}'
        })

        # update flowExecutionKey
        self._set_flow_execution_key(get_flow_execution_key(
            res.url) or self.get_flow_execution_key(namespace), namespace)

        self.debug and debug_response(res)

        return res

    def do(self, data={}, namespace='default', method: str = 'post'):
        res = self.session.post(self.url, data=data, headers={
            'Referer': f'{self.url}?_flowExecutionKey={self.get_flow_execution_key(namespace)}'
        })

        # update flowExecutionKey
        self._set_flow_execution_key(get_flow_execution_key(res.url) or self.get_flow_execution_key(namespace), namespace)

        # error check
        doc = bs4.BeautifulSoup(res.text, 'html.parser')
        if doc.select_one('title').text == 'SYSTEM ERROR':
            raise CampusSquareFlowError()

        self.debug and debug_response(res)

        return res

    def _refresh(self):
        print('refreshing key...', file=sys.stderr)
        res = self.do({
            '_eventId': 'extendSession',
            '_flowExecutionKey': self.get_flow_execution_key('topmenu'),
        }, namespace='topmenu')

    def _get_topmenu_flow_execution_key(self):
        url = f'{self.url}?_flowId=USW0009210-flow'
        res = self.session.get(url)
        regex = re.compile('document\.TopForm\._flowExecutionKey\.value = "([^"]+)";')
        topmenu_flow_execution_key = regex.findall(res.text)[0]
        return topmenu_flow_execution_key

    def logout(self):
        data = {'_flowId': 'USW0009100-flow'}
        raise NotImplementedError()
