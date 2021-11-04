import undetected_chromedriver.patcher
from undetected_chromedriver.v2 import ChromeOptions
from selenium.webdriver.common.keys import Keys
import vpncmd
import browsermobproxy as bmp
from subprocess import run, PIPE, DEVNULL
from .helper import Chrome
import os


class SNEAKY:
    def __init__(
            self,
            *args,
            user_agent: str = None,
            open_developer_tools: bool = False,
            browsermobproxy_enable: bool = True,
            browsermobproxy_server_init: dict = None,
            browsermobproxy_create_proxy_kwargs: dict = None,
            browsermobproxy_new_har_kwargs: dict = None,
            vpncmd_enable: bool = True,
            vpncmd_init: dict = None,
            vpncmd_setup_cmd_args: list = None,
            vpncmd_connect_known_vpn_kwargs: dict = None,
            debug: bool = False,
            **kwargs
    ):
        args = list(args)
        self.debug = debug
        self.open_developer_tools = open_developer_tools
        self.browsermobproxy_enable = browsermobproxy_enable
        self.vpncmd_enable = vpncmd_enable
        if self.browsermobproxy_enable:
            if not os.path.isfile(browsermobproxy_server_init["path"]):
                raise FileNotFoundError
            self.bmpserver = bmp.Server(**(browsermobproxy_server_init or {}))
            self.bmpserver.start()
            self.bmpproxy = self.bmpserver.create_proxy(**(browsermobproxy_create_proxy_kwargs or {}))
            if self.debug:
                print("started browsermob proxy")
        if self.vpncmd_enable:
            self.vpncmd = vpncmd.VPNCMD(**(vpncmd_init or {}))
            self.vpncmd.setup_cmd(*(vpncmd_setup_cmd_args or []))
            self.vpncmd.connect_known_vpn(**(vpncmd_connect_known_vpn_kwargs or {}))
            while not self.vpncmd.is_connected_to_vpn():
                Chrome.wait(0.5)
            if self.debug:
                print("started vpncmd")
        self.chrome_options = self.tweak_chrome_options(args, kwargs)
        self.chrome_capabilities = self.tweak_chrome_capabilities(args, kwargs)
        if self.debug:
            print("chrome_options", self.chrome_options)
            print("chrome_capabilities", self.chrome_capabilities)
            print("Chrome(args, kwargs)", args, kwargs)
        self.driver = Chrome(*args, **kwargs)
        self.driver.wait(1)
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": user_agent or "Mozilla/5.0 (Windows NT 8.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
            },
        )

    def tweak_chrome_capabilities(self, args, kwargs):
        chrome_capabilities = None
        chrome_capabilities_in_args = any(
            isinstance(_, dict) and "browserName" in _ and _["browserName"] == "chrome" for _ in args)
        chrome_capabilities_i = -1
        if "desired_capabilities" in kwargs:
            chrome_capabilities = kwargs["desired_capabilities"]
        elif chrome_capabilities_in_args:
            for i, _ in enumerate(args):
                if isinstance(_, dict) and "browserName" in _ and _["browserName"] == "chrome":
                    chrome_capabilities = _
                    chrome_capabilities_i = i
                    break
        if not chrome_capabilities:
            chrome_capabilities = self.chrome_options.to_capabilities()
        else:
            chrome_capabilities.update(self.chrome_options.to_capabilities())
        chrome_capabilities["goog:loggingPrefs"] = {
            "browser": "ALL"
        }
        if chrome_capabilities_i != -1:
            args[chrome_capabilities_i] = chrome_capabilities
        else:
            kwargs["desired_capabilities"] = chrome_capabilities
        return chrome_capabilities

    def tweak_chrome_options(self, args, kwargs):
        chrome_options = None
        chrome_options_in_args = any(isinstance(_, ChromeOptions) for _ in args)
        chrome_options_i = -1
        if "options" in kwargs:
            chrome_options = kwargs["options"]
        elif chrome_options_in_args:
            for i, _ in enumerate(args):
                if isinstance(_, ChromeOptions):
                    chrome_options = _
                    chrome_options_i = i
                    break
        if not chrome_options:
            chrome_options = ChromeOptions()
        if self.open_developer_tools:
            chrome_options.add_argument("--auto-open-devtools-for-tabs")
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--ignore-certificate-errors")
        if self.browsermobproxy_enable:
            chrome_options.add_argument("--proxy-server={}".format(self.bmpproxy.proxy))
        if chrome_options_i != -1:
            args[chrome_options_i] = chrome_options
        else:
            kwargs["options"] = chrome_options
        return chrome_options

    def __del__(self):
        self.quit()

    def quit(self):
        self.driver.quit()
        if self.browsermobproxy_enable:
            if hasattr(self.bmpserver, "stop"):
                self.bmpserver.stop()
        if self.vpncmd_enable:
            self.vpncmd.disconnect_vpn()
        if undetected_chromedriver.patcher.IS_POSIX:
            kill_cmd = '''kill $(ps aux | grep 'browsermob-proxy' | awk '{print $2}')'''
        else:
            kill_cmd = '''wmic process where "CommandLine Like '%browsermob-proxy%'" delete'''
        run(kill_cmd, shell=True, stdin=DEVNULL, stdout=PIPE, stderr=PIPE)







