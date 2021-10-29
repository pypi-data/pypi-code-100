import datetime as dt
import pandas as pd
import time
import random
import string
import paho.mqtt.client as mqtt
import sqlite3
import threading

#load other scripts
from . import dash_tools as dash
from . import json_tools as json
from . import dictionary_tools as dictionary

__version__ = "1.10.1"

#print command with Script name in front
class ScriptPrint:
    def __init__(self, name, block = False):
        self.name = name
        self.block = block
    def print(self, msg):
        if not self.block:
            print(f"[{self.name}]: {msg}")
            
#Timer for Script runtimes
class Timer:
    def __init__(self):
        self.startpoint = None
        self.lapstartpoint = None
        self.runtime = dt.timedelta(seconds = 0)
        self.lapruntime = dt.timedelta(seconds = 0)
        self.laps = []
    def start(self):
        if not self.startpoint:
            self.startpoint = dt.datetime.now()
            self.lapstartpoint = dt.datetime.now()
        else:
            raise Exception("Timer already running")
    def pause(self):
        if self.startpoint:
            now = dt.datetime.now()
            self.runtime += now - self.startpoint
            self.lapruntime += now - self.lapstartpoint
            self.startpoint = None
            self.lapstartpoint = None
            return self.runtime
        else:
            raise Exception("Timer not running")
    def set_lap(self):
        if self.lapstartpoint:
            now = dt.datetime.now()
            self.laps.append(self.lapruntime + now - self.lapstartpoint)
            self.lapstartpoint = now
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
        else:
            self.laps.append(self.lapruntime)
            self.lapruntime = dt.timedelta(seconds = 0)
            return self.laps[-1]
    def get_runtime(self):
        if self.startpoint:
            return self.runtime + dt.datetime.now() - self.startpoint
        else:
            return self.runtime
    def get_laps(self):
        return self.laps
    def get_lap_runtime(self):
        if self.lapstartpoint:
            return self.lapruntime + dt.datetime.now() - self.lapstartpoint
        else:
            return self.lapruntime
    def reset(self):
        self.__init__()
timer = Timer()

#CloudMQTT connector
class CloudMQTT:
    def __init__(self, client_name = "mmt_client", channel = "", qos = 0):
        self.client_name = client_name
        self.channel = channel
        self.qos = qos
        self.client = None
        self.bindings = {}
        self.user = None
        self.pw = None
        self.addr = None
        self.port = None
        
    #for handling messages
    def on_message(self, client, obj, msg):
        for bind in self.bindings:
            if msg.topic.startswith(bind):
                self.bindings[bind](msg.payload.decode("utf-8"), "/".join(msg.topic.split("/")[1:]))
                break
    #for conecting to server
    def connect(self, user, pw, addr, port):
        self.user = user
        self.pw = pw
        self.addr = addr
        self.port = port
        self.client = mqtt.Client(self.client_name)
        self.client.username_pw_set(user, pw)
        self.client.connect(addr, port)
        self.client.on_message = self.on_message
        self.client.subscribe(self.channel + "/#", qos = self.qos)
        self.client.loop_start()
    #for disconnecting
    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
    #for reconnecting
    def reconnect(self):
        self.disconnect()
        self.connect(self.user, self.pw, self.addr, self.port)
    #check connection
    def check_connection(self):
        try: resp = self.client.is_connected()
        except NameError: resp = False
        return resp
    #for publishing on channel
    def publish(self, topic, message):
        self.client.publish("/".join([self.channel, topic]), message, qos = self.qos)
    #for binding function to topic subcription
    def bind(self, topic, function):
        self.bindings["/".join([self.channel, topic])] = function
    #for binding a response function to topic
    def bind_response(self, topic, function):
        def resp_func(msg, topic):
            topic_list = topic.split("/")
            if topic_list[1] == "req":
                topic_list[1] = "resp"
                self.publish("/".join(topic_list), function(msg, topic))
        self.bind(topic + "/req", resp_func)
    #for unbinding functions
    def unbind(self, topic):
        del self.bindings["/".join([self.channel, topic])]
    #for requesting information
    def request(self, topic, message = "request", ID = None, retry = 5):
        if not ID:
            ID = random_ID()
        response = None
        def get_resp(msg, topic):
            nonlocal response
            response = msg
        self.bind("/".join([topic, "resp", str(ID)]), get_resp)
        self.publish("/".join([topic, "req", str(ID)]), message)
        start = time.time()
        while not response:
            if time.time()-start > retry:
                break
        self.unbind("/".join([topic, "resp", str(ID)]))
        return response    
cloudmqtt = CloudMQTT()    

#for getting variable name as string
def get_variable_name(var, namespace):
    if not isinstance(var, pd.DataFrame):
        return [k for k, v in namespace.items() if v == var][0]
    else:
        return [k for k, v in namespace.items() if var.equals(v)][0]

#for generating random ID
def random_ID(len = 20):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

#SQL tools
class SQL:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db = None
        self.commands = []
    def __exc_cmds___(self):
        for command in self.commands:
            self.cursor.execute(command)
        self.connection.commit()
        self.commands = []
    def __update__(self):
        while self.connection:
            self.__exc_cmds___()
            time.sleep(1)
    def connect(self, db):
        self.db = db
        self.connection = sqlite3.connect(self.db, check_same_thread = False)
        self.cursor = self.connection.cursor()
        threading.Thread(target = self.__update__).start()
    def disconnect(self):
        self.__exc_cmds___()
        self.connection.close()
        self.__init__()
    def execute(self, command):
        self.commands.append(command)
sql = SQL()
        