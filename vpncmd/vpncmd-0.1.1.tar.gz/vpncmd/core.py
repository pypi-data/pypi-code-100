from subprocess import Popen, PIPE, DEVNULL
import requests
import csv
import re
import random
from io import StringIO
from .helper import VPN_Tools, VPN_Client_Management, VPN_Server_VPN_Bridge_Management_For_Entire_Server, VPN_Server_VPN_Bridge_Management_For_Virtual_Hub


class VPNCMD:
    s: requests.Session = requests.Session()
    vpns: list = None
    vpns_cols: list = None
    cmd_prefix: tuple = None

    def __init__(self, vpncmd_fp: str, debug: bool = False):
        self.vpncmd_fp = vpncmd_fp
        self.debug = debug
        self.VPN_Tools = VPN_Tools()
        self.VPN_Tools.cmd = self.cmd
        self.VPN_Client_Management = VPN_Client_Management()
        self.VPN_Client_Management.cmd = self.cmd
        self.VPN_Server_VPN_Bridge_Management_For_Entire_Server = VPN_Server_VPN_Bridge_Management_For_Entire_Server()
        self.VPN_Server_VPN_Bridge_Management_For_Entire_Server.cmd = self.cmd
        self.VPN_Server_VPN_Bridge_Management_For_Virtual_Hub = VPN_Server_VPN_Bridge_Management_For_Virtual_Hub()
        self.VPN_Server_VPN_Bridge_Management_For_Virtual_Hub.cmd = self.cmd

    def setup_cmd(self, *args):
        self.cmd_prefix = args

    def cmd(self, *args):
        if not self.cmd_prefix:
            raise ValueError("self.cmd_prefix is not set, use VPNCMD.setup_cmd first")
        cmd = [self.vpncmd_fp, *self.cmd_prefix, "/cmd", *args]
        shell = False
        if any(" " in _ for _ in args):
            shell = True
            cmd = " ".join('"{}"'.format(_) if " " in _ else _ for _ in cmd)
        if self.debug:
            print(cmd, shell)
            print()
        p = Popen(cmd, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, shell=shell)
        r = p.communicate()
        if self.debug:
            print(r)
            print()
        return r

    def get_vpns_csv(self):
        url = "http://www.vpngate.net/api/iphone/"
        try:
            return self.s.get(url, timeout=5).content.decode()
        except:
            try:
                _ = self.s.get("https://api.allorigins.win/get?url="+url, timeout=5).json()
                if _["status"]["http_code"] == 200:
                    return _["contents"]
                else:
                    raise
            except:
                try:
                    return self.s.get("https://jsonp.afeld.me/?callback=&url="+url).content.decode()
                except:
                    raise FileNotFoundError("cannot get vpns csv: {}".format(url))

    def fetch_vpns(self):
        _ = list(csv.reader(StringIO(self.get_vpns_csv())))
        self.vpns_cols = _[1]
        self.vpns = _[2:-1]
        _ = None

    def connect_random_vpn(self, _NICNAME: str = None):
        if not self.vpns:
            self.fetch_vpns()
        vpn = random.SystemRandom().choice(self.vpns)
        _SERVER = "{}:{}".format(vpn[1], 443)
        if not _NICNAME:
            nics = self.VPN_Client_Management.NicList()[0].decode().split("Virtual Network Adapter Name|")
            if len(nics) == 1:
                raise ValueError("VPN NIC does not exist, use VPNCMD.VPN_Client_Management.NicCreate first")
            _NICNAME = nics[1].splitlines()[0]
        name = "RANDOM VPN@{}".format(_SERVER)
        self.VPN_Client_Management.AccountCreate(name=name, _SERVER=_SERVER, _HUB="VPNGATE", _USERNAME="vpn", _NICNAME=_NICNAME)
        return self.VPN_Client_Management.AccountConnect(name=name)

    def delete_random_vpn(self):
        vpns = self.VPN_Client_Management.AccountList()[0].decode().split("VPN Connection Setting Name |")
        for vpn in vpns:
            vpn = vpn.splitlines()[0]
            if vpn.startswith("RANDOM VPN@") and vpn.endswith(":443"):
                return self.VPN_Client_Management.AccountDelete(name=vpn)

    def filter_vpns(self, column: str, value, sort: str = "Uptime", order: str = "desc"):
        if not self.vpns:
            self.fetch_vpns()
        if column not in self.vpns_cols:
            raise ValueError("'{}' not in '{}'".format(column, self.vpns_cols))
        if sort not in self.vpns_cols:
            raise ValueError("'{}' not in '{}'".format(sort, self.vpns_cols))
        column_index = self.vpns_cols.index(column)
        sort_index = self.vpns_cols.index(sort)
        def try_int(v):
            try:
                return int(v)
            except:
                return v
        def match(v1, v2):
            if isinstance(v2, re.Pattern):
                return v2.search(v1)
            else:
                return v1 == v2
        return sorted((_ for _ in self.vpns if match(_[column_index], value)), key=lambda x: try_int(x[sort_index]), reverse=True if order == "desc" else False)




