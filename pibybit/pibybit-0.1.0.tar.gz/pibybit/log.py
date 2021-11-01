#! /usr/bin/python3
import json
import os
import sys
import traceback
from functools import wraps
from inspect import currentframe, getframeinfo, getmodule, stack

from loguru import logger
from utils import *

LogPath = os.getcwd()

def _ntf_err_return_true(x):
    try:
        if x['level'].name == "ERROR":
            NtfWechat(x['message'])
    except:
        pass
    finally:
        return True


logger.remove()
handler_id = logger.add(sys.stderr, 
                        level="INFO",
                        filter=lambda x: _ntf_err_return_true(x)
                        )

__f = logger
__f.add(f"{LogPath}/md5m_{{time:YYYY-MM-DD}}.log",format="{message}",level="DEBUG",rotation="00:00",enqueue=True, filter=lambda x: x['function']=="Logf") 


ERROR = logger.error
Error = ERROR

INFO = logger.info
Info = INFO

DEBUG = logger.debug
Debug = DEBUG


def Logf(o):
    o['key'] = o['exchange'] + ":" + o['ac'] + ":" + o['symbol']
    o['idx'] = o['key'] + ":" + o['t']
    o = json.dumps(o)
    __f.debug(o)


if __name__ == "__main__":
    ERROR("asd")
