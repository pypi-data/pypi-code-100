# 获取机器人的回复
import os
from urllib.parse import urljoin

import requests


def get_robot_reply(data: dict) -> dict:
    server = os.getenv("CCP2_SERVER_ADDR")

    assert server != "", "please set CCP2_SERVER_ADDR env"

    api = urljoin(server, "/api/v1/im/message")

    resp = requests.post(api, json=data)
    resp.close()

    return resp.json() if resp.ok else {}
