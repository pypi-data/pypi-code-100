import json
import random
from sseclient import SSEClient

from .lib import Event
from sys import _getframe as getframe


class SSE:
    def __init__(self, client):
        self.sse_url = "https://capture.chat/api/eventsource?"
        self.client = client

    def handle_message(self, data, event):
        self.client.handle(data, event)
        return

    def launch(self):
        sse = SSEClient(f"{self.sse_url}x-token={self.client.token}&session-id={str(random.randint(1, 9999))}")
        for event in sse: self.handle_message(event.data, event.event)


class Recall:
    def __init__(self):
        self.handlers = {}
        self.methods = {
            "topic_user_leave": self.on_topic_user_leave,
            "topic_user_join": self.on_topic_user_join,
            "message_delete": self.on_message_delete,
            "message_edit": self.on_message_edit,
            "typing": self.on_typing_status,
            "message": self.on_message,
            "connect": self.on_ready,
            "ping": self.on_ping
        }

    def solve(self, data, event):
        data = json.loads(data)
        return self.methods.get(event, self.classic)(data)

    def roll(self, func, data):
        if func in self.handlers:
            for handler in self.handlers[func]: handler(data)

    def event(self, func):
        def regHandler(handler):
            if func in self.handlers: self.handlers[func].append(handler)
            else: self.handlers[func] = [handler]
            return handler
        return regHandler

    def on_topic_user_leave(self, data):self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_topic_user_join(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_message_delete(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_typing_status(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_message_edit(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_message(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_ready(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def on_ping(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
    def classic(self, data): self.roll(getframe(0).f_code.co_name, Event(data).Event)
