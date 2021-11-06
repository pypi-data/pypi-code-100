# HRI_Engine_client.py
#
# Copyright 2017 Eiichi Inohira
# Copyright 2019 Ryota Higashi
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python 3
# For Service Application

"""HRI_Engine_client
"""
import platform
from datetime import datetime
import time
import xmlrpc.client
import logging
import queue
import json

from pyrois import RoIS_HRI
from . import Service_Application_IF_sample

class SystemIF(RoIS_HRI.SystemIF):
    """SystemIF
    """
    def __init__(self, proxy_obj):
        self._proxy = proxy_obj
        self.logger.info("HRI_Engine_client_sample.SystemIF(): complete init")

    def connect(self):
        try:
            status = RoIS_HRI.ReturnCode_t(self._proxy.connect())
            self.logger.info("Connect:status[{}]".format(status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Connect:{}".format(e))
        return status

    def disconnect(self):
        try:
            status = RoIS_HRI.ReturnCode_t(self._proxy.disconnect())
            self.logger.info("Disconnect:status[{}]".format(status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Disconnect:{}".format(e))
        return status

    def get_profile(self, condition):
        try:
            (s, profile) = self._proxy.get_profile(condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Get_Profile:status[{}],profile[{}]".format(status,profile))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            profile = ""
            self.logger.error("Get_Profile:{}".format(e))
        return (status, profile)

    def get_error_detail(self, error_id, condition):
        try:
            (s, results) = self._proxy.get_error_detail(error_id, condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Get_Error_Detail({}):status[{}]".format(error_id,status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            results = [""]
            self.logger.error("Get_Error_Detail({}):{}".format(error_id,e))
        return (status, results)


class CommandIF(RoIS_HRI.CommandIF):
    """CommandIF
    """
    def __init__(self, proxy_obj):
        self._proxy = proxy_obj
        self.logger.info("HRI_Engine_client_sample.CommandIF(): complete init")

    def search(self, condition):
        try:
            (s, component_ref_list) = self._proxy.search(condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Search:status[{}],component_ref[{}]".format(status,component_ref_list))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            component_ref_list = [""]
            self.logger.error("Search:{}".format(e))
        return (status, component_ref_list)

    def bind(self, component_ref):
        try:
            status = RoIS_HRI.ReturnCode_t(self._proxy.bind(component_ref))
            self.logger.info("Bind({}):status[{}]".format(component_ref,status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Bind({}):{}".format(component_ref,e))
        return status

    def bind_any(self, condition):
        try:
            (s, component_ref_list) = self._proxy.search(condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Bind_Any:status[{}]".format(status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            component_ref_list = [""]
            self.logger.error("Bind_Any:{}".format(e))
        return (status, component_ref_list)

    def release(self, component_ref):
        try:
            status = RoIS_HRI.ReturnCode_t(self._proxy.release(component_ref))
            self.logger.info("Release({}):status[{}]".format(component_ref,status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Release({}):{}".format(component_ref,e))
        return status

    def get_parameter(self, component_ref):
        try:
            (s, parameter_list) = self._proxy.get_parameter(component_ref)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Get_Parameter({}):status[{}],parameter_list[{}]".format(component_ref,status,parameter_list))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            parameter_list = [""]
            self.logger.error("Get_Parameter({}):{}".format(component_ref,e))
        return (status, parameter_list)

    def set_parameter(self, component_ref, parameters):
        try:
            (s, command_id) = self._proxy.set_parameter(component_ref, parameters)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Set_Parameter({}):status[{}],id[{}]".format(component_ref,status,command_id))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            command_id = "00"
            self.logger.error("Set_Parameter({}):{}".format(component_ref,e))
        return (status, command_id)

    def execute(self, command_unit_list):
        try:
            j = json.dumps(command_unit_list, default=self.object_to_dict, indent=4)
            d = json.loads(j)
            if "command_unit_list" not in d.keys():
                status = RoIS_HRI.ReturnCode_t.BAD_PARAMETER
                return (status, command_unit_list)
            (s, command_unit_list) = self._proxy.execute(j)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Execute({}):status[{}]".format(command_unit_list,status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Execute({}):{}".format(command_unit_list,e))
        return (status, command_unit_list)

    def get_command_result(self, command_id, condition):
        try:
            (s, results) = self._proxy.get_command_result(command_id, condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Get_Command_Result({}):status[{}],results[{}]".format(command_id,status,results))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Disconnect:{}".format(e))
        return (status, results)


class QueryIF(RoIS_HRI.QueryIF):
    """QueryIF
    """
    def __init__(self, proxy_obj):
        self._proxy = proxy_obj
        self.logger.info("HRI_Engine_client_sample.QueryIF(): complete init")

    def query(self, query_type, condition):
        try:
            (s, results) = self._proxy.query(query_type, condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Query({}):status[{}],results[{}]".format(query_type,status,results))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            results = [""]
            self.logger.error("Query({}):{}".format(query_type,e))
        return (status, results)


class EventIF(RoIS_HRI.EventIF):
    """EventIF
    """
    def __init__(self, proxy_obj):
        self._proxy = proxy_obj
        self.logger.info("HRI_Engine_client_sample.EventIF(): complete init")

    def subscribe(self, event_type, condition):
        try:
            (s, subscribe_id) = self._proxy.subscribe(event_type, condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Subscribe({}):status[{}],id[{}]".format(event_type,status,subscribe_id))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            subscribe_id = "00"
            self.logger.error("Subscribe({}):{}".format(event_type,e))
        return (status, subscribe_id)

    def unsubscribe(self, subscribe_id):
        try:
            s = self._proxy.unsubscribe(subscribe_id)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Unsubscribe({}):status[{}]".format(subscribe_id,status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            self.logger.error("Unsubscribe({}):{}".format(subscribe_id,e))
        return status

    def get_event_detail(self, event_id, condition):
        try:
            (s, results) = self._proxy.get_event_detail(event_id, condition)
            status = RoIS_HRI.ReturnCode_t(s)
            self.logger.info("Get_Event_Detail({}):status[{}]".format(event_id,status))
        except Exception as e:
            status = RoIS_HRI.ReturnCode_t.ERROR
            results = [""]
            self.logger.error("Get_Event_Detail({}):{}".format(event_id,e))
        return (status, results)


class IF(SystemIF, CommandIF, QueryIF, EventIF, Service_Application_IF_sample.Service_Application_IF):
    """IF
    """
    def __init__(self, uri, logger=None, event_queue=None):
        self._uri = uri
        # self.a = Service_Application_Base_example.Service_Application_Base()

        self.dt = datetime.now()
        self.dt_format = self.dt.strftime("%Y%m%d-%H%M")
        self.os = platform.system()

        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger('Service_Application: HRI_Engine_client_sample.py')
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            #self.fh = logging.FileHandler('{}_{}.log'.format(self.dt_format,self.os))
            self.fh = logging.FileHandler('{}.log'.format(self.dt_format))
            self.fh.setLevel(logging.DEBUG)
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

            self.ch = logging.StreamHandler()
            self.ch.setLevel(logging.ERROR)
            self.ch.setFormatter(formatter)
            self.logger.addHandler(self.ch)

        import os
        self.logger.info("This_logger_has_also_logs_in_Service_Application_IF_sample.py {}".format(os.getpid()))

        self.logger.info("HRI Engine URL: {}".format(self._uri))
        self._proxy = xmlrpc.client.ServerProxy(self._uri)

        Service_Application_IF_sample.Service_Application_IF.__init__(self,self._uri,logger=self.logger,event_queue=event_queue)
        self.logger.info("HRI_Engine_client_sample.IF(): complete init")
    
    def object_to_dict(self, item):
        if isinstance(item, object) and hasattr(item, '__dict__'):
            return item.__dict__
        else:
            raise TypeError

if __name__ == "__main__":
    uri = 'http://127.0.0.1:8017'
    test = IF(uri)