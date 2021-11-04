import requests
import wmi;
class GETEWays:
    BASE_URL = "";
    net_label = "";
    NIC  = None;
    def __init__(self,baseurl,net_label):
        self.BASE_URL = baseurl;
        self.net_label = net_label;
    """
    获取网关
    """
    def get_net(self):
        url = f"{self.BASE_URL}/api/net"
        headers = {
        'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)'
        }
        net_json = requests.request("GET", url, headers=headers, timeout=10).json();
        return net_json;

    """
    获取固定网关
    """
    def get_fixed(self):
        url = f"{self.BASE_URL}/api/fixedip/geteway"
        headers = {
        'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)'
        }
        fixed_net_json = requests.request("GET", url, headers=headers, timeout=10).json();
        return fixed_net_json;
    """
    设置网关
    """
    def set_geteway(self,_status='enableDHCP'):
        if self.NIC is None:
            wlan_int_id = None
            #设定对哪个可用网络设备进行设置，确保这个设备可用而不是被禁用。
            # net_label = u'本地连接'
            for nic in wmi.WMI().Win32_NetworkAdapter():
                if nic.NetConnectionID == self.net_label:
                    wlan_int_id = nic.Index
                    break
            if wlan_int_id != None:
                for nic in wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1):
                    if nic.Index == wlan_int_id:
                        if type(_status) == dict:
                            NIC = nic;
                            nic.SetGateways(DefaultIPGateway=[_status['gateway']])
                        elif 'enableDHCP' == _status:
                            nic.EnableDHCP()
            else:
                print('error,id is empty!')
        else:
           self.NIC.SetGateways(DefaultIPGateway=[_status['gateway']])

    """
    重启网关
    """
    def reset_geteway(self,current_getaway):
        url = f"http://{current_getaway}/goform/goform_set_cmd_process"
        #   url2 = "http://192.168.0.1/goform/goform_set_cmd_process"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": current_getaway,
            "Origin": f"http://{current_getaway}",
            "Referer": f"http://{current_getaway}/index.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        data2 = {
            "isTest": "false",
            "goformId": "LOGIN",
            "password": "YWRtaW4="
        }
        requests.post(url=url, data=data2, headers=headers,timeout=5)
        data = {
                "isTest": "false",
                "goformId": "REBOOT_DEVICE"
        }
        requests.post(url=url, data=data, headers=headers,timeout=5)




