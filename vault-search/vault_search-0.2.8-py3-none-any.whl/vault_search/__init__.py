#!/usr/bin/env python3
import requests
from os import close, environ
import argparse
import colorlog
import logging
import sys
import urllib.parse
import re
import threading
import time
q = 0
"""
ToDo:
* search only in values flag
* search only in keys flag
"""
SUFFIX = "data/"
MIDDLE_SUFFIX = "/ui/vault/secrets/"

def queue(OPERATOR=""):
    global q
    if OPERATOR == "inc":
        q = q + 1
    elif OPERATOR == "dec":
        q = q - 1
    else:
        return q

def logger():
    LOGGER = logging.getLogger('vs')
    LOGGER.setLevel(logging.DEBUG) 
    CH = logging.StreamHandler()
    CH.setLevel(logging.DEBUG)
    FORMAT = '%(message)s'
    CFORMAT = '%(log_color)s' + FORMAT
    F = colorlog.ColoredFormatter(
        CFORMAT, log_colors={
            'DEBUG': 'reset',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'bold_red'
            })
    CH.setFormatter(F)
    if (LOGGER.hasHandlers()):
        LOGGER.handlers.clear()
    LOGGER.addHandler(CH)
    LOGGER.setLevel(20)
    return LOGGER

log = logger()

def check_env_var(var_name, default_val=None, sys_exit=False, verbose=True,
                  secure=False):
    env_var = environ.get(var_name)
    if env_var is None or env_var == "":
        if default_val != None:
            return default_val
        log.error(f'{var_name} environment variable is not defined')
        print_help()
        if sys_exit:
            sys.exit(1)
    else:
        if not secure:
            log.debug(f'{var_name} is set to {env_var}')
        else:
            log.debug(f'{var_name} is set to ***secured***')
        return env_var


def print_help():
    print('This script is searching inside vault KV storage')
    print('There are couple required ENV variables for this script:\n')
    print('\t* VAULT_ADDR - Format is PROTOCOL+FQDN of vault instance;')
    print('\t* VAULT_NS - Vault namespace;')
    print('\t* VAULT_KV_PATH - name of KV where search will start from.\n')


def compute_url(VAULT_ADDR, PATH, VAULT_NS, VAULT_KV_PATH,
                VAULT_INIT_KV_WEB, KEY="", TYPE=""):
    if VAULT_OUTPUT == 'url':
        if TYPE == "section":
            return PATH.replace("/v1/" + VAULT_NS + VAULT_KV_PATH + "metadata",
                                VAULT_ADDR + MIDDLE_SUFFIX + VAULT_INIT_KV_WEB +
                                "list") + "?namespace=" + VAULT_NS[:-1]
        else:
            return KEY + ' => ' + PATH.replace("/v1/" + VAULT_NS + VAULT_KV_PATH + SUFFIX,
                                VAULT_ADDR + MIDDLE_SUFFIX + VAULT_INIT_KV_WEB +
                                "show/") + "?namespace=" + VAULT_NS[:-1]
    elif VAULT_OUTPUT == 'cli':
        if TYPE == "section":
            return f"vault kv list {PATH.replace('/v1/' + VAULT_NS, '').replace(VAULT_KV_PATH + 'metadata/',VAULT_KV_PATH)}"
        else:
            return f"vault kv get -field={KEY} {PATH.replace('/v1/' + VAULT_NS, '').replace(VAULT_KV_PATH + 'data/',VAULT_KV_PATH)}"
    else:
        if TYPE == "section":
            return PATH.replace('/v1/' + VAULT_NS, '').replace(VAULT_KV_PATH + 'metadata/',VAULT_KV_PATH)
        else:
            return KEY + ' => ' + PATH.replace('/v1/' + VAULT_NS, '').replace(VAULT_KV_PATH + 'data/',VAULT_KV_PATH)
def case_val(text):
    if CASE:
        return text.lower()
    else:
        return text

def get_creds(PATH, VAULT_TOKEN, VAULT_ADDR, TEXT, VAULT_NS, VAULT_KV_PATH,
              VAULT_INIT_KV_WEB, VAULT_EXCLUDE):
    if PATH == '/v1/' + VAULT_NS + VAULT_KV_PATH + 'metadata/' + SUFFIX or VAULT_EXCLUDE in PATH:
        return
    elif PATH[-1] == '/':
        METHOD = 'List'
        if '/data/' in PATH:
            PATH = PATH.replace('/data/', '/metadata/')
    else:
        METHOD = "Get"
        if "/metadata/" in PATH:
            PATH = PATH.replace("/metadata/", "/data/")
    r = requests.request(METHOD,
                    VAULT_ADDR + PATH,
                    headers={"X-Vault-Token": VAULT_TOKEN})
    if r.status_code != 404:
        r.raise_for_status()
    if 'keys' in r.json()['data']:
        log.debug(f'Discovering {VAULT_ADDR + PATH}')
        if re.search(TEXT, case_val(PATH)):
            log.info(compute_url(VAULT_ADDR, PATH, VAULT_NS, VAULT_KV_PATH,
                                 VAULT_INIT_KV_WEB, KEY=re.search(TEXT, case_val(PATH)) ,TYPE='section'))
        for KEY in r.json()['data']['keys']:
            while queue() > MAX_THREADS:
                time.sleep(1)
            queue("inc")
            threading.Thread(target=get_creds, args=(PATH + KEY, VAULT_TOKEN,
                    VAULT_ADDR, TEXT, VAULT_NS,
                    VAULT_KV_PATH,
                    VAULT_INIT_KV_WEB, 
                    VAULT_EXCLUDE)).start()
    else:
        log.debug(f'Discovering {PATH}')
        if re.search(TEXT, case_val(PATH)):
            log.info(compute_url(VAULT_ADDR, PATH, VAULT_NS, VAULT_KV_PATH,
                                    VAULT_KV_PATH, VAULT_INIT_KV_WEB))
        if r.json()['data']['metadata']['deletion_time'] != '':
            log.debug(f'This path was deleted '+compute_url(VAULT_ADDR, PATH, 
                                                           VAULT_NS, 
                                                           VAULT_KV_PATH,
                                                           VAULT_INIT_KV_WEB))
            queue("dec")
            return
        try:
            for DICT_KEY, DICT_VALUE in r.json()['data']['data'].items():
                if re.search(TEXT, case_val(str(DICT_KEY))):
                    log.info(compute_url(VAULT_ADDR, PATH, VAULT_NS,
                                                    VAULT_KV_PATH,
                                                    VAULT_INIT_KV_WEB, KEY=DICT_KEY))
                elif re.search(TEXT, case_val(str(DICT_VALUE))):
                    log.info(compute_url(VAULT_ADDR, PATH, VAULT_NS,
                                                    VAULT_KV_PATH,
                                                    VAULT_INIT_KV_WEB, KEY=DICT_KEY))
        except Exception as e:
            log.error(f'Got the exception {e}')
            log.error(f'Discovering {VAULT_ADDR + PATH}')
            print(f'Response {r.json()}')
            print(f'Status code: {r.status_code}')
    queue("dec")
    return


def vs():
    parser = argparse.ArgumentParser('Vault KV search')
    parser.add_argument('TEXT', metavar='TEXT', type=str, help='regexp for search')
    parser.add_argument('-i', dest='CASE', action='store_true', default=False, help='for case insensitive search')
    parser.add_argument('-e', dest='EXCLUDE', default='', help='exclude path (VAULT_EXCLUDE env)')
    parser.add_argument('-o', dest='OUTPUT', default='', help='url, cli, path (VAULT_OUTPUT env)')
    parser.add_argument('-t', dest='MAX_THREADS', type=int, default=100, help='max threads (default: 100)')
    args = parser.parse_args()

    VAULT_ADDR = check_env_var('VAULT_ADDR', secure=True, sys_exit=True)
    VAULT_NS = check_env_var('VAULT_NAMESPACE', secure=True) + '/'
    VAULT_KV_PATH = check_env_var('VAULT_KV_PATH', secure=True,
                                  sys_exit=True) + '/'
    VAULT_INIT_KV_WEB = urllib.parse.quote(VAULT_KV_PATH[:-1], safe='') + '/'
    global CASE
    CASE = vars(args)['CASE']
    if vars(args)['EXCLUDE']:
        VAULT_EXCLUDE = vars(args)['EXCLUDE']
    else:
        VAULT_EXCLUDE = check_env_var('VAULT_EXCLUDE', secure=False, sys_exit=False, default_val="Pepe likes excluding")
    if CASE:
        TEXT = vars(args)['TEXT'].lower()
    else:
        TEXT = vars(args)['TEXT']
    global VAULT_OUTPUT
    if vars(args)['OUTPUT']:
        VAULT_OUTPUT = vars(args)['OUTPUT']
    else:
        VAULT_OUTPUT = check_env_var('VAULT_OUTPUT', secure=False, sys_exit=False, default_val="cli")
    global MAX_THREADS
    MAX_THREADS = vars(args)['MAX_THREADS']
    APP_DEBUG = check_env_var('APP_DEBUG', default_val=False)
    if APP_DEBUG:
        log.setLevel(10)
    try:
        with open(f"{check_env_var('HOME',secure=True)}/.vault-token") as file:
            VAULT_TOKEN = file.read()
    except Exception as e:
        log.error(f"Can't get auth token from Vault - {e}")
        log.error(f"Please make sure that you are logged into vault")
        sys.exit(1)
    log.info(f"Start looking for {TEXT}")
    try:
        queue("inc")
        mainThread = threading.Thread(target=get_creds, args=('/v1/'+VAULT_NS + VAULT_KV_PATH + SUFFIX,
                VAULT_TOKEN, VAULT_ADDR, TEXT,
                VAULT_NS, VAULT_KV_PATH,
                VAULT_INIT_KV_WEB, VAULT_EXCLUDE))
        mainThread.start()
        mainThread.join()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            log.error(f"Got a 403 - Forbidden URL, indicating you are not logged in or lack appropriate permissions")
            log.error(f"Please make sure that you are logged into vault")
            sys.exit(1)
        raise
    except KeyboardInterrupt:
        log.error("OMG, you hit CTRL+C. Don't do it anymore!!!")
        sys.exit(1)