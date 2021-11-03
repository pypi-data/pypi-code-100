"""
Copyright 2010-2021 Mikkel Munch Mortensen <3xm@detfalskested.dk>.

This file is part of SMS Gateway.

SMS Gateway is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SMS Gateway is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SMS Gateway.  If not, see <http://www.gnu.org/licenses/>.
"""

import base64
import getopt
import json
import re
from urllib import error, parse, request
from typing import Any, Tuple


class Gateway:
    """
    A Python wrapper around the SMS gateway from CPSMS <https://www.cpsms.dk/>.

    Please look at the README for further description.
    """

    options: dict[str, Any] = {}
    username: str
    password: str
    gateway_url: str = "https://api.cpsms.dk/v2/send"

    @property
    def default_options(self) -> dict[str, Any]:
        """Get some default options to use."""
        return {
            "to": "",
            "message": "",
            "from": "",
            "timestamp": "",  # For delaying messages. Format: Unix timestamp.
            "encoding": "UTF-8",
            "dlr_url": "",
            "flash": False,
            "reference": "",
            "format": "GSM",
        }

    def __init__(
        self,
        username: str,
        password: str,
        sender_name: str,
        options: dict[str, Any] = None,
        gateway_url: str = None,
    ) -> None:
        """Initialize SMS gateway."""
        self.username = username
        self.password = password

        self.options = self.default_options
        self.options["from"] = sender_name

        if options is not None:
            self.options.update(options)

        if gateway_url:
            self.gateway_url = gateway_url

    def send(self, to: str = None, message: str = None) -> Tuple[bool, str]:
        """
        Send a message to a recipient.

        Optionally, override the recpient and the message to be sent.
        """
        # Raise an error if the sender is not specified.
        if not self.options["from"]:
            raise ValueError("Sender name cannot be empty.")
        # Update message if specified.
        if message is not None:
            self.options["message"] = message

        # Raise error if message is empty.
        if not self.options["message"]:
            raise ValueError("Message cannot be empty.")

        # Raise error if message is too long.
        if len(self.options["message"]) > 459:
            raise ValueError(
                "Message not allowed to be more than 459 characters."
                "Current message is %i characters."
                % len(self.options["message"])
            )

        # Update recipient if specified.
        if to is not None:
            self.options["to"] = to

        # Raise error if recipients is empty.
        if not self.options["to"]:
            raise ValueError("No recipient is set.")

        # Raise error if recipient is not a number.
        pattern = re.compile("^[1-9]+$")
        if pattern.match(self.options["to"]) is None:
            raise ValueError("Recipient number must be numbers only (no characters, spaces or +)")

        # Prepare the data to send along.
        data = self.options
        data["flash"] = int(data["flash"])
        data = json.dumps(data).encode()

        # Prepare authentication.
        auth_header = "{}:{}".format(self.username, self.password)
        auth_header = base64.b64encode(auth_header.encode()).decode()

        http_request = request.Request(self.gateway_url, data=data)
        http_request.add_header(
            "Authorization", "Basic {}".format(auth_header)
        )
        response = request.urlopen(http_request)

        return json.loads(response.read().decode())
