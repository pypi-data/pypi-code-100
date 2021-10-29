import json

import requests


def ding_talk(ding_talk_url, title, text, develops):
    headers = {
        "Content-Type": "application/json"
    }
    mkdown = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        },
        "at": {
            "atMobiles": develops,
            "isAtAll": False
        }
    }
    json_data = json.dumps(mkdown)
    requests.post(url=ding_talk_url, data=json_data, headers=headers)
