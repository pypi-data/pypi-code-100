#! /usr/bin/python3

import json
import traceback
from datetime import datetime, timedelta

import pytz
import requests

timezone_china = pytz.timezone('Asia/Shanghai')

def GetFmtTm():
    return datetime.now().astimezone(timezone_china).isoformat()

def GetFmtTmFromBitMEX(a):
    if a!= None:
        a = datetime.strptime(a, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours = 8)
        return a.astimezone(timezone_china).isoformat()

def GetFmtTmFromBinance(a):
    if a!= None:
        a = datetime.fromtimestamp(a / 1000)
        return a.astimezone(timezone_china).isoformat()

def GetFmtTmFromBybit(a):
    if a!= None:
        a = datetime.fromtimestamp(a / 1000)
        return a.astimezone(timezone_china).isoformat()


def NtfWechat(text, url):
    try:
        data = {
            "msgtype": "text",
            "text": {
                    "content": text,
                }
        }
        res = requests.post(url=url,data=json.dumps(data))
        return res.text
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    print(GetFmtTmFromBinance(1634015099999))
