from .lib import CheckExceptions
from threading import Thread as Th

from random import randint
from time import sleep

import requests
import json


class Threads:
    def __init__(self):
        self.api = "https://capture.chat/api"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
            "session-id": str(randint(1, 9999)),
            "x-user-agent": "14 Web/1 ru"
        }
        self.time = 0

    def _send_typing_status_(self, headers, topicId: str, status: str = "text"):
        self.headers = headers
        response = requests.post(f"{self.api}/topic/{topicId}/typing?status={status}", headers=self.headers)
        if response.status_code != 200: return CheckExceptions(response.json())
        else: return response.status_code

    def _when_typing_(self, topicId, messageId, newText):
        data = json.dumps({"text": newText})
        response = requests.patch(f"{self.api}/topic/{topicId}/message/{messageId}", data=data, headers=self.headers)
        if response.status_code != 200: CheckExceptions(response.json())
        else: return response.status_code

    def send(self, fun, args, time):
        self.time = time
        for i in range(int(time / 4)):
            t = Th(target=fun, args=args)
            t.start()
            sleep(4)

    def send_edit(self, fun, args, args2):
        for i in range(int(self.time) + 1):
            t = Th(target=fun, args=(args, args2, str(i), ))
            t.start()
            sleep(0.750)
