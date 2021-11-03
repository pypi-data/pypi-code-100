import re
import time
import random
import requests
import vpncmd
from lxml import html
from netifaces import AF_INET, interfaces, ifaddresses


def create_session():
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"})
    return s


class zippyshare:
    s: requests.Session = None
    domain = "https://www.zippyshare.com"
    current_vpn_name = None

    def __init__(self, vpncmd_option = None, vpncmd_setup_cmd_option = None, debug = False):
        self.debug = debug
        if vpncmd_setup_cmd_option:
            self.vc = vpncmd.VPNCMD(**(vpncmd_option or {}))
            self.vc.setup_cmd(*(vpncmd_setup_cmd_option or []))
            self.s = create_session()

    def is_connected_to_vpn(self):
        for iface in interfaces():
            try:
                if not any(ifaddresses(iface)[AF_INET][0]['addr'].startswith(_) for _ in ["192.", "127.", "169.254."]):
                    return True
            except:
                pass
        return False

    def connect_vpn(self, _NICNAME):
        if not self.current_vpn_name:
            if self.debug:
                print("connecting to vpn")
            self.vc.connect_known_vpn(_NICNAME)
            while not self.is_connected_to_vpn():
                time.sleep(0.5)
        if self.debug:
            print("connected to vpn")

    def disconnect_vpn(self):
        if self.current_vpn_name:
            if self.debug:
                print("disconnecting vpn")
            self.vc.disconnect_known_vpn(name=self.current_vpn_name)
            self.current_vpn_name = None
        if self.debug:
            print("disconnected vpn")

    def login(self, credentials, use_vpn: bool = True, _NICNAME: str = "VPN2"):
        self.s = create_session()
        if use_vpn:
            self.connect_vpn(_NICNAME)
        if self.debug:
            print("logging in")
        self.s.get(self.domain)
        time.sleep(1)
        self.s.post(self.domain+"/services/login", data={
            "login": credentials[0],
            "pass": credentials[1],
            "remember": "on",
        })
        if self.debug:
            print("logged in")

    def logout(self):
        if self.debug:
            print("logging out")
        self.s.get(self.domain+"/services/logout")
        self.s.close()
        self.s = None
        if self.debug:
            print("logged out")
        self.disconnect_vpn()

    def remote_upload(self, remote_url, private: bool = True):
        if self.debug:
            print("remote uploading '{}'".format(remote_url))
        r = self.s.get(self.domain)
        r = html.fromstring(r.content.decode())
        action = r.xpath("//form[@name='upload_form2']/@action")[0]
        if action.startswith("//"):
            action = "https:"+action
        data = {"file1": remote_url}
        if private:
            data.update({"private": "checkbox"})
        r = self.s.post(action, data=data)
        if r.status_code != 200:
            raise Exception("cannot upload remote_url '{}' [{}] ({})".format(remote_url, r.status_code, r.content.decode()))
        r = html.fromstring(r.content.decode())
        text_field = r.xpath("//input[@class='text_field']/@value")[0]
        if self.debug:
            print("remote uploaded '{}'".format(remote_url))
        return text_field

    @staticmethod
    def get_link(file_url, _s=[]):
        if not _s:
            _s.append(create_session())
        s = _s[0]
        r = s.get(file_url)
        domain = "/".join(file_url.split("/")[:3])
        id = file_url.split("/")[-2]
        link = re.search(r".(/d/{}/)..*?\((.*?)\).*?(.)(/.*?)\3.*$".format(id), r.content.decode(), flags=re.MULTILINE)
        if not link:
            return Exception("file not found '{}' [{}]".format(id, r.status_code))
        return domain+link[1]+str(eval(link[2]))+link[4]

