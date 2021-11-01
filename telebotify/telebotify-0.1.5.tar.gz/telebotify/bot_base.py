from typing import Dict, Callable

from telebotify.models.user import User
from telebotify.services import translation_service, HttpClient


class Bot:
    def __init__(self,
                 api_key: str,
                 webhook_url: str = '',
                 commands: Dict[str, Callable] = {},
                 cert_path: str = None):
        self.http = HttpClient(api_key)
        self.commands = self.set_commands(commands)
        self.set_webhook(webhook_url, cert_path)
        self.last_update_id = 0
        self.started = False

    def get_me(self) -> User:
        return self.http.get('getMe', User)

    def set_webhook(self, webhook_url, certificate):
        data = {"url": webhook_url}
        if certificate is not None:
            data["certificate"] = open(certificate, 'r')
        self.http.post('setWebhook', data)

    def send_message(self, chat_id, text, **kwargs):
        data = {"chat_id": chat_id, "text": text}
        if dict.get(kwargs, "reply_to_message_id") is not None:
            data["reply_to_message_id"] = kwargs["reply_to_message_id"]
        self.http.post('sendMessage', data)

    def set_commands(self, commands):
        def start(message):
            if self.started:
                self.send_message(message.chat.chat_id,
                                  translation_service.get("START_COMMAND_BOT_ALREADY_STARTED_MESSAGE"),
                                  reply_to_message_id=message.message_id)
            else:
                self.started = True
                self.send_message(message,
                                  translation_service.get("START_COMMAND_MESSAGE"),
                                  reply_to_message_id=message.message_id)

        if "start" not in commands:
            commands["start"] = lambda _, message: start(message)

        commands["help"] = lambda _, message: self.send_message(message,
                                                                "Help",
                                                                reply_to_message_id=message.message_id)
        return commands
