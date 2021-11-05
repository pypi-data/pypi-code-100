# HRI_Engine(main).py
#
# Copyright 2017 Eiichi Inohira
# Copyright 2019 Ryota Higashi 
# This software may be modified and distributed under the terms
# of the MIT license
#
# For python 3
# For HRI Engine

"""Main_HRI_Engine_example
"""

from __future__ import print_function # 3⇒2系互換

import os
import sys
import xml.etree.ElementTree as ET
import threading
from concurrent.futures import ThreadPoolExecutor
import queue
import time
from datetime import datetime
from collections import deque
import logging
import platform
import importlib
import json
import itertools
import socketserver
import xmlrpc.server

from pyrois import RoIS_HRI, RoIS_Common, RoIS_Service, IF_server
from . import message_profile, Service_Application_Base_sample, HRI_Engine_client_sample

class SystemIF(RoIS_HRI.SystemIF):
    """SystemIF
    """
    def __init__(self, Engine):
        self._engine = Engine

    def connect(self):
        self._engine.state = True
        # サブHRIエンジンはコンストラクタで行うconnectを実行する
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.logger.info("connect")
        return status

    def disconnect(self):
        self._engine.state = False
        # サブHRIエンジンのdisconnectは実行しない
        status = RoIS_HRI.ReturnCode_t.OK.value
        self.logger.info("disconnect")
        return status

    def get_profile(self, condition):
        if self._engine.state is True:
            # プロファイルを返す(サブHRIエンジンと同じ) サブHRIエンジンのget_profileは呼ばない
            profile = self.engine_profile
            status = RoIS_HRI.ReturnCode_t.OK.value
            self.logger.info("Get_Profile:Success")
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            profile = " "
            self.logger.error("Get_Profile:Engine_status_is_false")
        return (status, profile)

    def get_error_detail(self, error_id, condition):
        if self._engine.state is True:
            # error_idからHRIエンジンを判別し，そのエンジンのget_error_detailを実行する
            e = error_id.split('-')
            engine_name = e[0]
            # サブエンジンの場合
            if engine_name in self.sub_engine.keys():
                try:
                    (s, results) = self.sub_engine[engine_name].get_error_detail(error_id, condition)
                    status = s.value
                    if s == RoIS_HRI.ReturnCode_t.OK:
                        self.logger.info("Get_Error_Detail({}):Status_of_Get_Error_Detail_in_sub_engine_is_{}".format(error_id,s))
                    else:
                        self.logger.error("Get_Error_Detail({}):Status_of_Get_Error_Detail_in_sub_engine_is_{}".format(error_id,s))
                except:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    results = ["Cannot_connect_to_the_engine[{}]".format(e[0])]
                    self.logger.error("Get_Error_Detail({}):Cannot_connect_to_the_Get_Error_Detail_in_[{}]_engine".format(error_id,e[0]))
            # メインエンジン(自分自身)の場合
            elif engine_name == self.my_engine_name:
                if error_id in self.error_detail.keys():
                    status = RoIS_HRI.ReturnCode_t.OK.value
                    results = [self.error_detail[error_id]]
                    self.logger.info("Get_Error_Detail({}):Success <results:{}>".format(error_id,results))
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    results = ["Error_id({})_is_wrong".format(error_id)]
                    self.logger.error("Get_Error_Detail({}):Error_id_is_wrong".format(error_id))
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                results = ["Engine[{}]_is_not_registered".format(e[0])]
                self.logger.error("Get_Error_Detail({}):Engine[{}]_is_not_registered".format(error_id,e[0]))
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            results = ["Engine_state_is_false"]
            self.logger.error("Get_Error_Detail({}):Engine_status_is_false".format(error_id))
        return (status, results)


class CommandIF(RoIS_HRI.CommandIF):
    """CommandIF
    """
    def __init__(self, Engine):
        self._engine = Engine

    def search(self, condition):
        command_id = self.create_new_id("command")
        if self._engine.state is True:
            component_ref_list = self.component_list
            status = RoIS_HRI.ReturnCode_t.OK.value
            self.command_result[command_id] = "Search:Success <component_ref_list:{}>".format(component_ref_list)
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            component_ref_list = [" "]
            self.command_result[command_id] = "Search:Engine_status_is_false"
        
        if status == RoIS_HRI.ReturnCode_t.OK.value:
            self.logger.info("{}:{}".format(command_id,self.command_result[command_id]))
        else:
            self.logger.error("{}:{}".format(command_id,self.command_result[command_id]))
        return (status, component_ref_list)

    def bind(self, component_ref):
        command_id = self.create_new_id("command")
        if self._engine.state is True:
            if component_ref in self.component_list:
                # component_refからサブHRIエンジンを判別し，そのエンジンのbindを実行する
                m = component_ref.split(':')
                engine_name = m[5]
                # サブエンジンの場合
                if engine_name in self.sub_engine.keys():
                    try:
                        s = self.sub_engine[engine_name].bind(component_ref)
                        status = s.value
                        self.command_result[command_id] = "Bind({}):Status_of_bind_in_sub_engine_is_{}".format(component_ref,s)
                    except:
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        self.command_result[command_id] = "Bind({}):Cannot_connect_to_the_bind_method_in_[{}]_engine".format(component_ref,m[5])
                # メインエンジン(自分自身)の場合
                elif engine_name == self.my_engine_name:
                    if component_ref in self.binding:
                        status = RoIS_HRI.ReturnCode_t.OK.value
                        self.command_result[command_id] = "Bind({}):Already_Bound".format(component_ref)
                    else:
                        self.binding.append(component_ref)
                        status = RoIS_HRI.ReturnCode_t.OK.value
                        self.command_result[command_id] = "Bind({}):Success".format(component_ref)
                # エンジンがない場合
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    self.command_result[command_id] = "Bind({}):Engine[{}]_is_not_registered".format(component_ref,m[5])
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.command_result[command_id] = "Bind({}):This_component_is_not_registered".format(component_ref)
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            self.command_result[command_id] = "Bind({}):Engine_status_is_false".format(component_ref)

        if status == RoIS_HRI.ReturnCode_t.OK.value:
            self.logger.info("{}:{}".format(command_id,self.command_result[command_id]))
        else:
            self.logger.error("{}:{}".format(command_id,self.command_result[command_id]))
        return status

    def bind_any(self, condition):
        if self._engine.state is True:
            status = RoIS_HRI.ReturnCode_t.OK.value
            component_ref_list = ["None"]
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            component_ref_list = [" "]
        return (status, component_ref_list)

    def release(self, component_ref):
        command_id = self.create_new_id("command")
        if self._engine.state is True:
            if component_ref in self.component_list:
                # component_refからサブHRIエンジンを判別し，そのエンジンのreleaseを実行する
                m = component_ref.split(':')
                engine_name = m[5]
                # サブエンジンの場合
                if engine_name in self.sub_engine.keys():
                    try:
                        s = self.sub_engine[engine_name].release(component_ref)
                        status = s.value
                        self.command_result[command_id] = "Release({}):Status_of_release_in_sub_engine_is_{}".format(component_ref,s)
                    except:
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        self.command_result[command_id] = "Release({}):Cannot_connect_to_the_release_method_in_[{}]_engine".format(component_ref,m[5])
                # メインエンジン(自分自身)の場合
                elif engine_name == self.my_engine_name:
                    if component_ref in self.binding:
                        self.binding.remove(component_ref)
                        status = RoIS_HRI.ReturnCode_t.OK.value
                        self.command_result[command_id] = "Release({}):Success"
                    else:
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        self.command_result[command_id] = "Release({}):This_component_has_not_been_Bound".format(component_ref)
                # エンジンがない場合
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    self.command_result[command_id] = "Release({}):Engine[{}]_is_not_registered".format(component_ref,m[5])
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.command_result[command_id] = "Release({}):This_component_is_not_registered".format(component_ref)
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            self.command_result[command_id] = "Release({}):Engine_status_is_false".format(component_ref)
        
        if status == RoIS_HRI.ReturnCode_t.OK.value:
            self.logger.info("{}:{}".format(command_id,self.command_result[command_id]))
        else:
            self.logger.error("{}:{}".format(command_id,self.command_result[command_id]))
        return status

    def get_parameter(self, component_ref, command_id=None):
        if command_id is None:
            command_id = self.create_new_id("command")
        if self._engine.state is True:
            if component_ref in self.component_list:
                # component_refからサブHRIエンジンを判別し，そのエンジンのget_parameterを実行する
                m = component_ref.split(':')
                engine_name = m[5]
                # サブエンジンの場合
                if engine_name in self.sub_engine.keys():
                    try:
                        (s, parameter_list) = self.sub_engine[engine_name].get_parameter(component_ref)
                        status = s.value
                        self.command_result[command_id] = "Get_parameter({}):Status_of_get_parameter_in_sub_engine_is_{}".format(component_ref,s)
                    except:
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        self.command_result[command_id] = "Get_parameter({}):Cannot_connect_to_the_get_parameter_method_in_[{}]_engine".format(component_ref,m[5])
                # メインエンジン(自分自身)の場合
                elif engine_name == self.my_engine_name:
                    if component_ref in self.binding:
                        m = component_ref.split(':')
                        comp_name = m[6]
                        comp_param = ['SystemInformation','PersonLocalization','FaceLocalization','SoundLocalization','SpeechRecognition','GestureRecognition',
                                    'SpeechSynthesis','Reaction','Navigation','Follow','Move']
                        if comp_name in comp_param:
                            # comp_urn = m[5] +":"+ m[6]
                            # if comp_urn in self.component_client.keys():
                            if comp_name in self.component_client.keys():
                                try:
                                    if comp_name == 'SystemInformation':
                                        (status, e_status, operable_time) = self.component_client['SystemInformation'].engine_status()
                                        (status, timestamp, robot_ref, position_data) = self.component_client['SystemInformation'].robot_position()
                                        parameters = (status, e_status.value, operable_time, timestamp, robot_ref, position_data)
                                    else:
                                        # parameters = self.component_client[comp_urn].get_parameter()
                                        parameters = self.component_client[comp_name].get_parameter()
                                        
                                    if parameters[0] == RoIS_HRI.ReturnCode_t.OK:
                                        parameter_list = parameters[1:]
                                        status = RoIS_HRI.ReturnCode_t.OK.value
                                        self.command_result[command_id] = 'Get_parameter({}):Parameters_{}'.format(component_ref,str(parameter_list))
                                    else:
                                        status = parameters[0].value
                                        self.command_result[command_id] = "Get_parameter({}):Component_status_is_{}".format(component_ref,parameters[0])
                                except Exception as e:
                                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                                    self.command_result[command_id] = "Get_parameter({}):{}".format(component_ref,e)
                            else:
                                status = RoIS_HRI.ReturnCode_t.ERROR.value
                                self.command_result[command_id] = "Get_parameter({}):Not_found_the_specified_component".format(component_ref)
                        else:
                            status = RoIS_HRI.ReturnCode_t.ERROR.value
                            self.command_result[command_id] = "Get_parameter({}):This_component_doesn't_have_parameter".format(component_ref)
                    else:
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        self.command_result[command_id] = "Get_parameter({}):This_component_have_not_been_bound".format(component_ref)
                # エンジンがない場合
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    self.command_result[command_id] = "Get_parameter({}):Engine[{}]_is_not_registered".format(component_ref,m[5])
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.command_result[command_id] = "Get_parameter({}):This_component_is_not_registered".format(component_ref)
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            self.command_result[command_id] = "Get_parameter({}):Engine_status_is_false".format(component_ref)
        
        if status == RoIS_HRI.ReturnCode_t.OK.value:
            self.logger.info("{}:{}".format(command_id,self.command_result[command_id]))
        else:
            parameter_list = [""]
            self.logger.error("{}:{}".format(command_id,self.command_result[command_id]))
        return (status, parameter_list)

    def set_parameter(self, component_ref, parameters, command_id=None):
        setparam_command_id = command_id
        if setparam_command_id is None:
            command_id = self.create_new_id("command")
        para_num = {'PersonLocalization':2,'FaceLocalization':2,'SoundLocalization':2,'SpeechRecognition':3,
                    'SpeechSynthesis':5,'Reaction':1,'Navigation':3,'Follow':3,'Move':3}
        if self._engine.state is True:
            if component_ref in self.component_list:
                # component_refからサブHRIエンジンを判別し，そのエンジンのset_parameterを実行する
                m = component_ref.split(':')
                engine_name = m[5]
                # サブエンジンの場合
                if engine_name in self.sub_engine.keys():
                    try:
                        (s, command_id) = self.sub_engine[engine_name].set_parameter(component_ref, parameters)
                        status = s.value
                        self.command_result[command_id] = "Set_parameter({}):Status_of_set_parameter_in_sub_engine_is_{}".format(component_ref,s)
                    except:
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        self.command_result[command_id] = "Set_parameter({}):Cannot_connect_to_the_set_parameter_method_in_[{}]_engine".format(component_ref,m[5])
                # メインエンジン(自分自身)の場合
                elif engine_name == self.my_engine_name:
                    if component_ref in self.binding:
                        comp_name = m[6]
                        if comp_name in para_num.keys():
                            # comp_urn = m[5] +":"+ m[6]
                            # if comp_urn in self.component_client.keys():
                            if comp_name in self.component_client.keys():
                                if len(parameters) == para_num[comp_name]:
                                    try:
                                        # comp_state = self.component_client[comp_urn].set_parameter(*parameters)
                                        comp_state = self.component_client[comp_name].set_parameter(*parameters)
                                        if comp_state == RoIS_HRI.ReturnCode_t.OK:
                                            # t = threading.Thread(target=self.analyze_component_status, daemon=True, args=(self.component_client[comp_urn],self.command_id,))
                                            t = threading.Thread(target=self.analyze_component_status, daemon=True, args=(self.component_client[comp_name],command_id,))
                                            t.start()
                                            self.command_result[command_id] = "Set_parameter({})".format(component_ref)
                                            status = RoIS_HRI.ReturnCode_t.OK.value
                                        else:
                                            self.command_result[command_id] = "Set_parameter({}):Component_status_is_{}".format(component_ref,comp_state)
                                            status = comp_state.value
                                    except Exception as e:
                                        self.command_result[command_id] = "Set_parameter({}):{}".format(component_ref,e)
                                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                                else:
                                    self.command_result[command_id] = "Set_parameter({}):Incorrect_number_of_arguments;now[{}]/correct[{}]".format(component_ref,str(len(parameters)),str(para_num[comp_name]))
                                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                            else:
                                self.command_result[command_id] = "Set_parameter({}):Not_found_the_specified_component".format(component_ref)
                                status = RoIS_HRI.ReturnCode_t.ERROR.value
                        else:
                            self.command_result[command_id] = "Set_parameter({}):This_component_doesn't_have_set_parameter".format(component_ref)
                            status = RoIS_HRI.ReturnCode_t.ERROR.value
                    else:
                        self.command_result[command_id] = "Set_parameter({}):This_component_have_not_been_bound".format(component_ref)
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                # エンジンがない場合
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    self.command_result[command_id] = "Set_parameter({}):Engine[{}]_is_not_registered".format(component_ref,m[5])
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.command_result[command_id] = "Set_parameter({}):This_component_is_not_registered".format(component_ref)
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            self.command_result[command_id] = "Set_parameter({}):Engine_status_is_false".format(component_ref)
        
        if status == RoIS_HRI.ReturnCode_t.OK.value:
            self.logger.info("{}:{}".format(command_id,self.command_result[command_id]))
        else:
            self.logger.error("{}:{}".format(command_id,self.command_result[command_id]))
        return (status, command_id)

    def execute(self, command_unit_list, is_branch=False, command_id_base=None): # command_unit_list: command_message.CommandUnitSequence
        self.logger.info("Start Execute")
        # self.logger.info(command_unit_list)
        execute_id = self.create_new_id("execute",is_branch=is_branch,command_id_base=command_id_base)
        if self._engine.state is True:
            # self.logger.info("OK")
            status = RoIS_HRI.ReturnCode_t.OK.value
            try:
                d = json.loads(command_unit_list)
                # self.logger.info(d)
                if is_branch == False:
                    if self.check_branch(d,execute_id) == False: 
                        self.command_result[execute_id] = "Execute({}):Can't access the set_parameter in the same component from different branches".format(execute_id)
                        self.logger.error(self.command_result[execute_id])
                        status = RoIS_HRI.ReturnCode_t.ERROR.value
                        return (status, command_unit_list)
                    command_list = d["command_unit_list"]
                else:
                    command_list = d["command_list"]
                i = 0
                for c in command_list:
                    # self.logger.info(c)
                    if "branch_list" not in c.keys():
                        i += 1
                        # self.logger.info(c_k[0])
                        command_id = self.create_new_id("execute",command_id_base=command_id_base,command_num=i)
                        component_ref = c["component_ref"]
                        command_type = c["command_type"]  
                        c["command_id"] = command_id

                        # self.logger.info(c["arguments"]["parameters"])
                        arguments = {p["name"]:p["value"] for p in list(c["arguments"]["parameters"])}
                        delay_time = c["delay_time"]
                        # self.logger.info("component_ref:{},command_type:{},arguments:{},delay_time:{}".format(component_ref,command_type,arguments,delay_time))
                        # self.logger.info(d)
                        
                        if component_ref in self.component_list:
                            time.sleep(delay_time * 0.001)
                            if command_type == "set_parameter":
                                (status, c_id) = self.set_parameter(component_ref,list(arguments.values()),command_id)
                                self.command_result[command_id] = "Execute({},{}):Finished set parameter / set_parameter id = {}".format(component_ref,command_type,c_id)
                                self.logger.info(self.command_result[command_id])
                                c["command_id"] = c_id
                                if status == RoIS_HRI.ReturnCode_t.ERROR.value:
                                    self.command_result[execute_id] = "Execute({},{}):Status of Set_Parameter is ERROR".format(component_ref,command_type)
                                    self.logger.error(self.command_result[execute_id])
                                    command_unit_list = json.dumps(d, indent=4) 
                                    return (status,command_unit_list)
                            elif command_type == "get_parameter":
                                (status, parameter_list) = self.get_parameter(component_ref)
                                self.command_result[command_id] = "Execute({},{}):Finished get parameter".format(component_ref,command_type)
                                self.logger.info(self.command_result[command_id])
                                # サブエンジンのget_parameterのidは取得できない
                                if status == RoIS_HRI.ReturnCode_t.ERROR.value:
                                    self.command_result[execute_id] = "Execute({},{}):Status of Get_Parameter is ERROR".format(component_ref,command_type)
                                    self.logger.error(self.command_result[execute_id])
                                    command_unit_list = json.dumps(d, indent=4)
                                    return (status,command_unit_list)
                            else:
                                status = RoIS_HRI.ReturnCode_t.ERROR.value
                                self.command_result[execute_id] = "Execute({},{}):The command_type is undefined".format(component_ref,command_type)
                                self.logger.error(self.command_result[execute_id])
                                command_unit_list = json.dumps(d, indent=4)
                                return (status,command_unit_list)
                        else:
                            status = RoIS_HRI.ReturnCode_t.ERROR.value
                            self.command_result[execute_id] = "Execute({},{}):This_component_is_not_registered".format(component_ref,command_type)
                            self.logger.error(self.command_result[execute_id])
                            command_unit_list = json.dumps(d, indent=4)
                            return (status,command_unit_list)

                    else: # ConcurrentCommands(Branch list) -> Branch(CommandMessage list)
                        branch_delay_time = c["delay_time"]
                        time.sleep(branch_delay_time * 0.001)
                        futures = []
                        results = []
                        execute_branch_num = 1
                        for branch in c["branch_list"]:
                            if command_id_base is None:
                                id_base = "b-{}".format(execute_branch_num)
                            else:
                                id_base = "{}-b-{}".format(command_id_base, execute_branch_num)
                            cul = json.dumps(branch, indent=4)
                            executor = ThreadPoolExecutor(max_workers=None)
                            future = executor.submit(self.execute, cul, is_branch=True, command_id_base=id_base)
                            futures.append(future)
                            execute_branch_num += 1
                        for future in futures:
                            results.append(future.result())
                        executor.shutdown()
                        for x in range(len(c["branch_list"])):
                            j = json.loads(results[x][1])
                            c["branch_list"][x] = j
                    
                command_unit_list = json.dumps(d, indent=4)    
                self.command_result[execute_id] = "Execute({}): Success".format(execute_id)
                self.logger.info(self.command_result[execute_id])

            except Exception as e:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.command_result[execute_id] = "Execute:{}".format(e)
                self.logger.error(self.command_result[execute_id])
                command_unit_list = json.dumps(d, indent=4)
                return (status,command_unit_list)

        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            self.command_result[execute_id] = "Execute:Engine_status_is_false"
            self.logger.error(self.command_result[execute_id])
            return (status, command_unit_list)
        
        status = RoIS_HRI.ReturnCode_t.OK.value
        if is_branch == True:
            self.logger.info("Execute:this is branch")
        else:
            self.logger.info("status:{},command_unit_list:{}".format(status,command_unit_list))
            # self.logger.info("command_ids: {}".format(self.command_result))
        return (status, command_unit_list)

    def get_command_result(self, command_id, condition):
        if self._engine.state is True:
            # command_idからサブHRIエンジンを判別し，そのエンジンのget_command_resultを実行する
            e = command_id.split('-')
            engine_name = e[0]
            # サブエンジンの場合
            if engine_name in self.sub_engine.keys():
                try:
                    (s, results) = self.sub_engine[engine_name].get_command_result(command_id, condition)
                    status = s.value
                    if s == RoIS_HRI.ReturnCode_t.OK:
                        self.logger.info("Get_Command_Result({}):Status_of_get_command_result_in_sub_engine_is_{}".format(command_id,s))
                    else:
                        self.logger.error("Get_Command_Result({}):Status_of_get_command_result_in_sub_engine_is_{}".format(command_id,s))
                except:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    results = ["Cannot_connect_to_the_engine[{}]".format(e[0])]
                    self.logger.error("Get_Command_Result({}):Cannot_connect_to_the_get_command_result_in_[{}]_engine".format(command_id,e[0]))
            # メインエンジン(自分自身)の場合
            elif engine_name == self.my_engine_name:
                if command_id in self.command_result.keys():
                    status = RoIS_HRI.ReturnCode_t.OK.value
                    results = [self.command_result[command_id]]
                    self.logger.info("Get_Command_Result({}):Success <results:{}>".format(command_id,results))
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    results = ["Command_id({})_is_wrong".format(command_id)]
                    self.logger.error("Get_Command_Result({}):Command_id_is_wrong".format(command_id))
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                results = ["Engine[{}]_is_not_registered".format(e[0])]
                self.logger.error("Get_Command_Result({}):Engine[{}]_is_not_registered".format(command_id,e[0]))
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            results = ["Engine_state_is_false"]
            self.logger.error("Get_Command_Result({}):Engine_status_is_false".format(command_id))
        return (status, results)


class QueryIF(RoIS_HRI.QueryIF):
    """
    class QueryIF(object):
    """

    def __init__(self, Engine):
        self._engine = Engine

    def query(self, query_type, condition):
        if self._engine.state is True:
            # サブHRIエンジンを呼ぶ必要はない
            status = RoIS_HRI.ReturnCode_t.OK.value
            profile = message_profile.Analyze_Component_Profile(query_type)
            self.component_profile = profile.get_profile()
            results = self.component_profile
            self.logger.info("Query({}):Success:{}:{}".format(query_type,status,results))
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            results = [" "]
            self.logger.error("Query({}):Engine_status_is_false".format(query_type))
        return (status, results)


class EventIF(RoIS_HRI.EventIF):
    """
    class QueryIF(object):
    """

    def __init__(self, Engine):
        self._engine = Engine

    def subscribe(self, event_type, condition):
        if self._engine.state is True:
            # subscribe_id = "{}-{}".format(self.my_engine_name, self.subscribe_id_num) 
            # # サブエンジンのsubscribeも同時に行うためidは全て共通なものにする
            subscribe_id = self.create_new_id("subscribe")
            self.subscribed_event[subscribe_id] = event_type
            try:
                for x in self.sub_engine.keys():
                    self.sub_engine[x].subscribe(event_type, condition)
                status = RoIS_HRI.ReturnCode_t.OK.value
                self.logger.info("Subscribe({}):Success <subscribed_event:{}>".format(event_type, self.subscribed_event))
            except:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.logger.error("Subscribe({}):Cannot_run_Subscribe_in_sub_engine".format(event_type))
                # subscribe_id = "{}-00".format(self.my_engine_name)
                subscribe_id = "00"
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            # subscribe_id = "{}-00".format(self.my_engine_name)
            subscribe_id = "00"
            self.logger.error("Subscribe({}):Engine_status_is_false <subscribed_event:{}>".format(event_type,self.subscribed_event))
        return (status, subscribe_id)

    def unsubscribe(self, subscribe_id):
        if self._engine.state is True:
            if subscribe_id in self.subscribed_event.keys():
                del self.subscribed_event[subscribe_id]
                try:
                    for x in self.sub_engine.keys():
                        self.sub_engine[x].unsubscribe(subscribe_id)
                    status = RoIS_HRI.ReturnCode_t.OK.value
                    self.logger.info("Unsubscribe({}):Success <subscribed_event:{}>".format(subscribe_id,self.subscribed_event))
                except:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    self.logger.error("Unsubscribe({}):Cannot_run_Unsubscribe_in_sub_engine".format(subscribe_id))
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                self.logger.error("Unsubscribe({}):Subscribe_id_is_wrong(subscribed_event:{})".format(subscribe_id,self.subscribed_event))
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            self.logger.error("Unsubscribe({}):Engine_status_is_false(subscribed_event:{})".format(subscribe_id,self.subscribed_event))
        return status

    def get_event_detail(self, event_id, condition):
        if self._engine.state is True:
            e = event_id.split('-')
            engine_name = e[0]
            # サブエンジンの場合
            if engine_name in self.sub_engine.keys():
                try:
                    (s, results) = self.sub_engine[engine_name].get_event_detail(event_id, condition)
                    status = s.value
                    if s == RoIS_HRI.ReturnCode_t.OK:
                        self.logger.info("Get_Event_Detail({}):Status_of_Get_Event_Detail_in_sub_engine_is_{}".format(event_id,s))
                    else:
                        self.logger.error("Get_Event_Detail({}):Status_of_Get_Event_Detail_in_sub_engine_is_{}".format(event_id,s))
                except:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    results = ["Cannot_connect_to_the_engine[{}]".format(e[0])]
                    self.logger.error("Get_Event_Detail({}):Cannot_connect_to_the_Get_Event_Detail_in_[{}]_engine".format(event_id,e[0]))
            # メインエンジン(自分自身)の場合
            elif engine_name == self.my_engine_name:
                if event_id in self.event_detail.keys():
                    status = RoIS_HRI.ReturnCode_t.OK.value
                    results = self.event_detail[event_id]
                    self.logger.info("Get_Event_Detail({}):Success <results:{}>".format(event_id,results))
                else:
                    status = RoIS_HRI.ReturnCode_t.ERROR.value
                    results = ["Event_id({})_is_wrong".format(event_id)]
                    self.logger.error("Get_Event_Detail({}):Event_id_is_wrong".format(event_id))
            else:
                status = RoIS_HRI.ReturnCode_t.ERROR.value
                results = ["Engine[{}]_is_not_registered".format(e[0])]
                self.logger.error("Get_Event_Detail({}):Engine[{}]_is_not_registered".format(event_id,e[0]))
        else:
            status = RoIS_HRI.ReturnCode_t.ERROR.value
            results = ["Engine_state_is_false"]
            self.logger.error("Get_Event_Detail({}):Engine_status_is_false".format(event_id))
        return (status, results)


class IF(SystemIF, CommandIF, QueryIF, EventIF, Service_Application_Base_sample.Service_Application_Base):
    """IF
    """
    def __init__(self, Engine, engine_profile_file, client_info, my_engine_urn=None, logger=None):
        self._engine = Engine

        p = message_profile.Analyze_Engine_Profile(engine_profile_file, my_engine_urn)
        (self.engine_profile, self.engine_and_component ,self.component_list) = p.analysis()
        self.engine_list = list(self.engine_and_component.keys())
        m = self.engine_list[0].split(':')
        self.my_engine_name = m[6]
        self.init_logger(self.my_engine_name,logger)
        self.init_vars()
        self.init_instance(client_info)
        
        Service_Application_Base_sample.Service_Application_Base.__init__(self,logger=self.logger)

        # sub_engine connection_test
        for x in self.sub_engine.keys():
            for i in range(3):
                try:
                    c = self.sub_engine[x].connect()
                    self.logger.info("Init: Connect_to_[{}]".format(x))
                    self.logger.info("Init: Result_of_connect".format(c))
                except Exception as e1:
                    if i != 2:
                        self.logger.error("Init: {}".format(str(e1)))
                        self.logger.error("Init: Try_again_to_connect_to_[{}]".format(x))
                        time.sleep(1)
                    else:
                        self.logger.error("Init: Cannot_connect_to_[{}]".format(x))
                        sys.exit()
                else:
                    break
            
        # component connection_test
        for y in self.component_client.keys():
            for j in range(3):
                try:
                    if y == 'SystemInformation':
                        (status, e_status, operable_time) = self.component_client[y].engine_status()
                        self.logger.info("Init: Result_of_component_status [{}]".format(e_status))
                    else:
                        cs = self.component_client[y].component_status()
                        self.logger.info("Init: Result_of_component_status [{}]".format(cs[1]))
                    # cs = self.component_client[y].component_status()
                    # self.logger.info("Init: Result_of_component_status [{}]".format(cs[1]))
                    self.logger.info("Init: Connect_to_[{}]".format(y))
                except Exception as e2:
                    if j != 2:
                        self.logger.error("Init: {}".format(str(e2)))
                        self.logger.error("Init: Try_again_to_connect_to_[{}]".format(y))
                        time.sleep(1)
                    else:
                        self.logger.error("Init: Cannot_connect_to_[{}]".format(y))
                        sys.exit()
                else:
                    break
        
        self.lock = threading.Lock()
        self.th_mon = threading.Thread(target=self.monitor_event, daemon=True)
        self.th_mon.start()

        if len(self.sub_engine) > 0:
            self.th_mon_sub = threading.Thread(target=self.monitor_event_from_sub_engine, daemon=True)        
            self.th_mon_sub.start()
        else:
            pass

        self.logger.info("main_engine_server: IF init completed")
    
    def init_instance(self, client_info):
        # 2層以内のエンジンの階層構造を想定している
        self.main_event_q = queue.Queue() # check event from main engine
        self.sub_event_q = queue.Queue() # check event from sub engine
        self.sub_engine = {}
        self.component_client = {}
        event_occur_component = ['PersonDetection','PersonLocalization','PersonIdentification','FaceDetection','FaceLocalization',
                                'SoundDetection','SoundLocalization','SpeechRecognition','GestureRecognition']

        with open("{}.json".format(client_info),"r") as f:
            d = json.load(f)
            # print(d)
            try:
                for x in self.engine_list[1:]:
                    # print(x)
                    s = x.split(':')
                    s_name = s[6]
                    s_module = importlib.import_module("pyrois_common.{}".format(str(d[x]["module"])))
                    s_method = getattr(s_module, d[x]["class"])
                    self.sub_engine[s_name] = s_method(d[x]["url"],logger=self.logger_client,event_queue=self.sub_event_q)
                self.logger.info("self.sub_engine: {}".format(str(self.sub_engine)))
                for y in self.engine_and_component[self.engine_list[0]]:
                    # print(x)
                    c = y.split(':')
                    c_name = c[6]
                    c_module = importlib.import_module("pyrois_common.{}".format(d[y]["module"])) # PYTHONPATHでコンポーネントのディレクトリ指定　export PYTHONPATH="$(pwd):$PYTHONPATH"
                    # c_module = importlib.import_module("{}".format(d[y]["module"])) 
                    c_method = getattr(c_module, d[y]["class"])
                    if c_name in event_occur_component:
                        self.component_client[c_name] = c_method(d[y]["url"],self.main_event_q)
                    else:
                        self.component_client[c_name] = c_method(d[y]["url"])
                self.logger.info("self.component_client: {}".format(str(self.component_client)))
            except Exception as e:
                self.logger.error("Init_instance(HRI_Component): {}".format(str(e)))
                sys.exit()       

    def init_logger(self, engine_name, logger):
        if logger is not None:
            self.logger = logger
        else:
            self.dt = datetime.now()
            self.dt_format = self.dt.strftime("%Y%m%d-%H%M")
            self.os = platform.system()
            self.logger = logging.getLogger('[{}]_Engine: HRI_Engine_sample.py'.format(engine_name))
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.fh = logging.FileHandler('{}.log'.format(self.dt_format))
            self.fh.setLevel(logging.DEBUG)
            self.fh.setFormatter(formatter)
            self.logger.addHandler(self.fh)

            self.ch = logging.StreamHandler()
            self.ch.setLevel(logging.ERROR)
            self.ch.setFormatter(formatter)
            self.logger.addHandler(self.ch)
        
        self.logger_client = logging.getLogger('[{}]_Engine: HRI_Engine_client_sample.py'.format(engine_name))
        self.logger_client.setLevel(logging.DEBUG)
        self.logger_client.addHandler(self.fh)
        self.logger_client.addHandler(self.ch)

        self.logger.debug("[{}]_Server running".format(engine_name))
        self.logger.info("This_logger_has_also_logs_in_Service_Application_Base_sample.py")
    
    def init_vars(self):
        self.command_id_num = 0
        self.command_result = {}
        self.subscribe_id_num = 0
        self.subscribed_event = {}
        self.error_id_num = 0
        self.error_detail = {}
        self.event_id_num = 0
        self.binding = []
        self.component_profile = []
        self.event_detail = {}
        self.execute_id_num = 0

    def analyze_component_status(self, component, command_id):
        d = deque([],2)
        error_id = self.create_new_id("error")
        e = [RoIS_Common.Component_Status.BUSY, RoIS_Common.Component_Status.READY]
        while True:
            # 現状ではどのコンポーネントの実行が終了したか分からない．
            with self.lock:
                (_, c_status) = component.component_status()
                d.append(c_status)
            # print(d)

            if c_status == RoIS_Common.Component_Status.ERROR:
                with self.lock:
                    # self.notify_error(error_id, RoIS_Service.ErrorType.COMPONENT_INTERNEL_ERROR.value)
                    # self.logger.info("analyze_component_status:notify_error")
                    # self.error_detail[error_id] = "component_status_is_error"
                    self.completed(command_id, RoIS_Service.Completed_Status.ERROR.value)
                    self.logger.error("analyze_component_status:completed error")
                    
                return

            if len(d) and list(d) == e:
                with self.lock:
                    self.completed(command_id, RoIS_Service.Completed_Status.OK.value)
                    self.logger.info("analyze_component_status:completed")
                return
            time.sleep(0.5)

    def monitor_event(self):
        self.logger.info("monitor_event:start")
        while True:
            x = self.main_event_q.get()
            # print(x)
            event_type = x[0]

            event_id = self.create_new_id("event")
            #self.logger.info("monitor_event:eventtype({}),subscribed_event({})".format(event_type, self.subscribed_event))

            if event_type in self.subscribed_event.values():
                subscribe_id = [k for k, v in self.subscribed_event.items() if v == event_type ]
                for idx in subscribe_id:
                    self.notify_event(event_id, event_type, idx, datetime.now().isoformat())
                self.event_detail[event_id] = x
                self.logger.debug("event_detail:{}".format(x))
                self.logger.info("monitor_event:notify_event(subscribe_id:{})".format(subscribe_id))
            else:
                self.logger.info("monitor_event:This_event({})_is_not_subscribed".format(event_type))

    def monitor_event_from_sub_engine(self):
        while True:
            (params, methodname) = self.sub_event_q.get()
            if methodname == 'completed':
                status = params[1].value
                self.completed(params[0], status)
            elif methodname == 'notify_error':
                error_type = params[1].value
                self.notify_error(params[0], error_type)
            elif methodname == 'notify_event':
                self.notify_event(params[0], params[1], params[2], params[3])
            else:
                print("methodname={}".format(methodname))
                pass
    
    def create_new_id(self, id_type, command_id_base=None, command_num=None, is_branch=False):
        with self.lock:
            if id_type == "command":
                self.command_id_num += 1
                command_id = "{}-{}".format(self.my_engine_name, self.command_id_num)
                return command_id
            elif id_type == "execute":
                if command_num == None:
                    if is_branch == False:
                        self.execute_id_num += 1    
                    command_id = "{}-exe-{}".format(self.my_engine_name, self.execute_id_num)
                else:
                    if command_id_base == None:
                        command_id = "{}-exe-{}-{}".format(self.my_engine_name, self.execute_id_num, command_num)
                    else:
                        command_id = "{}-exe-{}-{}-{}".format(self.my_engine_name, self.execute_id_num, command_id_base, command_num)
                return command_id
            elif id_type == "subscribe":
                self.subscribe_id_num += 1
                subscribe_id = str(self.subscribe_id_num)
                return subscribe_id
            elif id_type == "event":
                self.event_id_num += 1
                event_id = "{}-{}".format(self.my_engine_name, self.event_id_num)
                return event_id
            elif id_type == "error":
                self.error_id_num += 1
                error_id = "{}-{}".format(self.my_engine_name, self.error_id_num)
                return error_id
            else:
                return False
        
    def check_branch(self, command_unit_list_dict, execute_id):
        branch_list_num = 0
        is_correct = True
        command_list = command_unit_list_dict["command_unit_list"]
        for command in command_list:
            if "branch_list" in command.keys():
                branch_list_num += 1
                all_branch_comprefs = []
                branch_num = 0
                all_branch_comprefs = {}
                for branch in command["branch_list"]:
                    branch_num += 1
                    branch_command_list = branch["command_list"]
                    component_refs = [branch_command["component_ref"] for branch_command in branch_command_list if branch_command["command_type"] == "set_parameter"]
                    all_branch_comprefs[branch_num] = component_refs
                for combi in itertools.combinations(all_branch_comprefs.keys(),2):
                    common = set(all_branch_comprefs[combi[0]]).intersection(set(all_branch_comprefs[combi[1]]))
                    if len(common) > 0:
                        is_correct = False
                        self.logger.error("Execute({}) [BranchList_num:{}, Branch_Combination:{}, Same_Components:{}]: Cannot access the set_parameter in the same component from different branches.".format(execute_id,branch_list_num,combi,common))
        if is_correct == False:
            return False
        else:
            return True


class MyHRIE:
    """IF_Server
    """
    def __init__(self):
        self.state = False


def test_engine(port, engine_profile_file=None, client_info=None, my_engine_urn=None, logger=None):
    """test_engine
    """
    IF_server.IF_server(port).run(IF(MyHRIE(), engine_profile_file, client_info, my_engine_urn, logger))

if __name__ == "__main__":
    # コマンドラインでの実行の場合はloggerの指定は厳しい
    args = sys.argv
    if len(args) == 6:
        print(args)
        args[1] = int(args[1])
        for i in range(len(args)):
            if args[i] == "None":
                args[i] = None
            else:
                pass
        print(args)
        test_engine(*args[1:])
        del sys.argv[1:]
    else:
        print("The number of arguments is wrong. The argument types are [port, engine_profile_file, client_info, my_engine_urn, logger].")
        sys.exit()



# export PYTHONPATH="$(pwd)/pyRoIS_higashi:$PYTHONPATH"
# python3 HRI_Engine_sample.py 8000 engine_profile_gazebo client_info_gazebo None None   
# ^ pyRoIS_higashiディレクトリに移動しないと実行できないが、移動すると実行できなくなる 親ディレクトリから子ディレクトリの実行はできないか

# python3 -c "from pyRoIS_higashi import HRI_Engine_sample; HRI_Engine_sample.test_engine(8000,"engine_profile_gazebo", "client_info_gazebo", None, None)"
# ^ もう一つの手段 ただし、実行結果は上記方法と同様  pyRoIS_higashiディレクトリ内での実行になってしまう