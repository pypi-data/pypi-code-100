# https://python-socketio.readthedocs.io/en/latest/client.html
# https://flask-socketio.readthedocs.io/en/latest/
# https://python-socketio.readthedocs.io/en/latest/intro.html


import queue
import socketio
import json 
import time
import threading
from neurospeed.utils.api_config_service import ApiConfig


class HIA_Client:
    
    _HIA_version = "HIA version 2.0.0" 
    _packet_endpoint = 'pipeline'
    #_streams_dict = {}  # BAD IDEA - this variable would be shared across all class instances, causing data override


    def __init__(self, user_auth_handler, sensor_info):
        self._device_type = "user_data"
        self._hia_id = user_auth_handler.get_hia_id()
        self._username = user_auth_handler.get_username()
        self._contex = "User: {} HIA: {} - ".format(self._username, self._hia_id)
        self._api_config = ApiConfig()
        self._auth_handler = user_auth_handler
        
        # init streams qeueus for each sensor
        self._streams_dict = {} # GOOD IDEA - instance level variable, not shared at class level
        for key, value in sensor_info.items():
            stream_id = key
            sensor_payload =  value
            self._streams_dict[stream_id] = queue.Queue(-1)
            
        self._sensor_info = sensor_info
        self._access_token = self._auth_handler.get_access_token()
        self._user_config = self._auth_handler.get_config()
        self._exit_flag_2 = threading.Event() 
        self._external_socket_connection_handler = None
        self._external_socket_disconnect_handler = None
        self._connection_status = False
        
        logger_on = True
        if self._auth_handler.is_verbose_log() == False:
                logger_on = False
                
        self._sio = socketio.Client(logger=logger_on, engineio_logger=False, reconnection_delay  = 5, reconnection = True) 

        
    # Socket data sender - Start 
    def send_data(self, data, stream_id):  
        out_data = {"timestamp": time.time()} 
        out_data.update(data)

        # insert data into stream queue which belongs to received stream_id
        self._streams_dict[stream_id].put(json.dumps(out_data), timeout = 1)     
           
        
    def send_user_data_to_websocket(self, stream_id):  
        packet_ready = False
        sender_active = True
        while sender_active:
            time.sleep(0.1)
            if self._connection_status is False:
                message = "{} Socket disconnected, stopping user_data upstream for stream_id: {}".format(self._contex, stream_id)
                print(message)
                sender_active = False
                return
            TX_buffer = {"sample": []}
            stream_q_user_data = self._streams_dict[stream_id] # get relevant stream queue
            while (stream_q_user_data.empty() == False):  
                # pull sample from queue, and add to TX buffer:
                sample = json.loads(stream_q_user_data.get(timeout = 1))
                y = TX_buffer['sample']
                y.append(sample)
                packet_ready = True                    
            if (packet_ready):       
               # print("{} user_data packet ready for stream_id: {} ".format(self._contex, stream_id))
                packet_payload = {"stream_id": stream_id, "device_type": self._device_type, "hia_id": self._hia_id, "data": json.dumps(TX_buffer)}
                self._sio.emit(self._packet_endpoint, packet_payload)      
                packet_ready = False
     # Socket data sender - End      
    
    
    # Socket handlers - Start
    def attach_stream_state_handler(self, handler_function):
        self._sio.on('ssr_stream_state',handler = handler_function)
        
    def attach_downlink_handler(self, handler_function):
        self._sio.on('ssr_downlink',handler = handler_function)  
        
    def attach_socket_connection_handler(self, handler_function):
         self._sio.on('connect',handler = handler_function)
    
    def attach_socket_disconnect_handler(self, handler_function):
        self._sio.on('disconnect',handler = handler_function)
    
    def ping_handler(self):  # required DO NOT REMOVE
       self._sio.emit('pong')
       
       
    # internal stream state handler
    def stream_state_handler(self, data):
        print('{} SSR stream_state event: {}'.format(self._contex, data))
        # The incoming packet is a dictionary of shape {"stream_id_x": "stream_state", .., "stream_id_y": "stream_state"}
        # where stream_state is either "disabled" or "enabled" and stream_id is identifier of specific sensor
        str_id = list(data)[0] 
        if str_id in list(self._sensor_info):
            self._sensor_info[str_id]["stream_state"] = data[str_id]
        else:
            print("{} Stream state change error, invalid stream_id: {}".format(self._contex, str_id))
    
    # internal downlink handler
    def downlink_handler(self, payload):
        print('{} SSR downlink event: {}'.format(self._contex, payload))

        
    # internal connection error handler        
    def connection_error_handler(self, data):
        print('{} Connection error, message: {}'.format(self._contex, data) )
        self._connection_status = False
        
    # internal socket disconnect handler
    def socket_disconnect_handler(self):
        self._connection_status = False
        
        # propogate disconnect event to external handler if exist.. 
        if self._external_disconnection_handler != None:
            self._external_disconnection_handler(self) # send current instance contex
        
        
     # internal socket connection handler    
    def socket_connection_handler(self):
        print("{} Connected to NeuroSpeed Pipeline.".format(self._contex))
        self._connection_status = True

        # for each stream inside stream_dict, activate thread for sending data
        for key, value in self._streams_dict.items():
            stream_id = key
            print("{} starting user_data upstream thread for stream_id: {} ".format(self._contex, stream_id))
            user_data_outbound_websocket_TX = threading.Thread(target = self.send_user_data_to_websocket, args=[key])
            time.sleep(0.1)
            user_data_outbound_websocket_TX.start()
        
        # propogate connection event to external handler if exist.. 
        if self._socket_connection_external_handler != None:
            self._socket_connection_external_handler(self) # send current instance contex

   # Socket handlers - End
   
   
   #  Getters, Setters - Start
    def set_socket_connection_external_handler(self, handler):
        self._socket_connection_external_handler = handler
    
    def set_socket_disconnect_external_handler(self, handler):
        self._external_disconnection_handler = handler
        
    def is_connected(self):
        return self._connection_status == True
        
    def update_sensor_info(self, stream_id, payload):
        if (self.is_connected()):
            raise ValueError('Updating sensor info after connection is no allowed. ')
        self._sensor_info[stream_id].update(payload)    
        
    def is_stream_enabled(self, stream_id): 
        return self._sensor_info[stream_id]["stream_state"] == "enabled"
    
    def get_sensor_info(self):
        return self._sensor_info
    
    def get_username(self):
        return self._auth_handler.get_config()["username"]
    
    def get_hia_id(self):
        return self._hia_id
    
    # Self Getters Setters - End
    
    
    def connect(self):
        print(self._HIA_version)
    
        # internal HIA handlers
        self._sio.on('connect_error', handler=self.connection_error_handler)
        self._sio.on('ping', handler=self.ping_handler) #required to identify HIA health by the server ! do not remove.
        self.attach_stream_state_handler(self.stream_state_handler)
        self.attach_downlink_handler(self.downlink_handler)
        self.attach_socket_connection_handler(self.socket_connection_handler)
        self.attach_socket_disconnect_handler(self.socket_disconnect_handler)
        
        headers = {
            "jwt_token": self._access_token,  # required
            "hia_id": self._hia_id,  # required, make sure there are no 2 HIAs with the same id for specific user !
            "sensors_info": json.dumps(self._sensor_info),  # required, at least 1 sensor, otherwise connection will fail
        }
        pipeline_url =  self._api_config.get_socket_url()
     
        print("Connecting to NeuroSpeed pipeline as HIA: {} User: {} Sensors Stream ids: {}"
              .format( self._hia_id, self._username, list(self._sensor_info.keys()) ))
  
        self._sio.connect(url = pipeline_url, transports ='websocket', headers=headers, socketio_path= '/hia' ) 
    

    def disconnect(self):
        self._sio.disconnect()