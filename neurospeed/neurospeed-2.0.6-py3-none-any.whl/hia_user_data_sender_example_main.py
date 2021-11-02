
import time
from pathlib import Path
import os

from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.api_socket_handlers.downlink_room_as_user_handler import DownlinkRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService
from neurospeed.hia_user_data.neurobrave_sensor_interface import HIA_Client

import threading


x={'ch1':12, 'ch2': 14}

my_custom_sensor_info = {
   'sensor_type': 'vehicle speed',
   'channel_count' : 2,
   'manufacturer_id': 'toyota'

}

# see README(5)
def get_sensors_mockup():
    # generate SOME sensors stream ids
    user_data_stream_id =  "user_data" + '_' + UtilService.generateId(6)
    user_data_custom_stream_id = "some_custom_stream_id"

    sensor_info = dict()
    sensor_info[user_data_stream_id] =  {
        "device_type": "user_data",
        "channel_count": 2,
        "sensor_id" : user_data_stream_id,
        "stream_id": user_data_stream_id,
        "stream_state" : "enabled"
    } 
    
    sensor_info[user_data_custom_stream_id] =  {
        "device_type": "user_data",
        "channel_count": 2,
        "sensor_id" : user_data_custom_stream_id,
        "stream_id": user_data_custom_stream_id,
        "stream_state" : "enabled"
    } 
    
    return sensor_info
 


def downlink_message_external_handler(downlink_handler_instance, payload):
    username = downlink_handler_instance.get_username()
    print('~~~external user', username,' downlink message: ', payload)


# send dummy data loop for some stream_id. must be activated after socket successful connection.
def generate_data(hia_client, stream_id):
    for i in range(5000):
        if hia_client.is_connected() == False: # stop sending data if disconnected
            raise ValueError("hia for " , hia_client.get_username(), " disconnected , stopping data generator thread")
        if hia_client.is_stream_enabled(stream_id): # send only if stream enabled for that sensor
            hia_client.send_data(x, stream_id)
        time.sleep(0.2)
        
    hia_client.disconnect() #disconnect after finish, just for the example


def disconnect_external_handler(hia_client):
   print("hia:[", hia_client.get_hia_id(),"]", "user:[", hia_client.get_username(),"] disconnected ")
    
 
    
# would be called for each hia after successfuly connection  
def connection_external_handler(hia_client):
    username = hia_client.get_username()
    hia_id = hia_client.get_hia_id()
    print('connected as ', username, " with hia: " ,hia_id, ". sending data..")
    
    # generate dummy data for each sensor inside HIA_Client, 
    sensor_info = hia_client.get_sensor_info()
    for stream_id in sensor_info:
        print("activating data generator thread for stream_id:", stream_id , " username: ", username, "hia_id: ", hia_id)
        user_data_data_generator = threading.Thread(target = generate_data, args=[hia_client, stream_id])
        time.sleep(0.1)
        user_data_data_generator.start()

    

# example of login, connect and send data as 2 different HIA users with 2 mockup sensors for each
# Hint: you can set "Verbose_socket_log": "True" in user config to enable more logging
def run_HIAs():
    
    # load users configuration
    user1_config_path = os.path.join(str(Path().absolute()) ,"config","hia_config1.json")
    config_user1 = UtilService.load_config_file(user1_config_path)
    
    user2_config_path = os.path.join(str(Path().absolute()) ,"config","hia_config2.json")
    config_user2 = UtilService.load_config_file(user2_config_path)
    
    # create Auth_AS_User_Handler for each user and pass user configuration 
    user1_auth = Auth_AS_User_Handler(config_user1)
    user2_auth = Auth_AS_User_Handler(config_user2)
    
    user1_auth.login()
    user2_auth.login()
    
    time.sleep(1)
    # get sensors info mockups 
    hia_sensor_info_user1 = get_sensors_mockup() 
    hia_sensor_info_user2 = get_sensors_mockup() 
    print('Generated mockup sensors for user 1: {}'.format(hia_sensor_info_user1) )
    print('Generated mockup sensors for user 2: {}'.format(hia_sensor_info_user2))
    
    # create HIA instances for both users, pass user's auth handler and generated sensors info
    hia_user1 = HIA_Client(user1_auth, hia_sensor_info_user1)
    hia_user2 = HIA_Client(user2_auth, hia_sensor_info_user2)

    # update sensor information example. Updating sensor info after (!) connection is not allowed and will cause errors
    first_stream_id = next(iter(hia_sensor_info_user1)) # take first stream_id for the example
    print('Updaing sensor info for first_stream_id:', first_stream_id)
    hia_user1.update_sensor_info(first_stream_id, my_custom_sensor_info) 
    
    
    # example connecting to SSR downlink and listen on events from customer
    user1_downlink = DownlinkRoom_AS_User_Handler(user1_auth)
    user1_downlink.set_downlink_router_external_handler(downlink_message_external_handler)
    user1_downlink.connect()
    
    
    # This is example for periodical sending of data from a thread
    
    # attach external handlers this external dis\connection handler would be called on dis\connection in addition
    # to internal built-in connection handler inside HIA_Client
    hia_user1.set_socket_connection_external_handler(connection_external_handler) 
    hia_user2.set_socket_connection_external_handler(connection_external_handler)
    
    hia_user1.set_socket_disconnect_external_handler(disconnect_external_handler)
    hia_user2.set_socket_disconnect_external_handler(disconnect_external_handler)
    
    # connect HIAs to NeuroSpeed pipeline 
    hia_user1.connect()
    hia_user2.connect()
    
    ## once connection established, "connection_external_handler" function would be called for each connected HIA, results in mockup data generation 
    
    # This example of simple manual data sender:
    time.sleep(5) 
    if hia_user1.is_connected():
        hia_user1.send_data({"ch0": 5}, first_stream_id ) 

  
 
    
  
def main():
    run_HIAs()
    


if __name__ == '__main__':    
    main()  