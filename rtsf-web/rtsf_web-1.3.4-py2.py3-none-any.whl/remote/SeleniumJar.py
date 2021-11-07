#! python3
# -*- encoding: utf-8 -*-

import requests
import time
import subprocess


class SeleniumJar(object):    
    def __init__(self, server_jar_full_path, java_exe_full_path="java"):
        self._conf = {
            "java_path": java_exe_full_path,
            "jar_path": server_jar_full_path,
            }
        self._ip = "localhost"
        self._port = 4444
        self.command = []
        self.__subp = None
        self._block = False
                        
    def hub(self, port):
        """ java -jar selenium-server.jar -role hub -port 4444
        @param port:  listen port of selenium hub 
        """
        self._ip = "localhost"
        self._port = port 
        self.command = [self._conf["java_path"], "-jar", self._conf["jar_path"], "-port", str(port), "-role", "hub"]        
        return self
        
    def node(self, node_address=("", 5555), hub_address=("localhost", 4444)):
        """ java -jar selenium-server.jar -role node -port 5555 -hub http://127.0.0.1:4444/grid/register/
        @param node_address: selenium node(host, port), host usually determined automatically.
        @param hub_address: hub address which node will connect to 
        """
        host, port = node_address
        self._ip, self._port = hub_address
        self.command = [self._conf["java_path"], "-jar", self._conf["jar_path"],
                        "-port", str(port),
                        "-role", "node",
                        "-hub", "http://{0}:{1}/grid/register/".format(self._ip, self._port)]
        if host:
            self.command.extend(['-host', host])

        return self
    
    def start_server(self, block=False):
        """start the selenium Remote Server."""
        self._block = block if type(block) is bool else False

        if self._block:
            subprocess.call(self.command)
        else:
            self.__subp = subprocess.Popen(self.command)
        # print("\tselenium jar pid[%s] is running." %self.__subp.pid)
        time.sleep(2)
        
    def stop_server(self):
        """stop the selenium Remote Server
        :return:
        """
        if self._block is False:
            self.__subp.kill()
        # print("\tselenium jar pid[%s] is stopped." %self.__subp.pid)
        
    def re_start_server(self):
        """reStart the selenium Remote server"""
        self.stop_server()
        self.start_server()
    
    def is_runnnig(self):
        """Determine whether hub server is running
        :return:True or False
        """
        try:
            resp = requests.get("http://{0}:{1}".format(self._ip, self._port))

            if resp.status_code == 200:
                return True
            else:
                return False
        except:
            return False
