__all__ = ['RestManager']

import time
from dataclasses import dataclass
from queue import Queue, Empty
from threading import Thread, Lock, Condition

from ayradb.rest.http.response import Response, Header
from ayradb.rest.promise import Promise
from ayradb.rest.socket.wrapper import CherrySocketWrapper
from ayradb.utils.singleton import Singleton

DISCONNECTION_TIME = 8 # 10 seconds -> keep 2 second margin

@dataclass
class RestManager(metaclass=Singleton):

    _MAX_CONN=1
    _MAX_CONN_ON_NODE=1

    _SLEEP_EMPTY_QUEUE_SEC =0.00001 # 10us
    _SLEEP_TCP_BUFFER_EMPTY = 0.00001 # 10us

    _MIN_NON_INFO_STATUS_CODE=200

    threads: list
    lock: Lock
    condition: Condition
    queue: Queue
    process: bool
    connections: int
    conn_on_node:dict

    def __init__(self):
        self.process=False
        self.queue=Queue()
        self.lock=Lock()
        self.connections=0
        self.condition=Condition(lock=self.lock)
        self.threads=[]
        self.conn_on_node={}
    
    def connect(self, ip, port = None):
        self.lock.acquire()
        connections = self.conn_on_node.get(ip)
        if self.connections<RestManager._MAX_CONN and\
            (connections is None or connections<RestManager._MAX_CONN_ON_NODE):
            # A new connection can be stablished
            self.connections += 1
            if connections is None:
                # Add node to connection list
                self.conn_on_node[ip]=1
            else: 
                # Increment node connections
                self.conn_on_node[ip]=connections+1
            self.lock.release()
            curr_th = Thread(target=self._process_data_exchange, args=(ip,port,))
            curr_th.start()
            self.threads.append(curr_th)
            with self.condition:
                while not self.process:
                    # Wait for thread connection setup
                    self.condition.wait()
        else:
            self.lock.release()

    def is_connected(self):
        self.lock.acquire()
        is_processing = self.process
        self.lock.release()
        return is_processing
    
    def stop_processing(self):
        self.lock.acquire()
        self.process = False
        self.lock.release()

    def _process_data_exchange(self,ip, port = None):
        thread_ip=ip
        # Open connection to cherry table
        socket = None
        if port is None:
            socket = CherrySocketWrapper(ip)
        else:
            socket = CherrySocketWrapper(ip, port=port)
        # Create buffer for response bytes
        res_buffer= b''
        # Last message sent time
        last_sent_time = time.time()

        # Start processing incoming requests
        continue_processing=True
        with self.condition:
            self.process=continue_processing
            # Notify main thread that socket thread is
            # ready to process requests
            self.condition.notify()
        while continue_processing:
            # Main thread didn't request to stop processing
            try:
                while 1:
                    # Process every message in queue (until it's empty)
                    promise = self.queue.get(block=False)
                    # Send request to ayra
                    request = promise.get_request()
                    request.upsert_header(Header.HOST, thread_ip)
                    socket.write(request.to_byte_array())
                    last_sent_time = time.time()
                    response_parsed = False
                    res = Response()
                    last_read_len = 0
                    while not response_parsed:
                        # Parse responses related to request sent
                        res_buffer += socket.read_available_bytes()
                        curr_read_len = res_buffer.__len__()
                        if curr_read_len == last_read_len:
                            # No new bytes -> sleep
                            time.sleep(RestManager._SLEEP_TCP_BUFFER_EMPTY)
                        else:
                            last_read_len = curr_read_len
                        bytes_read = res.from_byte_array(res_buffer)
                        if bytes_read > 0:
                            # Response found in buffer
                            if last_read_len > bytes_read:
                                res_buffer = res_buffer[bytes_read:last_read_len]
                            else:
                                res_buffer = b''
                            # Update buffer length of current read
                            last_read_len = res_buffer.__len__()
                            if res.status_code >= RestManager._MIN_NON_INFO_STATUS_CODE:
                                # Case non informational response [>=200]
                                promise.submit(res)
                                response_parsed = True
                            else:
                                # Case informational response [1xx]
                                promise.submit_informational(res)
                                res = Response()
            except Empty:
                # Queue is empty
                self.lock.acquire()
                # Check if we should stop processing
                continue_processing = self.process
                self.lock.release()
                if time.time()-last_sent_time > DISCONNECTION_TIME:
                    socket = CherrySocketWrapper(ip)
                    last_sent_time=time.time()
                if continue_processing:
                    time.sleep(RestManager._SLEEP_EMPTY_QUEUE_SEC)

        socket.close()
        return True

    def submit(self, request,build:type(lambda x:Response)):
        # Add connection keep-alive to keep socket open
        request.upsert_header(Header.CONNECTION, "Keep-Alive")
        # submit to connection thread
        promise = Promise(request,build)
        self.queue.put(promise)
        return promise