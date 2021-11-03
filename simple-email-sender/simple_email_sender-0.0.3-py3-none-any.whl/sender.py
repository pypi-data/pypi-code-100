from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Optional, Union

import yaml


@dataclass(frozen=True)
class ServerSettings:
    """Class to store the credentials and settings for the SMTP-Server"""

    name: str
    server: str
    password: Optional[str] = None
    port: Optional[int] = None

    @classmethod
    def settings_from_yaml(cls, server_setting: str) -> ServerSettings:
        with open(server_setting, "r") as f:
            config: dict = yaml.load(f, Loader=yaml.FullLoader)

        if "password" not in config.keys():
            config["password"] = None
        if "port" not in config.keys():
            config["port"] = None

        return cls(
            name=config["name"],
            server=config["server"],
            password=config["password"],
            port=config["port"],
        )


class Sender:
    """
    Sender which will notify you with messages from a given Email account sending to
    a predefined Email address
    """

    def __init__(
        self,
        settings: Union[str, dict, ServerSettings],
        receiver: str,
        subject: Optional[str] = None,
    ):
        """

        :param settings: as ServerSettings
        :param receiver: as email address, who will get notified
        :param subject: Optional default subject for the email
        """
        if isinstance(settings, str):
            self._settings = ServerSettings.settings_from_yaml(settings)
        elif isinstance(settings, dict):
            self._settings = ServerSettings(**settings)
        else:
            self._settings = settings
        self._receiver = receiver
        self._subject = subject

    def send_with_ssl(
        self,
        message: str,
        receiver: Optional[str] = None,
        subject: Optional[str] = None,
    ):
        """
        Sends the message with SSL encrypted transmission of the password

        :param message: Message to send as a str
        :param subject: Optional subject to be used in email
        :param receiver: Optional receiver different to the default one
        """

        msg = MIMEText(message)
        msg["Subject"] = subject or self._subject
        msg["From"] = self._settings.name
        msg["To"] = receiver or self._receiver

        port = self._settings.port if self._settings.port else 0

        with smtplib.SMTP_SSL(self._settings.server, port) as smtp:
            smtp.login(self._settings.name, self._settings.password)
            smtp.send_message(msg)

    def send_without_login(
        self,
        message: str,
        receiver: Optional[str] = None,
        subject: Optional[str] = None,
    ):
        """
        Sends the message directly without authenticating at the server

        :param message:
        :param receiver:
        :param subject:
        """
        msg = MIMEText(message)
        msg["Subject"] = subject or self._subject
        msg["From"] = self._settings.name
        msg["To"] = receiver or self._receiver

        with smtplib.SMTP(self._settings.server) as smtp:
            smtp.send_message(msg)

    def send(
        self,
        message: str,
        receiver: Optional[str] = None,
        subject: Optional[str] = None,
    ):
        """
        Sends a message and chooses between encrypted transmission and anonymous
        sending whether a password is set or not

        :param message:
        :param receiver:
        :param subject:
        """

        if self._settings.password:
            self.send_with_ssl(message, receiver, subject)
        else:
            self.send_without_login(message, receiver, subject)

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
