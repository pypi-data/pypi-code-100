#!/usr/bin/env python3
'''
Copyright (C) 2020-2022 John Landers

This program is free software: you can redistribute it and/or modify it under the terms of the 
GNU General Public License as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even 
the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
'''

# This now just imports requests under the assumption that you have included this in your package.
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import json
import uuid
import time

import queue as Queue
import threading
import sys

import resource

class splunk_hec:
    '''
    Init Variables
        token                               The HEC token to use
        hec_server                          The server FQDN or IP address to connect to
        hec_port                            HEC port
        input_type                          raw/json; This tells the library which endpoint to use. Functionality is the same otherwise.
        use_hec_tls                         True/False; Set to False to use http connections instead of https
        use_ack                             True/False; Set to True to enforce acknowledgment
        hec_tls_verify                      True/False; Set to True to verify the remote TLS certificate
        ack_interval                        Integer; Time to wait between ACK checks
        max_ack_attempts                    Integer; Number of ack attempts to make. Also controls how many overall send attempts to make.
        max_content_length                  Integer; Maximum estimated payload size before sending a batch of events
        max_events_per_batch                Integer; Maximum number of events to send in a batch
        backup_queue                        Queue; If a queue is provided, any events that fail to send will be placed on this queue for the caller to process
        context_id                          String; Used for log messages to associate typically to the lambda request id
        rotate_session_after                Integer; It's possible to establish a long session in this lib. This will rotate the session after X attempts to prevent sending all data to a single indexer
        debug_enabled                       True/False; Enable or disable debug level logging
        logger                              Object; Pass in a logger object if you have a preferred logging mechanism
        max_threads                         Integer; 0 disables threading. Anything else will attempt to create X number of subthreads
        disable_tls_validation_warnings     True/False; disable those pesky TLS validation warnings that we should care about but often don't
        http_timeout                        Integer; HTTP Timeout setting. Default: 60

    '''
    def __init__(self, token, hec_server, hec_port='8088', input_type='raw', use_hec_tls=True, 
        use_ack=False, hec_tls_verify=True, ack_interval=5, max_ack_attempts=5, 
        max_content_length=50000000, max_events_per_batch=100000, backup_queue=None, context_id='default', 
        rotate_session_after=10, debug_enabled=False, logger=None,  max_threads=0, 
        disable_tls_validation_warnings=True, http_timeout=60, max_memory=0 ):

        # Moved this here to make it configurable by the calling application.
        if disable_tls_validation_warnings:
            try:
                # Try to disable these warnings because it adds log clutter that we probably don't want.
                requests.packages.urllib3.disable_warnings()
            except:
                # In case of failure, who cares about the clutter?
                pass
 
        # Initialize core settings expected to be passed in by the calling app
        self.token = token
        self.hec_server = hec_server
        self.hec_port = str(hec_port)
        self.input_type = str(input_type).lower()
        self.hec_tls_verify = self.normalize_str_to_bool(hec_tls_verify)
        self.use_hec_tls = self.normalize_str_to_bool(use_hec_tls)
        self.max_content_length = int(max_content_length)
        self.max_events_per_batch = int(max_events_per_batch)
        self.backup_queue = backup_queue
        self.context_id = str(context_id)
        self.rotate_session_after = rotate_session_after
        self.debug_enabled = self.normalize_str_to_bool(debug_enabled)
        self.use_ack = self.normalize_str_to_bool(use_ack)
        self.http_timeout = int(http_timeout)
        self.ack_interval = int(ack_interval)
        self.current_mem_usage = 0

        # This is named "ack" but it's also used to define the maximum attempts we make to send a data payload.
        self.max_ack_attempts = int(max_ack_attempts)
       
        # Handle the logger
        if logger is None:
            self.logger = None
        else:
            # I assume if you pass in a logger object, you know the format, settings, and output filename for that logger.
            self.logger = logger

        # Initialize settings we may use later
        self.http_session = None
        self.user_params = None
        self.request_params = None
        self.current_payload_length = 0
        self.current_batch_events = []
        self.http_request_count = 0

        # Set the request header based on given HEC Token
        self.request_headers = { 'Authorization': 'Splunk ' + str(self.token) }

        # If I understand the documentation correctly, using this channel identifier is required for ACK OR sending raw data
        # and it can be sent as a URL param or header item. I'm opting to use the header method here.
        if self.input_type=='raw' or self.use_ack:
            self.request_headers.update({ 'X-Splunk-Request-Channel': str(uuid.uuid1()) })
            
        if self.use_hec_tls:
            self.proto = 'https'
        else:
            self.proto = 'http'

        if self.input_type == 'json':
            endpoint = 'event'
            self.request_headers.update({'Content-Type': 'application/json; charset=utf-8'})
        else:
            self.request_headers.update({'Content-Type': 'text/plain; charset=utf-8'})
            endpoint = 'raw'                        

        # Set up the main URI
        self.server_uri = '%s://%s:%s/services/collector/%s' % (self.proto, self.hec_server, self.hec_port, endpoint)

        # Log out some debugging statements
        self.log('Library initialized. Settings to follow.', 'debug')
        self.log(('Splunk HEC Library HEC Library loaded with user vars: hec_token="%s" hec_server="%s" hec_port="%s" input_type="%s" use_ack="%s" hec_tls_verify="%s" hec_use_tls="%s"' 
            % (str(self.token), str(self.hec_server), str(self.hec_port), str(self.input_type), str(self.use_ack), str(self.hec_tls_verify), str(self.use_hec_tls))), 
            'debug')
        self.log(('Splunk HEC Library Configuration: server_uri="%s"' % str(self.server_uri)),'debug')

        # Set up the ACK URI when it's necessary to do so
        if self.use_ack:
            self.server_ack_uri = '%s://%s:%s/services/collector/ack' % (self.proto, self.hec_server, self.hec_port)
            self.log(('Splunk HEC Library Configuration: server_ack_uri="%s"' % str(self.server_ack_uri)),'debug')


        self.run_threads = False
        # finally, decide on threading
        if max_threads > 0:
            # Set this to true so it can be used later when we flush events to the HEC to determine how they are being sent.
            self.threading_enabled = True
            self.max_threads = max_threads
            self.processing_event = threading.Event()
            self.processing_event.clear()

            # This data queue is used for sending events. When a producer (wrapper script) calls send event, we just add it to a batch
            # from which our child threads monitor and process. This is important because we need to process multiple events at a time.
            #self.data_queue = Queue.Queue(0)

            # Instead of having an infinite queue, we need a limit to reduce overall memory consumption
            if self.max_threads > 5:
                q_length = self.max_threads - 1
            else:
                q_length = 4

            self.data_queue = Queue.Queue(q_length)

            # We will not create new threads at this time; wait until data actually needs to be sent... 
            self.my_child_threads = list()

        else:
            self.threading_enabled = False
            self.data_queue = None
            self.processing_event = None
            self.max_threads = 0

        self.set_max_memory(int(max_memory))

        # This is being done for tracking purposes regardless of memory settings.
        self.add_current_mem(self.get_maxrss()*1024*1024)

        ##### End of Object Init #####

    '''
    Had to move this to better support dynamic changes to setting the maximum memory. Setting maximum
    memory will override content length settings but will not override maximum event count settings
    at this time.
    '''
    def set_max_memory(self, max_memory):
        #### Testing Area -- Setting max content length based on maximum memory configurations ####
        try:
            self.max_memory = int(max_memory)
        except:
            # Effectively disable this control
            self.max_memory = 0
            self.log('Attempting to set integer for max memory failed. Ignoring.', 'error')

        if self.max_memory > 0:
            if self.max_threads > 5:
                denom = self.max_threads - 1
            else:
                denom = 4

            # Basic idea is to set limits on the max memory we can use for an in buffer queue by limiting
            # payload size. 
            multiplier = 0.65
            if self.threading_enabled:
                # 322,122,547.2  --> 80,530,636.8
                mcl = int(((self.max_memory*multiplier)*1024*1024)/denom)
            else:
                mcl = int((self.max_memory*multiplier)*1024*1024)

            # At the time of development, max content size accepted by the HEC is approx 800 MB
            # this ensures we don't exceed about 760mb, allowing for some overhead
            if mcl >= 800000000:
                mcl = 800000000

            # Set max content length to about 80% of maximum memory allowing for overhead
            self.max_content_length = mcl


    '''
    Return the resource usage for this process and all threads
    '''
    def get_maxrss(self):
        # This should return estimated memory usage in MB
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)

    '''
    Internal memory tracker methods; increase and decrease estimated memory usage
    whenever we accept a payload
    '''
    def add_current_mem(self, usage):
        self.current_mem_usage = self.current_mem_usage + usage

    def sub_current_mem(self, usage):
        self.current_mem_usage = self.current_mem_usage - usage

    def get_current_mem(self):
        # current_mem_usage should be a rough estimate in bytes; return bytes/1024/1024
        return int(self.current_mem_usage/1024/1024)

    '''
    If a logger object is passed into our class, we'll use it. Otherwise, we'll print messages that are INFO or higher. Unless, of course, the user has elected to enable debug logging.
    '''
    def log(self, message, level='info'):
        level = str(level).lower()
        if self.logger is None:
            message = '[%s] context=%s (maxrss_memory=%s MB, tracked_memory=%s MB, target_host=%s) %s' % (str(level), str(self.context_id), str(self.get_maxrss()), str(self.get_current_mem()), str(self.hec_server), str(message))
            if ('debug' in level and self.debug_enabled) or 'debug' not in level:
                print(message)
        else:
            message = 'context=%s (maxrss_memory=%s MB, tracked_memory=%s MB, target_host=%s) %s' % (str(self.context_id), str(self.get_maxrss()), str(self.get_current_mem()), str(self.hec_server), str(message))
            if 'debug' in level:
                self.logger.debug(message)
            elif 'warn' in level:
                self.logger.warning(message)
            elif 'err' in level:
                self.logger.error(message)
            elif 'critical' in level:
                self.logger.critical(message)
            else:
                self.logger.info(message)

    '''
    Standardize True/False based on input.
    '''
    def normalize_str_to_bool(self, val):
        val = str(val).lower()
        if val == '1' or val == 'true' or val == 'yes':
            return True
        else:
            return False

    '''
    Pass in a dictionary to add request params to the posting... This allows to set query params like index, source, sourcetype which may be necessary
    '''
    def set_request_params(self, params):
        if self.user_params is None:
            self.user_params = {}

        self.user_params.update(params)


    '''
    Used to invoke requests with additional Retry logic to add resilency to our POST requests. Specifically, if we encounter a 500/503 from the HEC
    this should force additional requests to occur.
    '''
    # For HEC http error codes, reference: https://docs.splunk.com/Documentation/Splunk/7.3.2/Data/TroubleshootHTTPEventCollector#Possible_error_codes
    def requests_data_send( self, retries=3, backoff_factor=0.3, status_forcelist=[500, 503], method_whitelist=['POST','GET'] ):
        # Basically, all of this setup was previously being done every time we wanted to post. It's unnecessary if we are going to keep a session
        # established beyond a single connection.
        if self.http_session is None or self.http_request_count >= self.rotate_session_after:
            self.set_http_session()     

            # total: The total number of retries to attempt (Takes precedence over other counts. So read, connect, and redirect seem unnecessary.)
            # read: The total number of retries to attempt on read errors (error occurs after data send, could result in data duplication)
            # connect: How many times to retry in the event of connection errors (error occurs before data send)
            # method_whitelist: Set of uppercased HTTP method verbs that trigger a retry. Default in urllib: frozenset(['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE'])
            # backoff_factor: A sleep is applied with formula: {backoff factor} * (2 ** ({number of total retries} - 1))
            #           -- With a backoff factor of 0.3, max retries of 5 - the max sleep time is expected to be: 0.3 + 0.6 + 1.2 + 2.4 + 4.8 = 9.3 seconds
            # status_forcelist: A set of integer HTTP status codes that we should force a retry on. 
            #         A retry is initiated if the request method is in method_whitelist and the response status code is in status_forcelist.

            # Set up retry configuration
            retry = Retry(total=retries, method_whitelist=method_whitelist, backoff_factor=backoff_factor, status_forcelist=status_forcelist)

            # Apply the retry configuration to the transport adapter interface
            adapter = HTTPAdapter(max_retries=retry)

            # Apply this configuration to all http/https calls made using this session interface
            self.http_session.mount('http://', adapter)
            self.http_session.mount('https://', adapter)

        # Always return the session
        return self.http_session


    '''
    I moved this to give the calling application the option to create a session in advance and reuse the same session
    for the life/duration of that application.
    '''
    def set_http_session(self, reset=True):
        # I updated this to have a reset flag for some possible future purpose but today, any time this is called, we assume a reset is necessary.
        if reset:
            if self.http_request_count>0:
                self.log(('context=%s Creating new http session after %s requests.' % (self.context_id, str(self.http_request_count))))
        
            self.http_request_count = 0
            self.http_session = requests.Session()
            self.http_session.headers.update(self.request_headers)


    '''
    I added this to handle event "backups" as I may choose to expand functionality later on instead of just relying on a backup queue
    '''
    def do_event_backup(self, payload):
        if self.backup_queue is not None:
            if isinstance(payload, list):
                while payload:
                    self.backup_queue.put(payload.pop(0))
            else:
                self.backup_queue.put(payload)

    '''
    The workhorse.

    We need to have data come in, be "normalized" to reduce chance of issues on send, and batch the events. When the batch reaches
    the max batch size and/or max content size, we need to send it off.

    Returns:
        * True        , if the event is believed to have been successfully added to the batch for processing
        * False       , if the event was unable to be converted to a string for adding to the payload
    '''
    def send_event(self, payload):
        # Basically, anything we bring in - we try to convert it to a string of valid utf-8 characters through a short series of encode/decode commands
        try:
            # If we get a dictionary, json dump it and make it a string and strip out non utf-8 characters
            if isinstance(payload, dict):
                payload = str(json.dumps(payload))
                payload = bytes(payload, 'utf-8').decode('utf-8', 'ignore')
    
            # If this should happen decode to a string of utf-8 characters ignoring those that couldn't be decoded
            elif isinstance(payload, bytes):
                payload = payload.decode('utf-8', 'ignore')

            # Finally, remove non utf-8 characters from a string
            elif isinstance(payload, str):
                payload = bytes(payload, 'utf-8').decode('utf-8', 'ignore')

            # Print out an error if some other type comes in...
            else:
                self.log(('ERROR: context=%s; Unexpected payload type brought into lambda. Detected type: %s. Will attempt string conversion anyways.' % (self.context_id, str(type(payload)))),'error')
                payload = bytes(str(payload), 'utf-8').decode('utf-8', 'ignore')

        except Exception as ex:
            self.log(('ERROR: context=%s; Exception occurred while trying to format the payload for sending. Dropping to backup queue. Exception: %s' % (self.context_id, str(ex))), 'error')
            self.do_event_backup(payload)

            # Returning False to indicate the data will not be sent.
            return False

        else:
            #self.log('String conversion completed. Queuing up for sending to HEC.','debug')
            # Get the rough payload length
            payload_length = len(payload)

            # Add this to the memory tracker mechanism
            self.add_current_mem(payload_length)

            ## Test the total length and if it would be more than the max content length, take the current stored payload and send it off for realsies.
            if ( self.current_payload_length + payload_length ) >= self.max_content_length:
                #self.log('Existing batch events + current payload length would be beyond the max_content_length. Flushing.', 'debug')
                self.force_flush_events()

                self.current_batch_events.append(payload)
                self.current_payload_length = payload_length

            else:
                ## Add it to the list of pending sends!
                self.current_batch_events.append(payload)
                self.current_payload_length += payload_length

            ## Test the number of events waiting to be sent if we met the threshold, send it for realsies.
            ## But only do this if max_memory is not in play because if max_memory is in play
            ## then we are adjusting the size of the payload based on this value
            if self.max_memory == 0:
                if len(self.current_batch_events) >= self.max_events_per_batch:
                    #self.log('Max events per batch met. Flushing pending events to HEC.','debug')
                    self.force_flush_events()

            return True

        return True

    '''
    This function serves as a router, essentially. Whenever it's called, we make an evaluation:
    is this multithreaded? Is ACK enabled? 
    '''
    def force_flush_events(self):
        # In some cases, this can be called when there isn't anything pending - so this avoids that issue...
        if len(self.current_batch_events)>0:
            self.log(('Queue flush requested. num_events_in_request=%s, estimated_payload_length=%s' % (str(len(self.current_batch_events)), str(self.current_payload_length))))

            # Threading enabled - do additional checks to make sure we have threads running to process the data
            if self.threading_enabled:
                # Thread count, from our perspective, is the number of active threads minus the baseline number of threads when
                # this library started.
                thread_count = len(self.my_child_threads)
                queue_length = self.data_queue.qsize()
                self.log('Current active thread count: %s; Queue length: %s' % (str(thread_count), str(queue_length)), 'debug')

                # First check: Do we have more than the parent thread? We expect the thread count to always be >=1 when multi-threading is in use
                if thread_count < 1:
                    self.run_threads = True

                    thread_created = self.create_child_thread()

                    if thread_created:
                        self.log('Successfully created first child thread.', 'debug')
                    else:
                        self.log('Unable to create the first child thread. Disabling multithreading. Sending data from the parent thread instead and disabling multithreading.', 'error')
                        self.threading_enabled = False
                        if self.use_ack:
                            return_val = self.force_flush_with_ack(self.current_batch_events)
                        else:
                            return_val = self.force_flush_no_ack(self.current_batch_events)

                        # Clean up and return
                        self.sub_current_mem(self.current_payload_length)
                        self.current_batch_events = []
                        self.current_payload_length = 0

                        return return_val

                # Second check: Increase the thread count if the number of pending items in the data queue is higher than the max thread count
                if queue_length > thread_count and thread_count < self.max_threads:
                    thread_created = self.create_child_thread( True )
                    if thread_created:
                        self.log('Successfully created a new thread.', 'debug')


                # Third check: We have the maximum number of threads
                if thread_count >= self.max_threads and queue_length > thread_count:
                    self.log('Performing a thread check to ensure our sending threads are still alive.', 'debug')
                    self.do_thread_check()

                # Set the processing event so the thread can go because we're about to add to the queue
                self.processing_event.set()

                
                '''
                Add data to a queue. Let the thread processor figure out what to do with it.

                Based on the current setup, this call will block execution if the queue is full which shouldn't be
                a problem if the threads are running and able to send data as expected. Doing this will ensure
                that we do not put an infinite amount of data on the queue driving memory utilization upwards.
                '''
                self.data_queue.put(self.current_batch_events)

                return_val = True
            else:
                if self.use_ack:
                    return_val = self.force_flush_with_ack(self.current_batch_events)
                else:
                    return_val = self.force_flush_no_ack(self.current_batch_events)

            # Clean up and return
            self.sub_current_mem(self.current_payload_length)
            self.current_batch_events = []
            self.current_payload_length = 0

            return return_val
     
        else:
           # self.log('Force flush called but no events available to send. Ignoring.','debug')
            return True

    '''
    This should create a child thread for sending data; the threads do nothing more than monitor a shared queue and 
    '''
    def create_child_thread(self, use_thread_breaker=False):
        # This is meant to be a secondary check so we don't go crazy with threads
        if len(self.my_child_threads) >= self.max_threads:
            self.log('Will not attempt to create a new thread because maximum thread count reached already.', 'error')
            return False
        else:
            try:
                t = threading.Thread(target=self.thread_processor, args=[use_thread_breaker])
                t.start()

                # We'll keep a reference to the thread around so it can be checked directly later
                self.my_child_threads.append(t)
                return True
            except Exception as ex1:
                self.log('Exception caught while starting threads. Exception: %s' % ex1, 'error' )
                return False

        # Assume failure
        return False

    '''
    The goal of this method is to loop through each of our created child threads and ensure it is still active. If it is not
    active, remove it from the tracking list.
    '''
    def do_thread_check(self):
        new_thread_list = list()

        while self.my_child_threads:
            thread = self.my_child_threads.pop(0)
            try:
                if thread.is_alive():
                    new_thread_list.append(thread)
                    self.log('Thread %s is alive.' % (str(thread.name)), 'debug')
                else:
                    self.log('Thread %s is dead. Clearing from list.' % (str(thread.name)), 'error')
            except Exception as ex1:
                self.log('Exception caught while checking threads. Exception: %s. ' % ex1, 'error' )

        # We've successfully checked all the threads so now we store them again
        self.my_child_threads = new_thread_list

        # If we're left with 0 active threads, we need to create a new one to make sure data flows
        if len(self.my_child_threads) == 0:
            self.log('Thread checking resulted in 0 alive threads. Starting a new thread.', 'error')
            self.create_child_thread()
        


    '''
    This allows the calling application to send batched events at any time. Additionally, this is how we are going to send batched
    events as well.

    Returns:

        True                , data was sent successfully (HEC post returned 200)
        False               , data was not sent (HEC did not return 200) after multiple attempts
    '''
    def force_flush_no_ack(self, payload_list):
        #self.log('Clearing out the batched payload. Sending to HEC.','debug')

        # Send it to the HEC
        data_attempt_counter = 0
        data_sent = False

        # This loop attends to send the data up to max_ack_attempts times.
        while not data_sent and data_attempt_counter < self.max_ack_attempts:
            # Get the request parameters, if any have been provided
            if self.request_params is not None and self.user_params is not None:
                initial_request_params = self.request_params
                initial_request_params.update(self.user_params)
            elif self.request_params is None and self.user_params is not None:
                initial_request_params = self.user_params
            elif self.user_params is None and self.request_params is not None:
                initial_request_params = self.request_params
            else:
                initial_request_params = None                

            # We will now make an attempt to send the data

            # This number is used for this individual payload and does not persist across sessions. It increases until it hits the max
            # attempts number and then we are done with this individual payload
            data_attempt_counter += 1

            try:
                self.log('Measurement: context={}, attempt_no={}, payload_length={}'.format(self.context_id, str(data_attempt_counter), len(payload_list)) )
                # Note: the data body is a newline separated byte string. The point of the byte object
                # is to control the encoding. We want utf-8, not latin-1.
                r = self.requests_data_send().post(self.server_uri, 
                    params=initial_request_params, 
                    data=('\n'.join(payload_list)).encode('utf-8'), 
                    verify=self.hec_tls_verify,
                    timeout=self.http_timeout)
                
                # This number can persist across payloads depending on the "rotate_after_x" value so while it may seem similar to the data_attempt_counter
                # it serves a different function
                self.http_request_count += 1
            except Exception as ex:
                self.log(('ERROR: context=%s; Exception occurred while trying to send data to HEC. Exception: %s' % (self.context_id, str(ex))),'error')
                self.set_http_session()
            else:
                if r.status_code == requests.codes.ok:
                    data_sent = True
                else:
                    self.log(('ERROR: context=%s; Unable to send payload to HEC. Status code: %s. Creating new session.' % (self.context_id, str(r.status_code))),'error')
                    self.log(('ERROR: context=%s; Status text: %s.' % (self.context_id, str(r.text))),'error')
                    # Also create a new session here
                    self.set_http_session()

                    # Remove bad messages
                    if str(r.status_code) == '400':
                        try:
                            response = json.loads(r.text)
                            if 'invalid-event-number' in response:
                                invalid_event = response['invalid-event-number']
                                if type(invalid_event) != list:
                                    invalid_event = [ invalid_event ]

                                for i in invalid_event:
                                    invalid_msg = payload_list.pop(i)
                                    self.log(('Invalid message removed from processing: %s') % (json.dumps(invalid_msg)), 'error')
                        except:
                            # Do nothing here on error.
                            pass


        # Check for data send success
        if data_sent:
            # Data was sent, record the measurement; this isn't really necessary when data fails to send
            # because we expect to push it out to a backup method which is presently defined by the caller.
            self.log(('Measurement: Request sucessfully sent. send_attempts_required=%s, context=%s' % (str(data_attempt_counter), self.context_id)))
            return_value = True
        else:
            self.log(('ERROR: context=%s; Detected error sending batch of events. Sending events to backup function.' % (self.context_id)),'error')
            self.do_event_backup(payload_list)

            return_value = False

        return return_value


    '''
    This allows the calling application to send batched events at any time. Additionally, this is how we are going to send batched
    events as well. This version uses ACK to confirm delivery of events.

    Returns:

        True                , data was sent successfully (HEC post returned 200)
        False               , data was not sent (HEC did not return 200) after multiple attempts
    '''
    def force_flush_with_ack(self, payload_list):
        #self.log('Clearing out the batched payload. Sending to HEC.','debug')

        # Send it to the HEC
        data_attempt_counter = 0
        data_sent = False

        # This loop attends to send the data up to max_ack_attempts times.
        while not data_sent and data_attempt_counter < self.max_ack_attempts:

            # Create a session if one has not already been created
            # or rotate as necessary
            if self.http_session is None or self.http_request_count >= self.rotate_session_after:
                self.set_http_session()                

            # Get the request parameters, if any have been provided
            if self.request_params is not None and self.user_params is not None:
                initial_request_params = self.request_params
                initial_request_params.update(self.user_params)
            elif self.request_params is None and self.user_params is not None:
                initial_request_params = self.user_params
            elif self.user_params is None and self.request_params is not None:
                initial_request_params = self.request_params
            else:
                initial_request_params = None                

            # We will now make an attempt to send the data

            # This number is used for this individual payload and does not persist across sessions. It increases until it hits the max
            # attempts number and then we are done with this individual payload
            data_attempt_counter += 1

            try:
                # Note: the data body is a newline separated byte string. The point of the byte object
                # is to control the encoding. We want utf-8, not latin-1.
                r = self.requests_data_send().post(self.server_uri, 
                    params=initial_request_params, 
                    data=('\n'.join(payload_list)).encode('utf-8'), 
                    verify=self.hec_tls_verify,
                    timeout=self.http_timeout)
                
                # This number can persist across payloads depending on the "rotate_after_x" value so while it may seem similar to the data_attempt_counter
                # it serves a different function
                self.http_request_count += 1
            except Exception as ex:
                self.log(('ERROR: context=%s; Exception occurred while trying to send data to HEC. Exception: %s' % (self.context_id, str(ex))),'error')
            else:
                # First make sure we got a 200 indicating everything is going well.
                if r.status_code == requests.codes.ok:
                    # Load the response data from our initial data sending
                    try:
                        response_data = json.loads(r.text)
                    except Exception as ex2:
                        self.log(('ERROR: context=%s; Unable to load ACK response from HEC. Data will be sent again likely causing duplicates. Exception: %s' % (self.context_id, str(ex2))),'error')
                    else:
                        if 'success' in str(response_data['text']).lower():
                            ack_attempt_counter = 0
                            ack_received = False
                            self.log('Entering ACK testing and parsing stage.','debug')

                            # At this point, we confirmed successful data delivery to the HEC. Before we do any ACK, we should
                            # take a little rest and give the indexer time to work.
                            time.sleep(self.ack_interval / 2)                                
                            while ack_attempt_counter < self.max_ack_attempts and not ack_received:
                                # Technically, we send a list of ACKs because if we weren't doing this single-threaded,
                                # we could queue up data blocks - send them, and track them all in the same request...
                                # So this needs to be sent as a list even though we're probably only ACKing one block of data
                                if isinstance(response_data['ackId'], list):
                                    ack_data = { 'acks': response_data['ackId'] } 
                                else:
                                    ack_data = { 'acks': [response_data['ackId']] }
                                  

                                ack_attempt_counter += 1

                                # This should use the same session as before to ensure we get to the same backend server
                                try:
                                    ack_r = self.requests_data_send().post(self.server_ack_uri, 
                                        params=self.request_params, 
                                        data=json.dumps(ack_data), 
                                        verify=self.hec_tls_verify,
                                        timeout=self.http_timeout)

                                except Exception as ex3:
                                    self.log(('ERROR: context=%s; Exception occurred while trying to send ACK to HEC. Will continue. Exception: %s' % (self.context_id, str(ex3))),'error')
                                else:
                                    if ack_r.status_code == requests.codes.ok:
                                        # This loads the response which should be a listing of True/False for the ACKs we requested
                                        ack_data = json.loads(ack_r.text)

                                        # This checks all the responses to make sure they are all True
                                        if all(value for value in list(ack_data['acks'].values())):
                                            ack_received = True
                                            data_sent = True
                                        else:
                                            #self.log('ACK did not return true will continue the loop if appropriate.','debug')
                                            pass
                                    else:
                                        #self.log('ACK attempt resulted in a non-200 status code. Assuming failure to ACK and continuing loop.','debug')
                                        pass

                                    # But following attempts should be delayed by the ack_interval
                                    # Also, only do this if we didn't get an ACK on the previous attempt
                                    if not ack_received:
                                        time.sleep(self.ack_interval)


                        else:
                            self.log(('ERROR: context=%s; Response from HEC implies data send failure. Try again. Response: %s' % (self.context_id, str(response_data['text']))),'error')
                            # Something went wrong with the data delivery so I want to move to a different server (assuming there are more to move to)
                            self.set_http_session()

                    #############################################
                else:
                    self.log(('ERROR: context=%s; Unable to send payload to HEC. Status code: %s. Creating new session.' % (self.context_id, str(r.status_code))),'error')
                    self.log(('ERROR: context=%s; Status text: %s.' % (self.context_id, str(r.text))),'error')
                    # Also create a new session here
                    self.set_http_session()


        # Check for data send success
        if data_sent:
            # Data was sent, record the measurement; this isn't really necessary when data fails to send
            # because we expect to push it out to a backup method which is presently defined by the caller.
            self.log(('Measurement: Request sucessfully sent. send_attempts_required=%s, context=%s' % (str(data_attempt_counter), self.context_id)))
            return_value = True
        else:
            self.log(('ERROR: context=%s; Detected error sending batch of events. Sending events to backup function.' % (self.context_id)),'error')
            self.do_event_backup(payload_list)

            return_value = False


        return return_value


    '''
    In the multithread version, we use this to clear out the queue and end exeuction. Same concept except we're just going to do a final flushing.
    Kept for compat purposes.
    '''
    def stop_threads_and_processing(self):
        self.force_flush_events()

        if self.threading_enabled:
            self.processing_event.set()
            self.log('Stop thread and processing method called. Blocking until queue is empty.', 'debug')
            self.data_queue.join()
            self.run_threads = False


    '''
    The thread_processor essentially sits and waits on the Queue for messages to pop. Once it gets a message, it will attempt to deliver it to the HEC
    '''
    def thread_processor(self, use_thread_breaker = False):
        if use_thread_breaker:
            local_counter = 0

        # This method is run by the individual threads; data is processed and put on a queue
        # the threads should pick up that data and send it on
        while True:
            if self.run_threads == False:
                self.log('Thread %s exiting due to run_threads being set to false.' % (str(threading.currentThread().getName())), 'info')
                break
            
            # Block execution if the flag is false; otherwise do not block
            # This helps reduce processor utilization; otherwise, it will be pegged at 100%
            self.processing_event.wait(0.5)
            try:
                # Try to get an item off the queue 
                payload = self.data_queue.get(False)
                # If we succesfully pull data off the queue and this flag was not set before, set it to True so the thread
                # will not block
                self.processing_event.set()
            except Queue.Empty:
                # The queue is empty, clear this flag to block the thread for the specified timeout
                self.processing_event.clear()
                if use_thread_breaker:
                    local_counter += 1
                    if local_counter >= 60:
                        self.log('Thread %s exiting due to being idle.' % (str(threading.currentThread().getName())), 'info')
                        break

                # Do nothing; emptiness is fine.
                pass
            else:
                # If the thread is actively in use, we'll reset the counter value
                if use_thread_breaker:
                    local_counter = 0

                # Basically the only thing this thread needs to do is attempt to send a given payload.
                if self.use_ack:
                    self.force_flush_with_ack(payload)
                else:
                    self.force_flush_no_ack(payload)

                # The data processed, regardless of success. We expect failures to go to a backup queue.
                self.data_queue.task_done()


        sys.exit(0)
