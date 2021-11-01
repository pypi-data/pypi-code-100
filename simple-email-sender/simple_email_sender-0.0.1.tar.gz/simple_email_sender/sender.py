import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Optional, Union

import yaml


@dataclass(frozen=True)
class ServerSettings:
    """Class to store the credentials and settings for the SMTP-Server"""

    name: str
    password: str
    server: str
    port: int


class Sender:
    """
    Sender which will notify you with messages from a given Email account sending to
    a predefined Email address
    """

    @classmethod
    def settings_from_yaml(cls, server_setting: str) -> ServerSettings:
        with open(server_setting, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        return ServerSettings(
            name=config["name"],
            password=config["password"],
            server=config["server"],
            port=config["port"],
        )

    def __init__(
        self,
        settings: Union[str, ServerSettings],
        receiver: str,
        subject: Optional[str] = None,
    ):
        """

        :param settings: as ServerSettings
        :param receiver: as email address, who will get notified
        :param subject: Optional default subject for the email
        """
        if isinstance(settings, str):
            self._settings = self.settings_from_yaml(settings)
        else:
            self._settings = settings
        self._receiver = receiver
        self._subject = subject

    def send(
        self,
        message: str,
        receiver: Optional[str] = None,
        subject: Optional[str] = None,
    ):
        """
        Sends the message
        :param message: Message to send as a str
        :param subject: Optional subject to be used in email
        :param receiver: Optional receiver different to the default one
        """

        msg = MIMEText(message)
        msg["Subject"] = subject or self._subject
        msg["From"] = self._settings.name
        msg["To"] = receiver or self._receiver

        with smtplib.SMTP_SSL(self._settings.server, self._settings.port) as smtp:
            smtp.login(self._settings.name, self._settings.password)
            smtp.send_message(msg)

    def info(self, message):
        """
        Sends an info message, using default subject with "INFO: " at the beginning
        :param message:
        """
        self.send(message, subject=f"INFO: {self._subject}")

    def error(self, message):
        """
        Sends an error message, using default subject with "ERROR: " at the beginning
        :param message:
        """
        self.send(message, subject=f"ERROR: {self._subject}")
