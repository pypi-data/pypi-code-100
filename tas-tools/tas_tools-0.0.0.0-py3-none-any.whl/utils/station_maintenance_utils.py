"""
Station maintenance-utility for querying station-states
and restarting TBS-systems.
"""
import json
import sys
import os
import re
import time
import queue
import getpass
import logging
import argparse
import platform
import paramiko
import requests
import subprocess
import threading
import traceback
import pandas as pd
import concurrent.futures
from datetime import datetime
from functools import wraps
from platformutil.ssh import Ssh
from collections import defaultdict, namedtuple


TAS_SHEET_FILEPATH = ""
OS_ENV = ""
if os.sep == "\\":
    TAS_SHEET_FILEPATH = os.path.join(r'\\qcdfs', 'bldr', 'BoulderDFS',
                                      'prj', 'tbs', 'infra', 'power_bi',
                                      'pub_source_copies', 'TaS_Stations.xlsm')
    OS_ENV = "W"
if os.sep == "/":
    TAS_SHEET_FILEPATH = os.path.join(os.sep, 'prj', 
                                      'tbs', 'infra', 'power_bi',
                                      'pub_source_copies', 'TaS_Stations.xlsm')
    OS_ENV = "L"

root_tmp = os.path.dirname(os.getcwd())
target_dir = os.path.join(
            'opt', 'data', 'tas', 'tas_maintenance_logger',
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


def _get_logger(level='warning'):
    """Get Logging"""
    level_mapper = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }
    if not level_mapper.get(level):
        level = 'warning'
    print(f"Setting logging level: {level}")
    # create logger
    logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(level_mapper.get(level))
    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s, %(threadName)s, %(levelname)s >> %(message)s')
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level_mapper.get(level))
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


logger = _get_logger()


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            out = func(*args, **kwargs)
        except Exception as e:
            print(f"Executing '{func.__name__}' failed!\n{e}")
            logger.error(f"Executing '{func.__name__}' failed!\n{e}")
        else:
            return out
    return wrapper


class ReturnResult:
    pass


class SshClient(Ssh):
    def __init__(self,
                 host, username=None, password=None, keyfile='', port=22,
                 preconnect=None, encoding='utf-8', logger=logger
                 ):
        super().__init__(host, username=username, password=password,
                         keyfile=keyfile, port=port, preconnect=preconnect,
                         encoding=encoding)
        self.host = host
        self.logger = logger

    @exception_handler
    def _check_last_cmd_returncode(self):
        cmd = ""
        if OS_ENV == "W":
            cmd = "echo %errorlevel%"
        if OS_ENV == "L":
            cmd = "echo $?"
        o = self.do(cmd)
        out = o.strip()
        if out == '0':
            self.logger.info(fr"Command successful")
        else:
            self.logger.warning("Command unsuccessful")
        status = str(out).strip() == '0'

        return status

    @exception_handler
    def check_ssh(self, cmd):
        stdout = self.do(cmd)
        print(stdout)
        self.logger.info(f"Issued {cmd}, \nOutput:\n{stdout}")

    @exception_handler
    def check_ping(self):
        cmd = f"ping {'-n' if OS_ENV == 'W' else '-c'} 1 8.8.8.8"
        stdout = self.do(cmd)
        self.logger.info(f"Issued {cmd}, \nOutput:\n{stdout}")

    @exception_handler
    def list_frus_present(self):
        cmd = "si list_frus_present"
        self.logger.info(f"Listing fru states for {self.host}")
        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED getting fru states")
        self.logger.info("Finished retrieving fru states")
        return out

    @exception_handler
    def check_state(self):
        cmd = "si state"
        self.logger.info(f"Listing config state for {self.host}")
        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED getting config state")
        self.logger.info("Finished retrieving config state")
        return out

    @exception_handler
    def check_connectivity(self):
        cmd = "si connectivity_check --all"
        self.logger.info(f"Listing connectivity_check for {self.host}")
        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED checking connectivity_check")
        self.logger.info("Finished retrieving connectivity_check")
        return out

    @exception_handler
    def restart_stationmngr(self):
        cmd = "super systemctl restart tbs-stationmngr"
        self.logger.info(f"Restarting tbs-http on {self.host}")
        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED restarting tbs-stationmngr")
        self.logger.info("Finished restarting tbs-stationmngr")
        return out

    @exception_handler
    def check_stationmngr(self):
        cmd = "super systemctl status tbs-stationmngr"
        self.logger.info(f"Checking tbs-stationmngr on {self.host}")

        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED checking tbs-stationmngr")
        self.logger.info("Finished checking tbs-stationmngr")
        return out

    @exception_handler
    def restart_http(self):
        """super systemctl restart tbs-http"""
        cmd = "super systemctl restart tbs-http"
        self.logger.info(f"Restarting tbs-http on {self.host}")

        out = self.do(cmd)
        self.logger.info(f"Output: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED to restart tbs-http")
        self.logger.info("Finished execution of restarting tbs-http")
        return out

    @exception_handler
    def check_http(self):
        """super systemctl status tbs-http"""
        cmd = "super systemctl status tbs-http"
        self.logger.info(f"Checking tbs-http on {self.host}")

        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED checking tbs-http")
        self.logger.info("Finished checking tbs-http")
        return out

    @exception_handler
    def restart_prodinfra(self):
        """super systemctl restart tbs-prodinfra"""
        cmd = "super systemctl restart tbs-prodinfra"
        self.logger.info(f"Checking prodinfra on {self.host}")
        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED restarting tbs-prodinfra")
        self.logger.info("Finished restarting tbs-prodinfra")
        return out

    @exception_handler
    def check_prodinfra(self):
        """super systemctl status tbs-prodinfra"""
        cmd = "super systemctl status tbs-prodinfra"
        self.logger.info(f"Checking prodinfra status on {self.host}")
        out = self.do(cmd)
        self.logger.info(f"Output:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                         f"{out}"
                         f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        if not self._check_last_cmd_returncode():
            self.logger.warning("Command FAILED checking tbs-prodinfra")
        self.logger.info("Finished checking tbs-prodinfra")
        return out

    @exception_handler
    def npc_chassis_ctrl_off(self):
        """si npc --all --control off --outlet_type CHASSIS"""

        cmd = "si npc --all --control off --outlet_type CHASSIS"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    @exception_handler
    def npc_chassis_ctrl_on(self):
        """si npc --all --control on --outlet_type CHASSIS"""

        cmd = "si npc --all --control on --outlet_type CHASSIS"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    @exception_handler
    def npc_gnb_ctrl_off(self):
        """si npc --all --control off --outlet_type SERVER_GNB"""

        cmd = "si npc --all --control off --outlet_type SERVER_GNB"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    @exception_handler
    def npc_gnb_ctrl_on(self):
        """si npc --all --control on --outlet_type SERVER_GNB"""

        cmd = "si npc --all --control on --outlet_type SERVER_GNB"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    @exception_handler
    def npc_5gc_ctrl_off(self):
        """si npc --all --control off --outlet_type SERVER_5GC"""

        cmd = "si npc --all --control off --outlet_type SERVER_5GC"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    @exception_handler
    def npc_5gc_ctrl_on(self):
        """si npc --all --control on --outlet_type SERVER_5GC"""

        cmd = "si npc --all --control on --outlet_type SERVER_5GC"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    def run_fiber_check(self):
        """/opt/tbs/nr/stationmngr/etc/fiber_check.sh --verbose

        check tail-end for "INFO:Fiber check passed!!"
        """
        cmd = "/opt/tbs/nr/stationmngr/etc/fiber_check.sh --verbose"
        self.logger.info(f"Issuing si cmd on {self.host} : {cmd}")
        self.do(cmd)

    def check_systemctl(self):
        """ /:>systemctl | grep tbs
                tbs-chassisctl.service
                    loaded active running TBS Chassis Control
                tbs-http.service
                    loaded active running TBSHTTP server
                tbs-installer.service
                    loaded active running TBSINSTALLER API service
                tbs-linuxstats.service
                    loaded active running Linuxstats server
                tbs-logging-tbslog2dm.service
                    loaded active running TBS Logging Service: tbslog2dm
                tbs-nr-dpdk-bind.service
                    loaded active exited tbs-nr-dpdk-bind.service
                tbs-nr-firewall.service
                    loaded failed failed Add tbs firewall rules
                tbs-nr-mlnx-vf-assign.service
                    loaded active exited tbs-nr-mlnx-vf-assign.service
                tbs-prodinfra.service
                    loaded active running TBS Product Infrastructure
                tbs-stationinfra.service
                    loaded active running TBS Station Infrastructure
                tbs-stationmngr.service
                    loaded active running TBS Station Manager
                tbs-utilization-framework.service
                    loaded active running Start tbs utilzation framework
                tbs-logging.target
                    loaded active active TBS Logging Service Target
        * parse line by line looking for "loaded failed"
        """
        pass

    def get_station_hardware_file(self):
        """/opt/tbs/etc/station_hardware.json"""
        pass


class TBSNRHTTPClient:
    def __init__(self, host, logger=logger):
        self.host = host
        self._logger = logger

    def _get(self, url):
        logger.info(f"Attempting request: {url}")
        try:
            r = requests.get(url, verify=False)
            if r.status_code != 200:
                logger.error(f"API {url} for {self.host} was unsuccessful")
                logger.error(f"Status Code: {r.status_code}")
                logger.error(f"Reasong: {r.reason}")
                return None
        except Exception as e:
            logger.error("!Request error:")
            logger.error(e)
        else:
            data = r.json().get('data')
            return data

    def _post(self, url, payload):

        try:
            r = requests.post(url, json=payload, verify=False)
            if r.status_code != 200:
                logger.error(f"Status Code: {r.status_code}")
                logger.error(f"Reasong: {r.reason}")
                raise Exception(r)
        except Exception as e:
            logger.error("!Request error:")
            logger.error(e)
        else:
            logger.info("Reboot command executed...")

    def get_station_status(self):
        """
        tbs-{host}-5g.qualcomm.com/api/private/station/status
        """
        url = f"http://tbs-{self.host}-5g.qualcomm.com" \
              f"/api/private/station/status"
        logger.info(f"Retrieving station status for {self.host}")
        station_status = self._get(url)
        if station_status:
            logger.info("Retrieved station status successfully...")
        return station_status

    def get_active_alarms(self):
        """Get list of active alarm from TBS 5G System."""
        url = f'http://tbs-{self.host}-5g.qualcomm.com' \
              f'/api/private/system/alarmInfo'
        try:
            alarm_info = self._get(url)
            active_alarms = alarm_info.get('activeAlarms')
        except Exception as e:
            err = f'Unable to get active Alarms info. {e}'
            logger.error(err)
        else:
            return active_alarms

    def reboot_servers(self):
        """
        tbs-{host}-5g.qualcomm.com/api/action/private/Admin/RebootReq
        """
        url = f"http://tbs-{self.host}-5g.qualcomm.com/" \
              f"api/action/private/Admin/reboot"
        payload = {
            "includeChassis": "NR_TRUE",
            "includeAllServers": "NR_TRUE"
        }
        self._post(url, payload)


class TasMaintenanceUtil:
    def __init__(self, host, logger=None, username=None, password=None,
                 key_file=None, ssh_client=None, http_client=None):
        self.host = host
        self.logger = logger
        self.username = username
        self.password = password
        self.key_file = key_file
        if not os.path.exists(self.key_file):
            TasMaintenanceUtil.generate_keys()
            TasMaintenanceUtil.copy_ssh_keys(username=self.username,
                                             password=self.password,
                                             host_id=self.host)
        self.ssh_client = ssh_client if ssh_client else \
            SshClient(f"tbs-{host}-5g", keyfile=key_file, logger=self.logger)
        self.http_client = http_client if http_client else \
            TBSNRHTTPClient(host, logger=self.logger)
        self.station_status = None

    @staticmethod
    def get_hosts(pool_type='TAS', filepath=TAS_SHEET_FILEPATH):
        hosts = []
        logger.info(f"Collecting hosts from {filepath}")
        xl = pd.read_excel(filepath, engine='openpyxl')
        for system in xl.to_dict('records'):
            fgs = system['5G System']
            station_pool = system['Purpose / Pool']
            if type(fgs) is str:
                m = re.match(r'tbs-([\d]+)-5g', fgs)
                if m and type(station_pool) is str and pool_type in station_pool:
                    hosts.append(m.group(1))
        logger.info(f"Hosts retrieved: {hosts}")
        return hosts

    @classmethod
    def copy_ssh_keys(cls, username=None, password=None, host_id=None):
        target_uri = f'{username}@tbs-{host_id}-5g'
        cmd = ['ssh-copy-id', target_uri]
        logger.info(f'Copying ssh keys: {cmd}')
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            res, err = p.communicate(input=password+'\n')
            p.wait()
        except Exception as e:
            print(e)
            print(f"Copying ssh keys failed")
        else:
            cert_content = res.decode('utf-8')
            print(cert_content)

    @classmethod
    def check_default_ssh_key_file(cls):
        home = rf'{os.path.expanduser("~")}'
        key_file = os.path.join(home, '.ssh', 'id_rsa')
        if os.path.exists(key_file):
            return True
        return False

    @classmethod
    def generate_keys(cls):
        cmd = ['ssh-keygen', '-t', 'rsa']
        logger.info(f'Generating ssh key: {cmd}')
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                 stdin=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            p.communicate(input=b"\n")
        except Exception as e:
            print(e)
        else:
            if TasMaintenanceUtil.check_default_ssh_key_file():
                print(f"SSH key created.")
            else:
                print("Ssh key not found")

    def get_ss(self):
        if not self.station_status:
            self.station_status = self.http_client.get_station_status()
            self.logger.info(f"Received station status for {self.host}")

    def get_active_alarms(self):
        alarms = self.http_client.get_active_alarms()
        self.logger.info(f"Active Alarms:\n{alarms}")

    def get_fru_state_from_status(self, non_m4_only=False):
        m4_re = re.compile(r"[M|m]4")
        fru_status = defaultdict(list)
        if not self.station_status:
            self.logger.info("Station status NOT FOUND")
            self.logger.info(self.station_status)
            return None
        self.logger.info("Iterating over status to parse fruState")

        for c in self.station_status["stationInfra"]["chassis"]:
            try:
                for f in c["fruList"]["entries"]:
                    if non_m4_only and not m4_re.search(f["fruState"]):
                        fru_status[f["fruState"]].append(
                            {"deviceName": f["deviceName"], "fruId": f["fruId"]})
                    else:
                        fru_status[f["fruState"]].append(
                            {"deviceName": f["deviceName"], "fruId": f["fruId"]})
            except Exception as e:
                self.logger.warning(e)
                self.logger.warning(f"Station status, chassis: {c}")

        return fru_status

    def get_fru_state_from_si(self):
        out = self.ssh_client.list_frus_present()
        return out

    def check_state(self):
        self.ssh_client.check_state()

    def check_connectivity(self):
        self.ssh_client.check_connectivity()

    def check_ping(self):
        """Ping a station"""
        cmd = ["ping", "-n" if OS_ENV == "W" else "-c", "1",
               f"tbs-{self.host}-5g"]
        out = subprocess.check_output(cmd)
        self.logger.info(out)

    def run_health_check(self):
        # todo: implement and test
        # add aesthetics for printing on screen
        # handle true/false-ness for pass-fail criteria
        self.check_ping()  # ping target
        self.http_client.get_station_status()  # get status
        self.ssh_client.check_ping()  # ping from target
        pass


class MaintenanceMenuController:
    """Dynamic command-line menu with MaintenanceMenuController.run()"""
    def __init__(self, args):
        self.username = None
        self.password = None
        self.host_ids = None
        self.args = args
        self.host_container = {}
        self.stations_status = {}
        self.key_file = self._get_default_key_file()
        self.station_id_re = re.compile(r"^\d{4}$")

    def _get_credentials(self):
        print("Credentials required to proceed...")
        self.username = getpass.getuser()
        self.password = getpass.getpass()

    def _get_default_key_file(self):
        home = rf'{os.path.expanduser("~")}'
        key_file = os.path.join(home, '.ssh', 'id_rsa')
        return key_file

    def _retrieve_host_ids(self):
        pool_mapper = {
            'tas_pool': 'TAS',
            'msim_pool': 'MSIM',
            'nextgen_pool': 'NEXTGEN'
        }
        while True:
            print("", flush=True)
            usr_input = input("Please enter the 4-digit station id(s) or "
                              "pool-designators 'tas_pool', 'msim_pool', "
                              "or 'nextgen_pool'"
                              " to retrieve associated tas stations: ")

            # if usr_input == 'tas_pool':
            if pool_mapper.get(usr_input):
                station_ids = TasMaintenanceUtil.get_hosts(
                    pool_type=pool_mapper.get(usr_input))
            else:
                station_ids = usr_input.split()
            bad_match = [i for i in station_ids if not self.station_id_re.match(i)]
            if not bad_match:
                break
            print(f"Station id(s) {bad_match} did not seem to fit criteria. "
                  f"Try again")
        self.host_ids = station_ids

    def init_tas_maintenance_util(self):
        auth_hosts = []
        unauth_hosts = []
        thrd_results = []
        if self.args.log_level:
            log = _get_logger(self.args.log_level)
        else:
            log = _get_logger('warning')
        
        for s in self.host_ids:
            try:
                if not self.host_container.get(s):
                    self.host_container[s] = \
                        TasMaintenanceUtil(s, logger=log,
                                           username=self.username,
                                           password=self.password,
                                           key_file=self.key_file)
            except paramiko.AuthenticationException as e:
                print(f"Authentication Failed for {s}: {e}")
                if not self.username and not self.password:
                    self._get_credentials()
                unauth_hosts.append(s)
                print(f"Are your ssh keys copied to {s}?")
                continue
            except FileNotFoundError:
                print("Unable to find ssh key in ~/.ssh/")
                if not self.username and not self.password:
                    self._get_credentials()
                TasMaintenanceUtil.generate_keys()
                print("Please create the key...")
            except Exception as e:
                print(f"Failed to initialize {s} due to following "
                      f"exception:\n{e}")
                print(traceback.print_exc())
                continue
            else:
                auth_hosts.append(s)
            
        # todo: may not need this anymore??
        if unauth_hosts:
            print(f"The follow hosts need ssh keys or authentication: "
                  f"{unauth_hosts}")
            if not self.username and not self.password:
                self._get_credentials()
            for s in unauth_hosts:
                print(s)
                TasMaintenanceUtil.copy_ssh_keys(
                    username=self.username,
                    password=self.password,
                    host_id=s)
                auth_hosts.append(s)
        with concurrent.futures.ThreadPoolExecutor() as thrd_exe:
            for s in self.host_ids:
                thrd_results.append(thrd_exe.submit(self.host_container[s].get_ss))
            for r in concurrent.futures.as_completed(thrd_results):
                r.result()
        if auth_hosts:
            self.host_ids = auth_hosts
            print(f"Verified authorization for host id(s): {self.host_ids}")
        print("Initialization of hosts complete.")

    def do_0(self):
        """Exit Program"""
        print("Exiting")

    def do_1(self):
        """Copy SSH key to Target"""
        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.username and not self.password:
            self._get_credentials()
        for s in self.host_ids:
            print(s)
            stdout = TasMaintenanceUtil.copy_ssh_keys(
                username=self.username,
                password=self.password,
                host_id=s)
            print(f"Output {stdout}")

        print(f"Process Complete.")

    def do_2(self):
        """Create SSH Keys"""
        print("Generating ssh key....")
        stdout = TasMaintenanceUtil.generate_keys()
        print(f"Output {stdout}")

        print(f"Process Complete.")

    def do_3(self):
        """Enter and Initialize host(s)"""
        re_enter_host = 'yes'
        re_no = re.compile(r"[nN][oO]?")
        re_yes = re.compile(r"[yY][eE]?[sS]?")
        if self.host_ids:
            while True:
                print("Would you like to use a different host id other than:")
                print(self.host_ids)
                re_enter_host = input("? [yes|no]: ")
                if re_no.search(re_enter_host) or re_yes.search(re_enter_host):
                    break
                print("Please try enter your answer again")
        if not self.host_ids or re_yes.match(re_enter_host):
            self._retrieve_host_ids()
        self.init_tas_maintenance_util()

    def do_4(self):
        """Get fru state from station status"""
        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()

        for s in self.host_ids:
            try:
                fru_state = self.host_container[s].get_fru_state_from_status()
            except KeyError:
                print(f"Key error for {s}")
            else:
                print(f"List of fru-state-types on {s}: "
                      f"\n\t{list(fru_state.keys()) if fru_state else None}")

        print("Finished retrieving fru states!!")

    def do_5(self):
        """Get fru from list_frus_present"""
        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()
        try:
            for s in self.host_ids:
                print(s)
                fru_state = self.host_container[s].get_fru_state_from_si()
                print(fru_state)
        except Exception as e:
            print(e)

        print("Finished retrieving fru states!!")

    def do_6(self):
        """Validate ssh"""
        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()

        cmd = input("Enter a linux command to test via ssh: ")
        for s in self.host_ids:
            print(s)
            self.host_container[s].ssh_client.check_ssh(cmd)

        print(f"Finished validating ssh capability")

    def do_7(self):
        """Check tbs service"""
        ssh_check_methods = [m.split('check_')[-1] for m in sorted(dir(SshClient), key=len)
                             if m.startswith('check_') and 'ping' not in m
                             and 'systemctl' not in m
                             and 'ssh' not in m]
        service_method = None
        service_method_name = None

        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()

        print(f"Supported services such as {ssh_check_methods}")
        while True:
            user_input = input('Please enter the service to be checked or enter "cancel" to abort: ')

            if user_input == "cancel":
                break
            else:
                service_method_name = f"check_{user_input}"
            try:
                service_method = getattr(self.host_container[self.host_ids[0]].ssh_client, service_method_name)
            except AttributeError:
                print(f"Method {service_method_name} not found")
                print(f"Try one of the following: {ssh_check_methods}")
            else:
                break

        if service_method is None:
            return

        for s in self.host_ids:
            print(s)
            cmd_out = service_method()
            print(cmd_out)

        print(f"Finished checking {service_method_name}")

    def do_8(self):
        """Reboot servers"""
        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()

        for s in self.host_ids:
            print(s)
            self.host_container[s].http_client.reboot_servers()

        print(f"Process Complete.")

    def do_9(self):
        """Restart tbs service"""
        ssh_restart_methods = [m.split('restart_')[-1] for m in sorted(dir(SshClient), key=len)
                             if m.startswith('restart_')]
        service_method = None
        service_method_name = None

        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()

        print(f"Supported services such as {ssh_restart_methods}")
        while True:
            user_input = input('Please enter the service to be restarted or enter "cancel" to abort: ')

            if user_input == "cancel":
                break
            else:
                service_method_name = f"restart_{user_input}"
            try:
                service_method = getattr(self.host_container[self.host_ids[0]].ssh_client, service_method_name)
            except AttributeError:
                print(f"Method {service_method_name} not found")
                print(f"Try one of the following: {ssh_restart_methods}")
            else:
                break

        if service_method is None:
            return

        for s in self.host_ids:
            print(s)
            cmd_out = service_method()
            print(cmd_out)

        print(f"Initiated {service_method_name}")

    def do_10(self):
        """Get Active Alarms"""
        if not self.host_ids:
            self._retrieve_host_ids()
        if not self.host_container:
            self.init_tas_maintenance_util()

        for s in self.host_ids:
            print(s)
            self.host_container[s].get_active_alarms()

        print(f"Process Complete.")

    # def do_14(self):
    #     """Issue NPC Chassis power cycle"""
    #     wait_time = 5
    #     if not self.host_ids:
    #         self._retrieve_host_ids()
    #     if not self.host_container:
    #         self.init_tas_maintenance_util()
    #
    #     for s in self.host_ids:
    #         print(s)
    #         stdout = self.host_container[s].ssh_client.npc_chassis_ctrl_off()
    #         print(f"Waiting {wait_time} seconds before powering on...")
    #         time.sleep(wait_time)
    #         print(f"Output {stdout}")
    #         stdout = self.host_container[s].ssh_client.npc_chassis_ctrl_on()
    #         print(f"Output {stdout}")
    #
    #     print(f"Process Complete.")
    #
    # def do_15(self):
    #     """Issue NPC GNB power cycle"""
    #     wait_time = 5
    #     if not self.host_ids:
    #         self._retrieve_host_ids()
    #     if not self.host_container:
    #         self.init_tas_maintenance_util()
    #
    #     for s in self.host_ids:
    #         print(s)
    #         stdout = self.host_container[s].ssh_client.npc_gnb_ctrl_off()
    #         print(f"Waiting {wait_time} seconds before powering on...")
    #         time.sleep(wait_time)
    #         print(f"Output {stdout}")
    #         stdout = self.host_container[s].ssh_client.npc_gnb_ctrl_on()
    #         print(f"Output {stdout}")
    #
    #     print(f"Process Complete.")
    #
    # def do_16(self):
    #     """Issue NPC 5GC power cycle"""
    #     wait_time = 5
    #     if not self.host_ids:
    #         self._retrieve_host_ids()
    #     if not self.host_container:
    #         self.init_tas_maintenance_util()
    #
    #     for s in self.host_ids:
    #         print(s)
    #         stdout = self.host_container[s].ssh_client.npc_5gc_ctrl_off()
    #         print(f"Waiting {wait_time} seconds before powering on...")
    #         time.sleep(wait_time)
    #         print(f"Output {stdout}")
    #
    #         stdout = self.host_container[s].ssh_client.npc_5gc_ctrl_on()
    #         print(f"Output {stdout}")
    #
    #     print(f"Process Complete.")

    # def do_17(self):
    #     """Ping 5G Server"""
    #     wait_time = 5
    #     if not self.host_ids:
    #         self._retrieve_host_ids()
    #     if not self.host_container:
    #         self.init_tas_maintenance_util()
    #
    #     for s in self.host_ids:
    #         print(s)
    #         stdout = self.host_container[s].check_ping()
    #         print(f"Output {stdout}")
    #
    #     print(f"Process Complete.")

    # def do_18(self):
    #     """Run Health Check"""
    #     wait_time = 5
    #     if not self.host_ids:
    #         self._retrieve_host_ids()
    #     if not self.host_container:
    #         self.init_tas_maintenance_util()
    #
    #     for s in self.host_ids:
    #         print(s)
    #         stdout = self.host_container[s].run_health_check()
    #         print(f"Output {stdout}")
    #
    #     print(f"Process Complete.")

    def execute(self, input):
        controller_name = f"do_{input}"
        try:
            controller = getattr(self, controller_name)
        except AttributeError:
            print(f"Method {controller_name} not found")
        else:
            controller()

    def run(self):
        user_input = None
        while user_input != 0:
            self.generate_menu()
            try:
                user_input = int(input())
            except Exception as e:
                print(f"Input raised an exception: {e}")
                continue
            self.execute(user_input)
        print("Execution finished.")

    @staticmethod
    def generate_menu():
        print("================================")
        do_methods = [m for m in
                      sorted(dir(MaintenanceMenuController), key=len)
                      if m.startswith('do_')]

        menu_string = "\n".join(
            [f"{method.split('_')[-1]}.    "
             f"{getattr(MaintenanceMenuController, method).__doc__}"
             for method in do_methods])
        print(menu_string)
        print("================================")
        print("Enter a selection:", end="", flush=True)


def get_parser():
    """Get parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--hosts', type=str,
                        nargs='+', default=[],
                        help='List of host ids, Eg: 1450 1451')
    parser.add_argument('--log-level', type=str, default='warning',
                        choices=['debug', 'info', 'warning', 'error'])

    return parser


def get_parser_args():
    """
    Create the command line parser for our user interface CLI

    :return: A parser arguments.
    """
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    return args


def main_user_driven():
    args = get_parser_args()
    logger.info(target_dir)
    MaintenanceMenuController(args).run()


if __name__ == "__main__":
    main_user_driven()
