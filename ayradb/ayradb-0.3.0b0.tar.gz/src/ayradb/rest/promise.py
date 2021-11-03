__all__ = ['Promise']

import time
from dataclasses import dataclass
from threading import Lock

from ayradb.rest.http.request import Request
from ayradb.rest.http.response import Response

WAIT_SLEEP = 0.00001 #10us

@dataclass
class Promise:

    __id_count = 0
    __lock = Lock()

    _req: Request
    res_method: type(lambda x:Response)
    informational_msgs: []
    lock: Lock

    def __init__(self,request,build:type(lambda x:Response)):
        self._req=request
        Promise.__lock.acquire()
        self.cID = Promise.__id_count
        Promise.__id_count+=1
        Promise.__lock.release()
        self._res = None
        self.res_method=build
        self.informational_msgs=[]
        self.lock=Lock()

    def get_request(self):
        return self._req
    
    def wait_response(self):
        self.lock.acquire()
        while self._res is None:
            self.lock.release()
            time.sleep(WAIT_SLEEP)
            self.lock.acquire()
        self.lock.release()
        return self._res

    def submit(self,response):
        self.lock.acquire()
        self._res = self.res_method(response)
        self.lock.release()

    def submit_informational(self,response):
        self.informational_msgs.append(response)

    @staticmethod
    def reject(error_object):
        promise = Promise(None, None)
        promise._res=error_object
        return promise
