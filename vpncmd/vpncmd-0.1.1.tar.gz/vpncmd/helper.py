class VPN_Server_VPN_Bridge_Management_For_Entire_Server:
    def About(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.1_.22About.22:_Display_the_version_information
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("About", *_cmd)

    def ServerInfoGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.2_.22ServerInfoGet.22:_Get_server_information
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ServerInfoGet", *_cmd)

    def ServerStatusGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.3_.22ServerStatusGet.22:_Get_Current_Server_Status
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ServerStatusGet", *_cmd)

    def ListenerCreate(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.4_.22ListenerCreate.22:_Create_New_TCP_Listener
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("ListenerCreate", *_cmd)

    def ListenerDelete(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.5_.22ListenerDelete.22:_Delete_TCP_Listener
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("ListenerDelete", *_cmd)

    def ListenerList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.6_.22ListenerList.22:_Get_List_of_TCP_Listeners
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ListenerList", *_cmd)

    def ListenerEnable(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.7_.22ListenerEnable.22:_Begin_TCP_Listener_Operation
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("ListenerEnable", *_cmd)

    def ListenerDisable(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.8_.22ListenerDisable.22:_Stop_TCP_Listener_Operation
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("ListenerDisable", *_cmd)

    def ServerPasswordSet(self, password=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.9_.22ServerPasswordSet.22:_Set_VPN_Server_Administrator_Password
        _cmd = [_ for _ in (None, password) if _]
        return self.cmd("ServerPasswordSet", *_cmd)

    def ClusterSettingGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.10_.22ClusterSettingGet.22:_Get_Clustering_Configuration_of_Current_VPN_Server
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ClusterSettingGet", *_cmd)

    def ClusterSettingStandalone(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.11_.22ClusterSettingStandalone.22:_Set_VPN_Server_Type_as_Standalone
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ClusterSettingStandalone", *_cmd)

    def ClusterSettingController(self, _WEIGHT=None, _ONLY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.12_.22ClusterSettingController.22:_Set_VPN_Server_Type_as_Cluster_Controller
        _cmd = [_ for _ in (None, "/WEIGHT:"+_WEIGHT if _WEIGHT else None, "/ONLY:"+_ONLY if _ONLY else None) if _]
        return self.cmd("ClusterSettingController", *_cmd)

    def ClusterSettingMember(self, server_port=None, _IP=None, _PORTS=None, _PASSWORD=None, _WEIGHT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.13_.22ClusterSettingMember.22:_Set_VPN_Server_Type_as_Cluster_Member
        _cmd = [_ for _ in (None, server_port, "/IP:"+_IP if _IP else None, "/PORTS:"+_PORTS if _PORTS else None, "/PASSWORD:"+_PASSWORD if _PASSWORD else None, "/WEIGHT:"+_WEIGHT if _WEIGHT else None) if _]
        return self.cmd("ClusterSettingMember", *_cmd)

    def ClusterMemberList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.14_.22ClusterMemberList.22:_Get_List_of_Cluster_Members
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ClusterMemberList", *_cmd)

    def ClusterMemberInfoGet(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.15_.22ClusterMemberInfoGet.22:_Get_Cluster_Member_Information
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("ClusterMemberInfoGet", *_cmd)

    def ClusterMemberCertGet(self, id=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.16_.22ClusterMemberCertGet.22:_Get_Cluster_Member_Certificate
        _cmd = [_ for _ in (None, id, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("ClusterMemberCertGet", *_cmd)

    def ClusterConnectionStatusGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.17_.22ClusterConnectionStatusGet.22:_Get_Connection_Status_to_Cluster_Controller
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ClusterConnectionStatusGet", *_cmd)

    def ServerCertGet(self, cert=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.18_.22ServerCertGet.22:_Get_SSL_Certificate_of_VPN_Server
        _cmd = [_ for _ in (None, cert) if _]
        return self.cmd("ServerCertGet", *_cmd)

    def ServerKeyGet(self, key=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.19_.22ServerKeyGet.22:_Get_SSL_Certificate_Private_Key_of_VPN_Server
        _cmd = [_ for _ in (None, key) if _]
        return self.cmd("ServerKeyGet", *_cmd)

    def ServerCertSet(self, _LOADCERT=None, _LOADKEY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.20_.22ServerCertSet.22:_Set_SSL_Certificate_and_Private_Key_of_VPN_Server
        _cmd = [_ for _ in (None, "/LOADCERT:"+_LOADCERT if _LOADCERT else None, "/LOADKEY:"+_LOADKEY if _LOADKEY else None) if _]
        return self.cmd("ServerCertSet", *_cmd)

    def ServerCipherGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.21_.22ServerCipherGet.22:_Get_the_Encrypted_Algorithm_Used_for_VPN_Communication.
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ServerCipherGet", *_cmd)

    def ServerCipherSet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.22_.22ServerCipherSet.22:_Set_the_Encrypted_Algorithm_Used_for_VPN_Communication.
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("ServerCipherSet", *_cmd)

    def Debug(self, id=None, _ARG=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.23_.22Debug.22:_Execute_a_Debug_Command
        _cmd = [_ for _ in (None, id, "/ARG:"+_ARG if _ARG else None) if _]
        return self.cmd("Debug", *_cmd)

    def Crash(self, yes=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.24_.22Crash.22:_Raise_a_error_on_the_VPN_Server_.2F_Bridge_to_terminate_the_process_forcefully.
        _cmd = [_ for _ in (None, yes) if _]
        return self.cmd("Crash", *_cmd)

    def Flush(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.25_.22Flush.22:_Save_All_Volatile_Data_of_VPN_Server_.2F_Bridge_to_the_Configuration_File
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Flush", *_cmd)

    def KeepEnable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.26_.22KeepEnable.22:_Enable_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("KeepEnable", *_cmd)

    def KeepDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.27_.22KeepDisable.22:_Disable_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("KeepDisable", *_cmd)

    def KeepSet(self, _HOST=None, _PROTOCOL=None, _INTERVAL=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.28_.22KeepSet.22:_Set_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, "/HOST:"+_HOST if _HOST else None, "/PROTOCOL:"+_PROTOCOL if _PROTOCOL else None, "/INTERVAL:"+_INTERVAL if _INTERVAL else None) if _]
        return self.cmd("KeepSet", *_cmd)

    def KeepGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.29_.22KeepGet.22:_Get_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("KeepGet", *_cmd)

    def SyslogEnable(self, _1_2_3=None, _HOST=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.30_.22SyslogEnable.22:_Set_syslog_Send_Function
        _cmd = [_ for _ in (None, _1_2_3, "/HOST:"+_HOST if _HOST else None) if _]
        return self.cmd("SyslogEnable", *_cmd)

    def SyslogDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.31_.22SyslogDisable.22:_Disable_syslog_Send_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SyslogDisable", *_cmd)

    def SyslogGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.32_.22SyslogGet.22:_Get_syslog_Send_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SyslogGet", *_cmd)

    def ConnectionList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.33_.22ConnectionList.22:_Get_List_of_TCP_Connections_Connecting_to_the_VPN_Server
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ConnectionList", *_cmd)

    def ConnectionGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.34_.22ConnectionGet.22:_Get_Information_of_TCP_Connections_Connecting_to_the_VPN_Server
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("ConnectionGet", *_cmd)

    def ConnectionDisconnect(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.35_.22ConnectionDisconnect.22:_Disconnect_TCP_Connections_Connecting_to_the_VPN_Server
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("ConnectionDisconnect", *_cmd)

    def BridgeDeviceList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.36_.22BridgeDeviceList.22:_Get_List_of_Network_Adapters_Usable_as_Local_Bridge
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("BridgeDeviceList", *_cmd)

    def BridgeList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.37_.22BridgeList.22:_Get_List_of_Local_Bridge_Connection
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("BridgeList", *_cmd)

    def BridgeCreate(self, hubname=None, _DEVICE=None, _TAP=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.38_.22BridgeCreate.22:_Create_Local_Bridge_Connection
        _cmd = [_ for _ in (None, hubname, "/DEVICE:"+_DEVICE if _DEVICE else None, "/TAP:"+_TAP if _TAP else None) if _]
        return self.cmd("BridgeCreate", *_cmd)

    def BridgeDelete(self, hubname=None, _DEVICE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.39_.22BridgeDelete.22:_Delete_Local_Bridge_Connection
        _cmd = [_ for _ in (None, hubname, "/DEVICE:"+_DEVICE if _DEVICE else None) if _]
        return self.cmd("BridgeDelete", *_cmd)

    def Caps(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.40_.22Caps.22:_Get_List_of_Server_Functions.2FCapability
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Caps", *_cmd)

    def Reboot(self, _RESETCONFIG=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.41_.22Reboot.22:_Reboot_VPN_Server_Service
        _cmd = [_ for _ in (None, "/RESETCONFIG:"+_RESETCONFIG if _RESETCONFIG else None) if _]
        return self.cmd("Reboot", *_cmd)

    def ConfigGet(self, path=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.42_.22ConfigGet.22:_Get_the_current_configuration_of_the_VPN_Server
        _cmd = [_ for _ in (None, path) if _]
        return self.cmd("ConfigGet", *_cmd)

    def ConfigSet(self, path=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.43_.22ConfigSet.22:_Write_Configuration_File_to_VPN_Server
        _cmd = [_ for _ in (None, path) if _]
        return self.cmd("ConfigSet", *_cmd)

    def RouterList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.44_.22RouterList.22:_Get_List_of_Virtual_Layer_3_Switches
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("RouterList", *_cmd)

    def RouterAdd(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.45_.22RouterAdd.22:_Define_New_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("RouterAdd", *_cmd)

    def RouterDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.46_.22RouterDelete.22:_Delete_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("RouterDelete", *_cmd)

    def RouterStart(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.47_.22RouterStart.22:_Start_Virtual_Layer_3_Switch_Operation
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("RouterStart", *_cmd)

    def RouterStop(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.48_.22RouterStop.22:_Stop_Virtual_Layer_3_Switch_Operation
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("RouterStop", *_cmd)

    def RouterIfList(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.49_.22RouterIfList.22:_Get_List_of_Interfaces_Registered_on_the_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("RouterIfList", *_cmd)

    def RouterIfAdd(self, name=None, _HUB=None, _IP=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.50_.22RouterIfAdd.22:_Add_Virtual_Interface_to_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name, "/HUB:"+_HUB if _HUB else None, "/IP:"+_IP if _IP else None) if _]
        return self.cmd("RouterIfAdd", *_cmd)

    def RouterIfDel(self, name=None, _HUB=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.51_.22RouterIfDel.22:_Delete_Virtual_Interface_of_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name, "/HUB:"+_HUB if _HUB else None) if _]
        return self.cmd("RouterIfDel", *_cmd)

    def RouterTableList(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.52_.22RouterTableList.22:_Get_List_of_Routing_Tables_of_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("RouterTableList", *_cmd)

    def RouterTableAdd(self, name=None, _NETWORK=None, _GATEWAY=None, _METRIC=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.53_.22RouterTableAdd.22:_Add_Routing_Table_Entry_for_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name, "/NETWORK:"+_NETWORK if _NETWORK else None, "/GATEWAY:"+_GATEWAY if _GATEWAY else None, "/METRIC:"+_METRIC if _METRIC else None) if _]
        return self.cmd("RouterTableAdd", *_cmd)

    def RouterTableDel(self, name=None, _NETWORK=None, _GATEWAY=None, _METRIC=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.54_.22RouterTableDel.22:_Delete_Routing_Table_Entry_of_Virtual_Layer_3_Switch
        _cmd = [_ for _ in (None, name, "/NETWORK:"+_NETWORK if _NETWORK else None, "/GATEWAY:"+_GATEWAY if _GATEWAY else None, "/METRIC:"+_METRIC if _METRIC else None) if _]
        return self.cmd("RouterTableDel", *_cmd)

    def LogFileList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.55_.22LogFileList.22:_Get_List_of_Log_Files
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("LogFileList", *_cmd)

    def LogFileGet(self, name=None, _SERVER=None, _SAVEPATH=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.56_.22LogFileGet.22:_Download_Log_file
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/SAVEPATH:"+_SAVEPATH if _SAVEPATH else None) if _]
        return self.cmd("LogFileGet", *_cmd)

    def HubCreate(self, name=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.57_.22HubCreate.22:_Create_New_Virtual_Hub
        _cmd = [_ for _ in (None, name, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("HubCreate", *_cmd)

    def HubCreateDynamic(self, name=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.58_.22HubCreateDynamic.22:_Create_New_Dynamic_Virtual_Hub_(For_Clustering)
        _cmd = [_ for _ in (None, name, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("HubCreateDynamic", *_cmd)

    def HubCreateStatic(self, name=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.59_.22HubCreateStatic.22:_Create_New_Static_Virtual_Hub_(For_Clustering)
        _cmd = [_ for _ in (None, name, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("HubCreateStatic", *_cmd)

    def HubDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.60_.22HubDelete.22:_Delete_Virtual_Hub
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("HubDelete", *_cmd)

    def HubSetStatic(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.61_.22HubSetStatic.22:_Change_Virtual_Hub_Type_to_Static_Virtual_Hub
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("HubSetStatic", *_cmd)

    def HubSetDynamic(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.62_.22HubSetDynamic.22:_Change_Virtual_Hub_Type_to_Dynamic_Virtual_Hub
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("HubSetDynamic", *_cmd)

    def HubList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.63_.22HubList.22:_Get_List_of_Virtual_Hubs
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("HubList", *_cmd)

    def Hub(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.64_.22Hub.22:_Select_Virtual_Hub_to_Manage
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("Hub", *_cmd)

    def MakeCert(self, _CN=None, _O=None, _OU=None, _C=None, _ST=None, _L=None, _SERIAL=None, _EXPIRES=None, _SIGNCERT=None, _SIGNKEY=None, _SAVECERT=None, _SAVEKEY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.65_.22MakeCert.22:_Create_New_X.509_Certificate_and_Private_Key
        _cmd = [_ for _ in (None, "/CN:"+_CN if _CN else None, "/O:"+_O if _O else None, "/OU:"+_OU if _OU else None, "/C:"+_C if _C else None, "/ST:"+_ST if _ST else None, "/L:"+_L if _L else None, "/SERIAL:"+_SERIAL if _SERIAL else None, "/EXPIRES:"+_EXPIRES if _EXPIRES else None, "/SIGNCERT:"+_SIGNCERT if _SIGNCERT else None, "/SIGNKEY:"+_SIGNKEY if _SIGNKEY else None, "/SAVECERT:"+_SAVECERT if _SAVECERT else None, "/SAVEKEY:"+_SAVEKEY if _SAVEKEY else None) if _]
        return self.cmd("MakeCert", *_cmd)

    def TrafficClient(self, host_port=None, _NUMTCP=None, _TYPE=None, _SPAN=None, _DOUBLE=None, _RAW=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.66_.22TrafficClient.22:_Run_Network_Traffic_Speed_Test_Tool_in_Client_Mode
        _cmd = [_ for _ in (None, host_port, "/NUMTCP:"+_NUMTCP if _NUMTCP else None, "/TYPE:"+_TYPE if _TYPE else None, "/SPAN:"+_SPAN if _SPAN else None, "/DOUBLE:"+_DOUBLE if _DOUBLE else None, "/RAW:"+_RAW if _RAW else None) if _]
        return self.cmd("TrafficClient", *_cmd)

    def TrafficServer(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.67_.22TrafficServer.22:_Run_Network_Traffic_Speed_Test_Tool_in_Server_Mode
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("TrafficServer", *_cmd)

    def Check(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.68_.22Check.22:_Check_whether_SoftEther_VPN_Operation_is_Possible
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Check", *_cmd)

    def IPsecEnable(self, _L2TP=None, _L2TPRAW=None, _ETHERIP=None, _PSK=None, _DEFAULTHUB=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.69_.22IPsecEnable.22:_Enable_or_Disable_IPsec_VPN_Server_Function
        _cmd = [_ for _ in (None, "/L2TP:"+_L2TP if _L2TP else None, "/L2TPRAW:"+_L2TPRAW if _L2TPRAW else None, "/ETHERIP:"+_ETHERIP if _ETHERIP else None, "/PSK:"+_PSK if _PSK else None, "/DEFAULTHUB:"+_DEFAULTHUB if _DEFAULTHUB else None) if _]
        return self.cmd("IPsecEnable", *_cmd)

    def IPsecGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.70_.22IPsecGet.22:_Get_the_Current_IPsec_VPN_Server_Settings
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("IPsecGet", *_cmd)

    def EtherIpClientAdd(self, ID=None, _HUB=None, _USERNAME=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.71_.22EtherIpClientAdd.22:_Add_New_EtherIP_.2F_L2TPv3_over_IPsec_Client_Setting_to_Accept_EthreIP_.2F_L2TPv3_Client_Devices
        _cmd = [_ for _ in (None, ID, "/HUB:"+_HUB if _HUB else None, "/USERNAME:"+_USERNAME if _USERNAME else None, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("EtherIpClientAdd", *_cmd)

    def EtherIpClientDelete(self, ID=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.72_.22EtherIpClientDelete.22:_Delete_an_EtherIP_.2F_L2TPv3_over_IPsec_Client_Setting
        _cmd = [_ for _ in (None, ID) if _]
        return self.cmd("EtherIpClientDelete", *_cmd)

    def EtherIpClientList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.73_.22EtherIpClientList.22:_Get_the_Current_List_of_EtherIP_.2F_L2TPv3_Client_Device_Entry_Definitions
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("EtherIpClientList", *_cmd)

    def OpenVpnEnable(self, yes_no=None, _PORTS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.74_.22OpenVpnEnable.22:_Enable_.2F_Disable_OpenVPN_Clone_Server_Function
        _cmd = [_ for _ in (None, yes_no, "/PORTS:"+_PORTS if _PORTS else None) if _]
        return self.cmd("OpenVpnEnable", *_cmd)

    def OpenVpnGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.75_.22OpenVpnGet.22:_Get_the_Current_Settings_of_OpenVPN_Clone_Server_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("OpenVpnGet", *_cmd)

    def OpenVpnMakeConfig(self, ZIP_FileName=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.76_.22OpenVpnMakeConfig.22:_Generate_a_Sample_Setting_File_for_OpenVPN_Client
        _cmd = [_ for _ in (None, ZIP_FileName) if _]
        return self.cmd("OpenVpnMakeConfig", *_cmd)

    def SstpEnable(self, yes_no=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.77_.22SstpEnable.22:_Enable_.2F_Disable_Microsoft_SSTP_VPN_Clone_Server_Function
        _cmd = [_ for _ in (None, yes_no) if _]
        return self.cmd("SstpEnable", *_cmd)

    def SstpGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.78_.22SstpGet.22:_Get_the_Current_Settings_of_Microsoft_SSTP_VPN_Clone_Server_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SstpGet", *_cmd)

    def ServerCertRegenerate(self, CN=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.79_.22ServerCertRegenerate.22:_Generate_New_Self-Signed_Certificate_with_Specified_CN_(Common_Name)_and_Register_on_VPN_Server
        _cmd = [_ for _ in (None, CN) if _]
        return self.cmd("ServerCertRegenerate", *_cmd)

    def VpnOverIcmpDnsEnable(self, _ICMP=None, _DNS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.80_.22VpnOverIcmpDnsEnable.22:_Enable_.2F_Disable_the_VPN_over_ICMP_.2F_VPN_over_DNS_Server_Function
        _cmd = [_ for _ in (None, "/ICMP:"+_ICMP if _ICMP else None, "/DNS:"+_DNS if _DNS else None) if _]
        return self.cmd("VpnOverIcmpDnsEnable", *_cmd)

    def VpnOverIcmpDnsGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.81_.22VpnOverIcmpDnsGet.22:_Get_Current_Setting_of_the_VPN_over_ICMP_.2F_VPN_over_DNS_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("VpnOverIcmpDnsGet", *_cmd)

    def DynamicDnsGetStatus(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.82_.22DynamicDnsGetStatus.22:_Show_the_Current_Status_of_Dynamic_DNS_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("DynamicDnsGetStatus", *_cmd)

    def DynamicDnsSetHostname(self, hostname=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.83_.22DynamicDnsSetHostname.22:_Set_the_Dynamic_DNS_Hostname
        _cmd = [_ for _ in (None, hostname) if _]
        return self.cmd("DynamicDnsSetHostname", *_cmd)

    def VpnAzureGetStatus(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.84_.22VpnAzureGetStatus.22:_Show_the_current_status_of_VPN_Azure_function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("VpnAzureGetStatus", *_cmd)

    def VpnAzureSetEnable(self, yes_no=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)#6.3.85_.22VpnAzureSetEnable.22:_Enable_.2F_Disable_VPN_Azure_Function
        _cmd = [_ for _ in (None, yes_no) if _]
        return self.cmd("VpnAzureSetEnable", *_cmd)

    def cmd(self, *args, **kwargs):
        pass


class VPN_Server_VPN_Bridge_Management_For_Virtual_Hub:
    def Online(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.1_.22Online.22:_Switch_Virtual_Hub_to_Online
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Online", *_cmd)

    def Offline(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.2_.22Offline.22:_Switch_Virtual_Hub_to_Offline
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Offline", *_cmd)

    def SetMaxSession(self, max_session=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.3_.22SetMaxSession.22:_Set_the_Max_Number_of_Concurrently_Connected_Sessions_for_Virtual_Hub
        _cmd = [_ for _ in (None, max_session) if _]
        return self.cmd("SetMaxSession", *_cmd)

    def SetHubPassword(self, password=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.4_.22SetHubPassword.22:_Set_Virtual_Hub_Administrator_Password
        _cmd = [_ for _ in (None, password) if _]
        return self.cmd("SetHubPassword", *_cmd)

    def SetEnumAllow(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.5_.22SetEnumAllow.22:_Allow_Enumeration_by_Virtual_Hub_Anonymous_Users
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SetEnumAllow", *_cmd)

    def SetEnumDeny(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.6_.22SetEnumDeny.22:_Deny_Enumeration_by_Virtual_Hub_Anonymous_Users
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SetEnumDeny", *_cmd)

    def OptionsGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.7_.22OptionsGet.22:_Get_Options_Setting_of_Virtual_Hubs
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("OptionsGet", *_cmd)

    def RadiusServerSet(self, server_name_port=None, _SECRET=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.8_.22RadiusServerSet.22:_Set_RADIUS_Server_to_use_for_User_Authentication
        _cmd = [_ for _ in (None, server_name_port, "/SECRET:"+_SECRET if _SECRET else None) if _]
        return self.cmd("RadiusServerSet", *_cmd)

    def RadiusServerDelete(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.9_.22RadiusServerDelete.22:_Delete_Setting_to_Use_RADIUS_Server_for_User_Authentication
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("RadiusServerDelete", *_cmd)

    def RadiusServerGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.10_.22RadiusServerGet.22:_Get_Setting_of_RADIUS_Server_Used_for_User_Authentication
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("RadiusServerGet", *_cmd)

    def StatusGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.11_.22StatusGet.22:_Get_Current_Status_of_Virtual_Hub
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("StatusGet", *_cmd)

    def LogGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.12_.22LogGet.22:_Get_Log_Save_Setting_of_Virtual_Hub
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("LogGet", *_cmd)

    def LogEnable(self, security_packet=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.13_.22LogEnable.22:_Enable_Security_Log_or_Packet_Log
        _cmd = [_ for _ in (None, security_packet) if _]
        return self.cmd("LogEnable", *_cmd)

    def LogDisable(self, security_packet=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.14_.22LogDisable.22:_Disable_Security_Log_or_Packet_Log
        _cmd = [_ for _ in (None, security_packet) if _]
        return self.cmd("LogDisable", *_cmd)

    def LogSwitchSet(self, security_packet=None, _SWITCH=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.15_.22LogSwitchSet.22:_Set_Log_File_Switch_Cycle
        _cmd = [_ for _ in (None, security_packet, "/SWITCH:"+_SWITCH if _SWITCH else None) if _]
        return self.cmd("LogSwitchSet", *_cmd)

    def LogPacketSaveType(self, _TYPE=None, _SAVE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.16_.22LogPacketSaveType.22:_Set_Save_Contents_and_Type_of_Packet_to_Save_to_Packet_Log
        _cmd = [_ for _ in (None, "/TYPE:"+_TYPE if _TYPE else None, "/SAVE:"+_SAVE if _SAVE else None) if _]
        return self.cmd("LogPacketSaveType", *_cmd)

    def CAList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.17_.22CAList.22:_Get_List_of_Trusted_CA_Certificates
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("CAList", *_cmd)

    def CAAdd(self, path=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.18_.22CAAdd.22:_Add_Trusted_CA_Certificate
        _cmd = [_ for _ in (None, path) if _]
        return self.cmd("CAAdd", *_cmd)

    def CADelete(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.19_.22CADelete.22:_Delete_Trusted_CA_Certificate
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("CADelete", *_cmd)

    def CAGet(self, id=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.20_.22CAGet.22:_Get_Trusted_CA_Certificate
        _cmd = [_ for _ in (None, id, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("CAGet", *_cmd)

    def CascadeList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.21_.22CascadeList.22:_Get_List_of_Cascade_Connections
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("CascadeList", *_cmd)

    def CascadeCreate(self, name=None, _SERVER=None, _HUB=None, _USERNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.22_.22CascadeCreate.22:_Create_New_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/HUB:"+_HUB if _HUB else None, "/USERNAME:"+_USERNAME if _USERNAME else None) if _]
        return self.cmd("CascadeCreate", *_cmd)

    def CascadeSet(self, name=None, _SERVER=None, _HUB=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.23_.22CascadeSet.22:_Set_the_Destination_for_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/HUB:"+_HUB if _HUB else None) if _]
        return self.cmd("CascadeSet", *_cmd)

    def CascadeGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.24_.22CascadeGet.22:_Get_the_Cascade_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeGet", *_cmd)

    def CascadeDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.25_.22CascadeDelete.22:_Delete_Cascade_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeDelete", *_cmd)

    def CascadeUsernameSet(self, name=None, _USERNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.26_.22CascadeUsernameSet.22:_Set_User_Name_to_Use_Connection_of_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/USERNAME:"+_USERNAME if _USERNAME else None) if _]
        return self.cmd("CascadeUsernameSet", *_cmd)

    def CascadeAnonymousSet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.27_.22CascadeAnonymousSet.22:_Set_User_Authentication_Type_of_Cascade_Connection_to_Anonymous_Authentication
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeAnonymousSet", *_cmd)

    def CascadePasswordSet(self, name=None, _PASSWORD=None, _TYPE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.28_.22CascadePasswordSet.22:_Set_User_Authentication_Type_of_Cascade_Connection_to_Password_Authentication
        _cmd = [_ for _ in (None, name, "/PASSWORD:"+_PASSWORD if _PASSWORD else None, "/TYPE:"+_TYPE if _TYPE else None) if _]
        return self.cmd("CascadePasswordSet", *_cmd)

    def CascadeCertSet(self, name=None, _LOADCERT=None, _LOADKEY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.29_.22CascadeCertSet.22:_Set_User_Authentication_Type_of_Cascade_Connection_to_Client_Certificate_Authentication
        _cmd = [_ for _ in (None, name, "/LOADCERT:"+_LOADCERT if _LOADCERT else None, "/LOADKEY:"+_LOADKEY if _LOADKEY else None) if _]
        return self.cmd("CascadeCertSet", *_cmd)

    def CascadeCertGet(self, name=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.30_.22CascadeCertGet.22:_Get_Client_Certificate_to_Use_for_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("CascadeCertGet", *_cmd)

    def CascadeEncryptEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.31_.22CascadeEncryptEnable.22:_Enable_Encryption_when_Communicating_by_Cascade_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeEncryptEnable", *_cmd)

    def CascadeEncryptDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.32_.22CascadeEncryptDisable.22:_Disable_Encryption_when_Communicating_by_Cascade_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeEncryptDisable", *_cmd)

    def CascadeCompressEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.33_.22CascadeCompressEnable.22:_Enable_Data_Compression_when_Communicating_by_Cascade_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeCompressEnable", *_cmd)

    def CascadeCompressDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.34_.22CascadeCompressDisable.22:_Disable_Data_Compression_when_Communicating_by_Cascade_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeCompressDisable", *_cmd)

    def CascadeProxyNone(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.35_.22CascadeProxyNone.22:_Specify_Direct_TCP.2FIP_Connection_as_the_Connection_Method_of_Cascade_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeProxyNone", *_cmd)

    def CascadeProxyHttp(self, name=None, _SERVER=None, _USERNAME=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.36_.22CascadeProxyHttp.22:_Set_Connection_Method_of_Cascade_Connection_to_be_via_an_HTTP_Proxy_Server
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/USERNAME:"+_USERNAME if _USERNAME else None, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("CascadeProxyHttp", *_cmd)

    def CascadeProxySocks(self, name=None, _SERVER=None, _USERNAME=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.37_.22CascadeProxySocks.22:_Set_Connection_Method_of_Cascade_Connection_to_be_via_an_SOCKS_Proxy_Server
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/USERNAME:"+_USERNAME if _USERNAME else None, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("CascadeProxySocks", *_cmd)

    def CascadeServerCertEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.38_.22CascadeServerCertEnable.22:_Enable_Cascade_Connection_Server_Certificate_Verification_Option
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeServerCertEnable", *_cmd)

    def CascadeServerCertDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.39_.22CascadeServerCertDisable.22:_Disable_Cascade_Connection_Server_Certificate_Verification_Option
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeServerCertDisable", *_cmd)

    def CascadeServerCertSet(self, name=None, _LOADCERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.40_.22CascadeServerCertSet.22:_Set_the_Server_Individual_Certificate_for_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/LOADCERT:"+_LOADCERT if _LOADCERT else None) if _]
        return self.cmd("CascadeServerCertSet", *_cmd)

    def CascadeServerCertDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.41_.22CascadeServerCertDelete.22:_Delete_the_Server_Individual_Certificate_for_Cascade_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeServerCertDelete", *_cmd)

    def CascadeServerCertGet(self, name=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.42_.22CascadeServerCertGet.22:_Get_the_Server_Individual_Certificate_for_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("CascadeServerCertGet", *_cmd)

    def CascadeDetailSet(self, name=None, _MAXTCP=None, _INTERVAL=None, _TTL=None, _HALF=None, _NOQOS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.43_.22CascadeDetailSet.22:_Set_Advanced_Settings_for_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/MAXTCP:"+_MAXTCP if _MAXTCP else None, "/INTERVAL:"+_INTERVAL if _INTERVAL else None, "/TTL:"+_TTL if _TTL else None, "/HALF:"+_HALF if _HALF else None, "/NOQOS:"+_NOQOS if _NOQOS else None) if _]
        return self.cmd("CascadeDetailSet", *_cmd)

    def CascadePolicySet(self, name=None, _NAME=None, _VALUE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.44_.22CascadePolicySet.22:_Set_Cascade_Connection_Session_Security_Policy
        _cmd = [_ for _ in (None, name, "/NAME:"+_NAME if _NAME else None, "/VALUE:"+_VALUE if _VALUE else None) if _]
        return self.cmd("CascadePolicySet", *_cmd)

    def PolicyList(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.45_.22PolicyList.22:_Display_List_of_Security_Policy_Types_and_Settable_Values
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("PolicyList", *_cmd)

    def CascadeStatusGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.46_.22CascadeStatusGet.22:_Get_Current_Cascade_Connection_Status
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeStatusGet", *_cmd)

    def CascadeRename(self, name=None, _NEW=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.47_.22CascadeRename.22:_Change_Name_of_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/NEW:"+_NEW if _NEW else None) if _]
        return self.cmd("CascadeRename", *_cmd)

    def CascadeOnline(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.48_.22CascadeOnline.22:_Switch_Cascade_Connection_to_Online_Status
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeOnline", *_cmd)

    def CascadeOffline(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.49_.22CascadeOffline.22:_Switch_Cascade_Connection_to_Offline_Status
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("CascadeOffline", *_cmd)

    def AccessAdd(self, pass_discard=None, _MEMO=None, _PRIORITY=None, _SRCUSERNAME=None, _DESTUSERNAME=None, _SRCMAC=None, _DESTMAC=None, _SRCIP=None, _DESTIP=None, _PROTOCOL=None, _SRCPORT=None, _DESTPORT=None, _TCPSTATE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.50_.22AccessAdd.22:_Add_Access_List_Rules_(IPv4)
        _cmd = [_ for _ in (None, pass_discard, "/MEMO:"+_MEMO if _MEMO else None, "/PRIORITY:"+_PRIORITY if _PRIORITY else None, "/SRCUSERNAME:"+_SRCUSERNAME if _SRCUSERNAME else None, "/DESTUSERNAME:"+_DESTUSERNAME if _DESTUSERNAME else None, "/SRCMAC:"+_SRCMAC if _SRCMAC else None, "/DESTMAC:"+_DESTMAC if _DESTMAC else None, "/SRCIP:"+_SRCIP if _SRCIP else None, "/DESTIP:"+_DESTIP if _DESTIP else None, "/PROTOCOL:"+_PROTOCOL if _PROTOCOL else None, "/SRCPORT:"+_SRCPORT if _SRCPORT else None, "/DESTPORT:"+_DESTPORT if _DESTPORT else None, "/TCPSTATE:"+_TCPSTATE if _TCPSTATE else None) if _]
        return self.cmd("AccessAdd", *_cmd)

    def AccessAddEx(self, pass_discard=None, _MEMO=None, _PRIORITY=None, _SRCUSERNAME=None, _DESTUSERNAME=None, _SRCMAC=None, _DESTMAC=None, _SRCIP=None, _DESTIP=None, _PROTOCOL=None, _SRCPORT=None, _DESTPORT=None, _TCPSTATE=None, _DELAY=None, _JITTER=None, _LOSS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.51_.22AccessAddEx.22:_Add_Extended_Access_List_Rules_(IPv4:_Delay.2C_Jitter_and_Packet_Loss_Generating)
        _cmd = [_ for _ in (None, pass_discard, "/MEMO:"+_MEMO if _MEMO else None, "/PRIORITY:"+_PRIORITY if _PRIORITY else None, "/SRCUSERNAME:"+_SRCUSERNAME if _SRCUSERNAME else None, "/DESTUSERNAME:"+_DESTUSERNAME if _DESTUSERNAME else None, "/SRCMAC:"+_SRCMAC if _SRCMAC else None, "/DESTMAC:"+_DESTMAC if _DESTMAC else None, "/SRCIP:"+_SRCIP if _SRCIP else None, "/DESTIP:"+_DESTIP if _DESTIP else None, "/PROTOCOL:"+_PROTOCOL if _PROTOCOL else None, "/SRCPORT:"+_SRCPORT if _SRCPORT else None, "/DESTPORT:"+_DESTPORT if _DESTPORT else None, "/TCPSTATE:"+_TCPSTATE if _TCPSTATE else None, "/DELAY:"+_DELAY if _DELAY else None, "/JITTER:"+_JITTER if _JITTER else None, "/LOSS:"+_LOSS if _LOSS else None) if _]
        return self.cmd("AccessAddEx", *_cmd)

    def AccessAdd6(self, pass_discard=None, _MEMO=None, _PRIORITY=None, _SRCUSERNAME=None, _DESTUSERNAME=None, _SRCMAC=None, _DESTMAC=None, _SRCIP=None, _DESTIP=None, _PROTOCOL=None, _SRCPORT=None, _DESTPORT=None, _TCPSTATE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.52_.22AccessAdd6.22:_Add_Access_List_Rules_(IPv6)
        _cmd = [_ for _ in (None, pass_discard, "/MEMO:"+_MEMO if _MEMO else None, "/PRIORITY:"+_PRIORITY if _PRIORITY else None, "/SRCUSERNAME:"+_SRCUSERNAME if _SRCUSERNAME else None, "/DESTUSERNAME:"+_DESTUSERNAME if _DESTUSERNAME else None, "/SRCMAC:"+_SRCMAC if _SRCMAC else None, "/DESTMAC:"+_DESTMAC if _DESTMAC else None, "/SRCIP:"+_SRCIP if _SRCIP else None, "/DESTIP:"+_DESTIP if _DESTIP else None, "/PROTOCOL:"+_PROTOCOL if _PROTOCOL else None, "/SRCPORT:"+_SRCPORT if _SRCPORT else None, "/DESTPORT:"+_DESTPORT if _DESTPORT else None, "/TCPSTATE:"+_TCPSTATE if _TCPSTATE else None) if _]
        return self.cmd("AccessAdd6", *_cmd)

    def AccessAddEx6(self, pass_discard=None, _MEMO=None, _PRIORITY=None, _SRCUSERNAME=None, _DESTUSERNAME=None, _SRCMAC=None, _DESTMAC=None, _SRCIP=None, _DESTIP=None, _PROTOCOL=None, _SRCPORT=None, _DESTPORT=None, _TCPSTATE=None, _DELAY=None, _JITTER=None, _LOSS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.53_.22AccessAddEx6.22:_Add_Extended_Access_List_Rules_(IPv6:_Delay.2C_Jitter_and_Packet_Loss_Generating)
        _cmd = [_ for _ in (None, pass_discard, "/MEMO:"+_MEMO if _MEMO else None, "/PRIORITY:"+_PRIORITY if _PRIORITY else None, "/SRCUSERNAME:"+_SRCUSERNAME if _SRCUSERNAME else None, "/DESTUSERNAME:"+_DESTUSERNAME if _DESTUSERNAME else None, "/SRCMAC:"+_SRCMAC if _SRCMAC else None, "/DESTMAC:"+_DESTMAC if _DESTMAC else None, "/SRCIP:"+_SRCIP if _SRCIP else None, "/DESTIP:"+_DESTIP if _DESTIP else None, "/PROTOCOL:"+_PROTOCOL if _PROTOCOL else None, "/SRCPORT:"+_SRCPORT if _SRCPORT else None, "/DESTPORT:"+_DESTPORT if _DESTPORT else None, "/TCPSTATE:"+_TCPSTATE if _TCPSTATE else None, "/DELAY:"+_DELAY if _DELAY else None, "/JITTER:"+_JITTER if _JITTER else None, "/LOSS:"+_LOSS if _LOSS else None) if _]
        return self.cmd("AccessAddEx6", *_cmd)

    def AccessList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.54_.22AccessList.22:_Get_Access_List_Rule_List
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("AccessList", *_cmd)

    def AccessDelete(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.55_.22AccessDelete.22:_Delete_Rule_from_Access_List
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("AccessDelete", *_cmd)

    def AccessEnable(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.56_.22AccessEnable.22:_Enable_Access_List_Rule
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("AccessEnable", *_cmd)

    def AccessDisable(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.57_.22AccessDisable.22:_Disable_Access_List_Rule
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("AccessDisable", *_cmd)

    def UserList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.58_.22UserList.22:_Get_List_of_Users
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("UserList", *_cmd)

    def UserCreate(self, name=None, _GROUP=None, _REALNAME=None, _NOTE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.59_.22UserCreate.22:_Create_User
        _cmd = [_ for _ in (None, name, "/GROUP:"+_GROUP if _GROUP else None, "/REALNAME:"+_REALNAME if _REALNAME else None, "/NOTE:"+_NOTE if _NOTE else None) if _]
        return self.cmd("UserCreate", *_cmd)

    def UserSet(self, name=None, _GROUP=None, _REALNAME=None, _NOTE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.60_.22UserSet.22:_Change_User_Information
        _cmd = [_ for _ in (None, name, "/GROUP:"+_GROUP if _GROUP else None, "/REALNAME:"+_REALNAME if _REALNAME else None, "/NOTE:"+_NOTE if _NOTE else None) if _]
        return self.cmd("UserSet", *_cmd)

    def UserDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.61_.22UserDelete.22:_Delete_User
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("UserDelete", *_cmd)

    def UserGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.62_.22UserGet.22:_Get_User_Information
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("UserGet", *_cmd)

    def UserAnonymousSet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.63_.22UserAnonymousSet.22:_Set_Anonymous_Authentication_for_User_Auth_Type
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("UserAnonymousSet", *_cmd)

    def UserPasswordSet(self, name=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.64_.22UserPasswordSet.22:_Set_Password_Authentication_for_User_Auth_Type_and_Set_Password
        _cmd = [_ for _ in (None, name, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("UserPasswordSet", *_cmd)

    def UserCertSet(self, name=None, _LOADCERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.65_.22UserCertSet.22:_Set_Individual_Certificate_Authentication_for_User_Auth_Type_and_Set_Certificate
        _cmd = [_ for _ in (None, name, "/LOADCERT:"+_LOADCERT if _LOADCERT else None) if _]
        return self.cmd("UserCertSet", *_cmd)

    def UserCertGet(self, name=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.66_.22UserCertGet.22:_Get_Certificate_Registered_for_Individual_Certificate_Authentication_User
        _cmd = [_ for _ in (None, name, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("UserCertGet", *_cmd)

    def UserSignedSet(self, name=None, _CN=None, _SERIAL=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.67_.22UserSignedSet.22:_Set_Signed_Certificate_Authentication_for_User_Auth_Type
        _cmd = [_ for _ in (None, name, "/CN:"+_CN if _CN else None, "/SERIAL:"+_SERIAL if _SERIAL else None) if _]
        return self.cmd("UserSignedSet", *_cmd)

    def UserRadiusSet(self, name=None, _ALIAS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.68_.22UserRadiusSet.22:_Set_RADIUS_Authentication_for_User_Auth_Type
        _cmd = [_ for _ in (None, name, "/ALIAS:"+_ALIAS if _ALIAS else None) if _]
        return self.cmd("UserRadiusSet", *_cmd)

    def UserNTLMSet(self, name=None, _ALIAS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.69_.22UserNTLMSet.22:_Set_NT_Domain_Authentication_for_User_Auth_Type
        _cmd = [_ for _ in (None, name, "/ALIAS:"+_ALIAS if _ALIAS else None) if _]
        return self.cmd("UserNTLMSet", *_cmd)

    def UserPolicyRemove(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.70_.22UserPolicyRemove.22:_Delete_User_Security_Policy
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("UserPolicyRemove", *_cmd)

    def UserPolicySet(self, name=None, _NAME=None, _VALUE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.71_.22UserPolicySet.22:_Set_User_Security_Policy
        _cmd = [_ for _ in (None, name, "/NAME:"+_NAME if _NAME else None, "/VALUE:"+_VALUE if _VALUE else None) if _]
        return self.cmd("UserPolicySet", *_cmd)

    def UserExpiresSet(self, name=None, _EXPIRES=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.72_.22UserExpiresSet.22:_Set_User's_Expiration_Date
        _cmd = [_ for _ in (None, name, "/EXPIRES:"+_EXPIRES if _EXPIRES else None) if _]
        return self.cmd("UserExpiresSet", *_cmd)

    def GroupList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.73_.22GroupList.22:_Get_List_of_Groups
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("GroupList", *_cmd)

    def GroupCreate(self, name=None, _REALNAME=None, _NOTE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.74_.22GroupCreate.22:_Create_Group
        _cmd = [_ for _ in (None, name, "/REALNAME:"+_REALNAME if _REALNAME else None, "/NOTE:"+_NOTE if _NOTE else None) if _]
        return self.cmd("GroupCreate", *_cmd)

    def GroupSet(self, name=None, _REALNAME=None, _NOTE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.75_.22GroupSet.22:_Set_Group_Information
        _cmd = [_ for _ in (None, name, "/REALNAME:"+_REALNAME if _REALNAME else None, "/NOTE:"+_NOTE if _NOTE else None) if _]
        return self.cmd("GroupSet", *_cmd)

    def GroupDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.76_.22GroupDelete.22:_Delete_Group
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("GroupDelete", *_cmd)

    def GroupGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.77_.22GroupGet.22:_Get_Group_Information_and_List_of_Assigned_Users
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("GroupGet", *_cmd)

    def GroupJoin(self, name=None, _USERNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.78_.22GroupJoin.22:_Add_User_to_Group
        _cmd = [_ for _ in (None, name, "/USERNAME:"+_USERNAME if _USERNAME else None) if _]
        return self.cmd("GroupJoin", *_cmd)

    def GroupUnjoin(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.79_.22GroupUnjoin.22:_Delete_User_from_Group
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("GroupUnjoin", *_cmd)

    def GroupPolicyRemove(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.80_.22GroupPolicyRemove.22:_Delete_Group_Security_Policy
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("GroupPolicyRemove", *_cmd)

    def GroupPolicySet(self, name=None, _NAME=None, _VALUE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.81_.22GroupPolicySet.22:_Set_Group_Security_Policy
        _cmd = [_ for _ in (None, name, "/NAME:"+_NAME if _NAME else None, "/VALUE:"+_VALUE if _VALUE else None) if _]
        return self.cmd("GroupPolicySet", *_cmd)

    def SessionList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.82_.22SessionList.22:_Get_List_of_Connected_Sessions
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SessionList", *_cmd)

    def SessionGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.83_.22SessionGet.22:_Get_Session_Information
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("SessionGet", *_cmd)

    def SessionDisconnect(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.84_.22SessionDisconnect.22:_Disconnect_Session
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("SessionDisconnect", *_cmd)

    def MacTable(self, session_name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.85_.22MacTable.22:_Get_the_MAC_Address_Table_Database
        _cmd = [_ for _ in (None, session_name) if _]
        return self.cmd("MacTable", *_cmd)

    def MacDelete(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.86_.22MacDelete.22:_Delete_MAC_Address_Table_Entry
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("MacDelete", *_cmd)

    def IpTable(self, session_name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.87_.22IpTable.22:_Get_the_IP_Address_Table_Database
        _cmd = [_ for _ in (None, session_name) if _]
        return self.cmd("IpTable", *_cmd)

    def IpDelete(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.88_.22IpDelete.22:_Delete_IP_Address_Table_Entry
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("IpDelete", *_cmd)

    def SecureNatEnable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.89_.22SecureNatEnable.22:_Enable_the_Virtual_NAT_and_DHCP_Server_Function_(SecureNat_Function)
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SecureNatEnable", *_cmd)

    def SecureNatDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.90_.22SecureNatDisable.22:_Disable_the_Virtual_NAT_and_DHCP_Server_Function_(SecureNat_Function)
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SecureNatDisable", *_cmd)

    def SecureNatStatusGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.91_.22SecureNatStatusGet.22:_Get_the_Operating_Status_of_the_Virtual_NAT_and_DHCP_Server_Function_(SecureNat_Function)
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SecureNatStatusGet", *_cmd)

    def SecureNatHostGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.92_.22SecureNatHostGet.22:_Get_Network_Interface_Setting_of_Virtual_Host_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SecureNatHostGet", *_cmd)

    def SecureNatHostSet(self, _MAC=None, _IP=None, _MASK=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.93_.22SecureNatHostSet.22:_Change_Network_Interface_Setting_of_Virtual_Host_of_SecureNAT_Function
        _cmd = [_ for _ in (None, "/MAC:"+_MAC if _MAC else None, "/IP:"+_IP if _IP else None, "/MASK:"+_MASK if _MASK else None) if _]
        return self.cmd("SecureNatHostSet", *_cmd)

    def NatGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.94_.22NatGet.22:_Get_Virtual_NAT_Function_Setting_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("NatGet", *_cmd)

    def NatEnable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.95_.22NatEnable.22:_Enable_Virtual_NAT_Function_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("NatEnable", *_cmd)

    def NatDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.96_.22NatDisable.22:_Disable_Virtual_NAT_Function_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("NatDisable", *_cmd)

    def NatSet(self, _MTU=None, _TCPTIMEOUT=None, _UDPTIMEOUT=None, _LOG=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.97_.22NatSet.22:_Change_Virtual_NAT_Function_Setting_of_SecureNAT_Function
        _cmd = [_ for _ in (None, "/MTU:"+_MTU if _MTU else None, "/TCPTIMEOUT:"+_TCPTIMEOUT if _TCPTIMEOUT else None, "/UDPTIMEOUT:"+_UDPTIMEOUT if _UDPTIMEOUT else None, "/LOG:"+_LOG if _LOG else None) if _]
        return self.cmd("NatSet", *_cmd)

    def NatTable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.98_.22NatTable.22:_Get_Virtual_NAT_Function_Session_Table_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("NatTable", *_cmd)

    def DhcpGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.99_.22DhcpGet.22:_Get_Virtual_DHCP_Server_Function_Setting_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("DhcpGet", *_cmd)

    def DhcpEnable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.100_.22DhcpEnable.22:_Enable_Virtual_DHCP_Server_Function_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("DhcpEnable", *_cmd)

    def DhcpDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.101_.22DhcpDisable.22:_Disable_Virtual_DHCP_Server_Function_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("DhcpDisable", *_cmd)

    def DhcpSet(self, _START=None, _END=None, _MASK=None, _EXPIRE=None, _GW=None, _DNS=None, _DOMAIN=None, _LOG=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.102_.22DhcpSet.22:_Change_Virtual_DHCP_Server_Function_Setting_of_SecureNAT_Function
        _cmd = [_ for _ in (None, "/START:"+_START if _START else None, "/END:"+_END if _END else None, "/MASK:"+_MASK if _MASK else None, "/EXPIRE:"+_EXPIRE if _EXPIRE else None, "/GW:"+_GW if _GW else None, "/DNS:"+_DNS if _DNS else None, "/DOMAIN:"+_DOMAIN if _DOMAIN else None, "/LOG:"+_LOG if _LOG else None) if _]
        return self.cmd("DhcpSet", *_cmd)

    def DhcpTable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.103_.22DhcpTable.22:_Get_Virtual_DHCP_Server_Function_Lease_Table_of_SecureNAT_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("DhcpTable", *_cmd)

    def AdminOptionList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.104_.22AdminOptionList.22:_Get_List_of_Virtual_Hub_Administration_Options
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("AdminOptionList", *_cmd)

    def AdminOptionSet(self, name=None, _VALUE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.105_.22AdminOptionSet.22:_Set_Values_of_Virtual_Hub_Administration_Options
        _cmd = [_ for _ in (None, name, "/VALUE:"+_VALUE if _VALUE else None) if _]
        return self.cmd("AdminOptionSet", *_cmd)

    def ExtOptionList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.106_.22ExtOptionList.22:_Get_List_of_Virtual_Hub_Extended_Options
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("ExtOptionList", *_cmd)

    def ExtOptionSet(self, name=None, _VALUE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.107_.22ExtOptionSet.22:_Set_a_Value_of_Virtual_Hub_Extended_Options
        _cmd = [_ for _ in (None, name, "/VALUE:"+_VALUE if _VALUE else None) if _]
        return self.cmd("ExtOptionSet", *_cmd)

    def CrlList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.108_.22CrlList.22:_Get_List_of_Certificates_Revocation_List
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("CrlList", *_cmd)

    def CrlAdd(self, _SERIAL=None, _MD5=None, _SHA1=None, _CN=None, _O=None, _OU=None, _C=None, _ST=None, _L=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.109_.22CrlAdd.22:_Add_a_Revoked_Certificate
        _cmd = [_ for _ in (None, "/SERIAL:"+_SERIAL if _SERIAL else None, "/MD5:"+_MD5 if _MD5 else None, "/SHA1:"+_SHA1 if _SHA1 else None, "/CN:"+_CN if _CN else None, "/O:"+_O if _O else None, "/OU:"+_OU if _OU else None, "/C:"+_C if _C else None, "/ST:"+_ST if _ST else None, "/L:"+_L if _L else None) if _]
        return self.cmd("CrlAdd", *_cmd)

    def CrlDel(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.110_.22CrlDel.22:_Delete_a_Revoked_Certificate
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("CrlDel", *_cmd)

    def CrlGet(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.111_.22CrlGet.22:_Get_a_Revoked_Certificate
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("CrlGet", *_cmd)

    def AcList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.112_.22AcList.22:_Get_List_of_Rule_Items_of_Source_IP_Address_Limit_List
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("AcList", *_cmd)

    def AcAdd(self, allow_deny=None, _PRIORITY=None, _IP=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.113_.22AcAdd.22:_Add_Rule_to_Source_IP_Address_Limit_List_(IPv4)
        _cmd = [_ for _ in (None, allow_deny, "/PRIORITY:"+_PRIORITY if _PRIORITY else None, "/IP:"+_IP if _IP else None) if _]
        return self.cmd("AcAdd", *_cmd)

    def AcDel(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.114_.22AcDel.22:_Delete_Rule_from_Source_IP_Address_Limit_List
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("AcDel", *_cmd)

    def AcAdd6(self, allow_deny=None, _PRIORITY=None, _IP=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)#6.4.115_.22AcAdd6.22:_Add_Rule_to_Source_IP_Address_Limit_List_(IPv6)
        _cmd = [_ for _ in (None, allow_deny, "/PRIORITY:"+_PRIORITY if _PRIORITY else None, "/IP:"+_IP if _IP else None) if _]
        return self.cmd("AcAdd6", *_cmd)

    def cmd(self, *args, **kwargs):
        pass


class VPN_Client_Management:
    def About(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.1_.22About.22:_Display_the_version_information
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("About", *_cmd)

    def VersionGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.2_.22VersionGet.22:_Get_Version_Information_of_VPN_Client_Service
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("VersionGet", *_cmd)

    def PasswordSet(self, password=None, _REMOTEONLY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.3_.22PasswordSet.22:_Set_the_password_to_connect_to_the_VPN_Client_service.
        _cmd = [_ for _ in (None, password, "/REMOTEONLY:"+_REMOTEONLY if _REMOTEONLY else None) if _]
        return self.cmd("PasswordSet", *_cmd)

    def PasswordGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.4_.22PasswordGet.22:_Get_Password_Setting_to_Connect_to_VPN_Client_Service
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("PasswordGet", *_cmd)

    def CertList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.5_.22CertList.22:_Get_List_of_Trusted_CA_Certificates
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("CertList", *_cmd)

    def CertAdd(self, path=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.6_.22CertAdd.22:_Add_Trusted_CA_Certificate
        _cmd = [_ for _ in (None, path) if _]
        return self.cmd("CertAdd", *_cmd)

    def CertDelete(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.7_.22CertDelete.22:_Delete_Trusted_CA_Certificate
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("CertDelete", *_cmd)

    def CertGet(self, id=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.8_.22CertGet.22:_Get_Trusted_CA_Certificate
        _cmd = [_ for _ in (None, id, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("CertGet", *_cmd)

    def SecureList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.9_.22SecureList.22:_Get_List_of_Usable_Smart_Card_Types
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SecureList", *_cmd)

    def SecureSelect(self, id=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.10_.22SecureSelect.22:_Select_the_Smart_Card_Type_to_Use
        _cmd = [_ for _ in (None, id) if _]
        return self.cmd("SecureSelect", *_cmd)

    def SecureGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.11_.22SecureGet.22:_Get_ID_of_Smart_Card_Type_to_Use
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("SecureGet", *_cmd)

    def NicCreate(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.12_.22NicCreate.22:_Create_New_Virtual_Network_Adapter
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("NicCreate", *_cmd)

    def NicDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.13_.22NicDelete.22:_Delete_Virtual_Network_Adapter
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("NicDelete", *_cmd)

    def NicUpgrade(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.14_.22NicUpgrade.22:_Upgrade_Virtual_Network_Adapter_Device_Driver
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("NicUpgrade", *_cmd)

    def NicGetSetting(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.15_.22NicGetSetting.22:_Get_Virtual_Network_Adapter_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("NicGetSetting", *_cmd)

    def NicSetSetting(self, name=None, _MAC=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.16_.22NicSetSetting.22:_Change_Virtual_Network_Adapter_Setting
        _cmd = [_ for _ in (None, name, "/MAC:"+_MAC if _MAC else None) if _]
        return self.cmd("NicSetSetting", *_cmd)

    def NicEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.17_.22NicEnable.22:_Enable_Virtual_Network_Adapter
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("NicEnable", *_cmd)

    def NicDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.18_.22NicDisable.22:_Disable_Virtual_Network_Adapter
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("NicDisable", *_cmd)

    def NicList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.19_.22NicList.22:_Get_List_of_Virtual_Network_Adapters
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("NicList", *_cmd)

    def AccountList(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.20_.22AccountList.22:_Get_List_of_VPN_Connection_Settings
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("AccountList", *_cmd)

    def AccountCreate(self, name=None, _SERVER=None, _HUB=None, _USERNAME=None, _NICNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.21_.22AccountCreate.22:_Create_New_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/HUB:"+_HUB if _HUB else None, "/USERNAME:"+_USERNAME if _USERNAME else None, "/NICNAME:"+_NICNAME if _NICNAME else None) if _]
        return self.cmd("AccountCreate", *_cmd)

    def AccountSet(self, name=None, _SERVER=None, _HUB=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.22_.22AccountSet.22:_Set_the_VPN_Connection_Setting_Connection_Destination
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/HUB:"+_HUB if _HUB else None) if _]
        return self.cmd("AccountSet", *_cmd)

    def AccountGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.23_.22AccountGet.22:_Get_Setting_of_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountGet", *_cmd)

    def AccountDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.24_.22AccountDelete.22:_Delete_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountDelete", *_cmd)

    def AccountUsernameSet(self, name=None, _USERNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.25_.22AccountUsernameSet.22:_Set_User_Name_of_User_to_Use_Connection_of_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/USERNAME:"+_USERNAME if _USERNAME else None) if _]
        return self.cmd("AccountUsernameSet", *_cmd)

    def AccountAnonymousSet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.26_.22AccountAnonymousSet.22:_Set_User_Authentication_Type_of_VPN_Connection_Setting_to_Anonymous_Authentication
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountAnonymousSet", *_cmd)

    def AccountPasswordSet(self, name=None, _PASSWORD=None, _TYPE=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.27_.22AccountPasswordSet.22:_Set_User_Authentication_Type_of_VPN_Connection_Setting_to_Password_Authentication
        _cmd = [_ for _ in (None, name, "/PASSWORD:"+_PASSWORD if _PASSWORD else None, "/TYPE:"+_TYPE if _TYPE else None) if _]
        return self.cmd("AccountPasswordSet", *_cmd)

    def AccountCertSet(self, name=None, _LOADCERT=None, _LOADKEY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.28_.22AccountCertSet.22:_Set_User_Authentication_Type_of_VPN_Connection_Setting_to_Client_Certificate_Authentication
        _cmd = [_ for _ in (None, name, "/LOADCERT:"+_LOADCERT if _LOADCERT else None, "/LOADKEY:"+_LOADKEY if _LOADKEY else None) if _]
        return self.cmd("AccountCertSet", *_cmd)

    def AccountCertGet(self, name=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.29_.22AccountCertGet.22:_Get_Client_Certificate_to_Use_for_Cascade_Connection
        _cmd = [_ for _ in (None, name, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("AccountCertGet", *_cmd)

    def AccountEncryptDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.30_.22AccountEncryptDisable.22:_Disable_Encryption_when_Communicating_by_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountEncryptDisable", *_cmd)

    def AccountEncryptEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.31_.22AccountEncryptEnable.22:_Enable_Encryption_when_Communicating_by_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountEncryptEnable", *_cmd)

    def AccountCompressEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.32_.22AccountCompressEnable.22:_Enable_Data_Compression_when_Communicating_by_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountCompressEnable", *_cmd)

    def AccountCompressDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.33_.22AccountCompressDisable.22:_Disable_Data_Compression_when_Communicating_by_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountCompressDisable", *_cmd)

    def AccountProxyNone(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.34_.22AccountProxyNone.22:_Specify_Direct_TCP.2FIP_Connection_as_the_Connection_Method_of_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountProxyNone", *_cmd)

    def AccountProxyHttp(self, name=None, _SERVER=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.35_.22AccountProxyHttp.22:_Set_Connection_Method_of_VPN_Connection_Setting_to_be_via_an_HTTP_Proxy_Server
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("AccountProxyHttp", *_cmd)

    def AccountProxySocks(self, name=None, _SERVER=None, _PASSWORD=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.36_.22AccountProxySocks.22:_Set_Connection_Method_of_VPN_Connection_Setting_to_be_via_an_SOCKS_Proxy_Server
        _cmd = [_ for _ in (None, name, "/SERVER:"+_SERVER if _SERVER else None, "/PASSWORD:"+_PASSWORD if _PASSWORD else None) if _]
        return self.cmd("AccountProxySocks", *_cmd)

    def AccountServerCertEnable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.37_.22AccountServerCertEnable.22:_Enable_VPN_Connection_Setting_Server_Certificate_Verification_Option
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountServerCertEnable", *_cmd)

    def AccountServerCertDisable(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.38_.22AccountServerCertDisable.22:_Disable_VPN_Connection_Setting_Server_Certificate_Verification_Option
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountServerCertDisable", *_cmd)

    def AccountServerCertSet(self, name=None, _LOADCERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.39_.22AccountServerCertSet.22:_Set_Server_Individual_Certificate_for_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/LOADCERT:"+_LOADCERT if _LOADCERT else None) if _]
        return self.cmd("AccountServerCertSet", *_cmd)

    def AccountServerCertDelete(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.40_.22AccountServerCertDelete.22:_Delete_Server_Individual_Certificate_for_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountServerCertDelete", *_cmd)

    def AccountServerCertGet(self, name=None, _SAVECERT=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.41_.22AccountServerCertGet.22:_Get_Server_Individual_Certificate_for_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/SAVECERT:"+_SAVECERT if _SAVECERT else None) if _]
        return self.cmd("AccountServerCertGet", *_cmd)

    def AccountDetailSet(self, name=None, _MAXTCP=None, _INTERVAL=None, _TTL=None, _HALF=None, _BRIDGE=None, _MONITOR=None, _NOTRACK=None, _NOQOS=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.42_.22AccountDetailSet.22:_Set_Advanced_Settings_for_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/MAXTCP:"+_MAXTCP if _MAXTCP else None, "/INTERVAL:"+_INTERVAL if _INTERVAL else None, "/TTL:"+_TTL if _TTL else None, "/HALF:"+_HALF if _HALF else None, "/BRIDGE:"+_BRIDGE if _BRIDGE else None, "/MONITOR:"+_MONITOR if _MONITOR else None, "/NOTRACK:"+_NOTRACK if _NOTRACK else None, "/NOQOS:"+_NOQOS if _NOQOS else None) if _]
        return self.cmd("AccountDetailSet", *_cmd)

    def AccountRename(self, name=None, _NEW=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.43_.22AccountRename.22:_Change_VPN_Connection_Setting_Name
        _cmd = [_ for _ in (None, name, "/NEW:"+_NEW if _NEW else None) if _]
        return self.cmd("AccountRename", *_cmd)

    def AccountConnect(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.44_.22AccountConnect.22:_Start_Connection_to_VPN_Server_using_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountConnect", *_cmd)

    def AccountDisconnect(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.45_.22AccountDisconnect.22:_Disconnect_VPN_Connection_Setting_During_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountDisconnect", *_cmd)

    def AccountStatusGet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.46_.22AccountStatusGet.22:_Get_Current_VPN_Connection_Setting_Status
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountStatusGet", *_cmd)

    def AccountNicSet(self, name=None, _NICNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.47_.22AccountNicSet.22:_Set_Virtual_Network_Adapter_for_VPN_Connection_Setting_to_Use
        _cmd = [_ for _ in (None, name, "/NICNAME:"+_NICNAME if _NICNAME else None) if _]
        return self.cmd("AccountNicSet", *_cmd)

    def AccountStatusShow(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.48_.22AccountStatusShow.22:_Set_Connection_Status_and_Error_Screen_to_Display_when_Connecting_to_VPN_Server
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountStatusShow", *_cmd)

    def AccountStatusHide(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.49_.22AccountStatusHide.22:_Set_Connection_Status_and_Error_Screen_to_be_Hidden_when_Connecting_to_VPN_Server
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountStatusHide", *_cmd)

    def AccountSecureCertSet(self, name=None, _CERTNAME=None, _KEYNAME=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.50_.22AccountSecureCertSet.22:_Set_User_Authentication_Type_of_VPN_Connection_Setting_to_Smart_Card_Authentication
        _cmd = [_ for _ in (None, name, "/CERTNAME:"+_CERTNAME if _CERTNAME else None, "/KEYNAME:"+_KEYNAME if _KEYNAME else None) if _]
        return self.cmd("AccountSecureCertSet", *_cmd)

    def AccountRetrySet(self, name=None, _NUM=None, _INTERVAL=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.51_.22AccountRetrySet.22:_Set_Interval_between_Connection_Retries_for_Connection_Failures_or_Disconnections_of_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/NUM:"+_NUM if _NUM else None, "/INTERVAL:"+_INTERVAL if _INTERVAL else None) if _]
        return self.cmd("AccountRetrySet", *_cmd)

    def AccountStartupSet(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.52_.22AccountStartupSet.22:_Set_VPN_Connection_Setting_as_Startup_Connection
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountStartupSet", *_cmd)

    def AccountStartupRemove(self, name=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.53_.22AccountStartupRemove.22:_Remove_Startup_Connection_of_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name) if _]
        return self.cmd("AccountStartupRemove", *_cmd)

    def AccountExport(self, name=None, _SAVEPATH=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.54_.22AccountExport.22:_Export_VPN_Connection_Setting
        _cmd = [_ for _ in (None, name, "/SAVEPATH:"+_SAVEPATH if _SAVEPATH else None) if _]
        return self.cmd("AccountExport", *_cmd)

    def AccountImport(self, path=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.55_.22AccountImport.22:_Import_VPN_Connection_Setting
        _cmd = [_ for _ in (None, path) if _]
        return self.cmd("AccountImport", *_cmd)

    def RemoteEnable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.56_.22RemoteEnable.22:_Allow_Remote_Management_of_VPN_Client_Service
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("RemoteEnable", *_cmd)

    def RemoteDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.57_.22RemoteDisable.22:_Deny_Remote_Management_of_VPN_Client_Service
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("RemoteDisable", *_cmd)

    def KeepEnable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.58_.22KeepEnable.22:_Enable_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("KeepEnable", *_cmd)

    def KeepDisable(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.59_.22KeepDisable.22:_Disable_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("KeepDisable", *_cmd)

    def KeepSet(self, _HOST=None, _PROTOCOL=None, _INTERVAL=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.60_.22KeepSet.22:_Set_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, "/HOST:"+_HOST if _HOST else None, "/PROTOCOL:"+_PROTOCOL if _PROTOCOL else None, "/INTERVAL:"+_INTERVAL if _INTERVAL else None) if _]
        return self.cmd("KeepSet", *_cmd)

    def KeepGet(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.61_.22KeepGet.22:_Get_the_Keep_Alive_Internet_Connection_Function
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("KeepGet", *_cmd)

    def MakeCert(self, _CN=None, _O=None, _OU=None, _C=None, _ST=None, _L=None, _SERIAL=None, _EXPIRES=None, _SIGNCERT=None, _SIGNKEY=None, _SAVECERT=None, _SAVEKEY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.62_.22MakeCert.22:_Create_New_X.509_Certificate_and_Private_Key
        _cmd = [_ for _ in (None, "/CN:"+_CN if _CN else None, "/O:"+_O if _O else None, "/OU:"+_OU if _OU else None, "/C:"+_C if _C else None, "/ST:"+_ST if _ST else None, "/L:"+_L if _L else None, "/SERIAL:"+_SERIAL if _SERIAL else None, "/EXPIRES:"+_EXPIRES if _EXPIRES else None, "/SIGNCERT:"+_SIGNCERT if _SIGNCERT else None, "/SIGNKEY:"+_SIGNKEY if _SIGNKEY else None, "/SAVECERT:"+_SAVECERT if _SAVECERT else None, "/SAVEKEY:"+_SAVEKEY if _SAVEKEY else None) if _]
        return self.cmd("MakeCert", *_cmd)

    def TrafficClient(self, host_port=None, _NUMTCP=None, _TYPE=None, _SPAN=None, _DOUBLE=None, _RAW=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.63_.22TrafficClient.22:_Run_Network_Traffic_Speed_Test_Tool_in_Client_Mode
        _cmd = [_ for _ in (None, host_port, "/NUMTCP:"+_NUMTCP if _NUMTCP else None, "/TYPE:"+_TYPE if _TYPE else None, "/SPAN:"+_SPAN if _SPAN else None, "/DOUBLE:"+_DOUBLE if _DOUBLE else None, "/RAW:"+_RAW if _RAW else None) if _]
        return self.cmd("TrafficClient", *_cmd)

    def TrafficServer(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.64_.22TrafficServer.22:_Run_Network_Traffic_Speed_Test_Tool_in_Server_Mode
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("TrafficServer", *_cmd)

    def Check(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.5_VPN_Client_Management_Command_Reference#6.5.65_.22Check.22:_Check_whether_SoftEther_VPN_Operation_is_Possible
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Check", *_cmd)

    def cmd(self, *args, **kwargs):
        pass


class VPN_Tools:
    def About(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.6_VPN_Tools_Command_Reference#6.6.1_.22About.22:_Display_the_version_information
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("About", *_cmd)

    def MakeCert(self, _CN=None, _O=None, _OU=None, _C=None, _ST=None, _L=None, _SERIAL=None, _EXPIRES=None, _SIGNCERT=None, _SIGNKEY=None, _SAVECERT=None, _SAVEKEY=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.6_VPN_Tools_Command_Reference#6.6.2_.22MakeCert.22:_Create_New_X.509_Certificate_and_Private_Key
        _cmd = [_ for _ in (None, "/CN:"+_CN if _CN else None, "/O:"+_O if _O else None, "/OU:"+_OU if _OU else None, "/C:"+_C if _C else None, "/ST:"+_ST if _ST else None, "/L:"+_L if _L else None, "/SERIAL:"+_SERIAL if _SERIAL else None, "/EXPIRES:"+_EXPIRES if _EXPIRES else None, "/SIGNCERT:"+_SIGNCERT if _SIGNCERT else None, "/SIGNKEY:"+_SIGNKEY if _SIGNKEY else None, "/SAVECERT:"+_SAVECERT if _SAVECERT else None, "/SAVEKEY:"+_SAVEKEY if _SAVEKEY else None) if _]
        return self.cmd("MakeCert", *_cmd)

    def TrafficClient(self, host_port=None, _NUMTCP=None, _TYPE=None, _SPAN=None, _DOUBLE=None, _RAW=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.6_VPN_Tools_Command_Reference#6.6.3_.22TrafficClient.22:_Run_Network_Traffic_Speed_Test_Tool_in_Client_Mode
        _cmd = [_ for _ in (None, host_port, "/NUMTCP:"+_NUMTCP if _NUMTCP else None, "/TYPE:"+_TYPE if _TYPE else None, "/SPAN:"+_SPAN if _SPAN else None, "/DOUBLE:"+_DOUBLE if _DOUBLE else None, "/RAW:"+_RAW if _RAW else None) if _]
        return self.cmd("TrafficClient", *_cmd)

    def TrafficServer(self, port=None):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.6_VPN_Tools_Command_Reference#6.6.4_.22TrafficServer.22:_Run_Network_Traffic_Speed_Test_Tool_in_Server_Mode
        _cmd = [_ for _ in (None, port) if _]
        return self.cmd("TrafficServer", *_cmd)

    def Check(self):
        # https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/6.6_VPN_Tools_Command_Reference#6.6.5_.22Check.22:_Check_whether_SoftEther_VPN_Operation_is_Possible
        _cmd = [_ for _ in (None, ) if _]
        return self.cmd("Check", *_cmd)

    def cmd(self, *args, **kwargs):
        pass


