"""Request handlers for the tornado application."""
import json
import tornado.web
import tornado.websocket

from asyncio import Event
from importlib.resources import open_binary
from mimetypes import guess_type


messages = []
complete = False
messageEvent = Event()
messageReceivedEvent = Event()


def send_message(msg: dict):
    """Send a message.

    Notifies all websocket handlers that a new message is to be sent.

    :param msg: The message to send
    :type msg: dict
    """
    messages.append(msg)
    messageEvent.set()
    messageEvent.clear()


def completed():
    """Indicate that the processing is complete."""
    global complete

    complete = True
    messageEvent.set()


class StaticHandler(tornado.web.RequestHandler):
    """Handles sending the static frontend files."""

    def initialize(self, base_path=None):
        """Initialise the :class:`~ou_container_content.handlers.StaticHandler`.

        :param base_path: The base path to prepend to any matched paths
        :type base_path: str
        """
        self._base_path = base_path

    def get(self, path=None):
        """Handle GET requests.

        :param path: The matched path of the file to fetch
        :type path: str
        """
        if path:
            full_path = f'{self._base_path}{path}'
        else:
            full_path = self._base_path
        elements = full_path.split('/')
        with open_binary(f'ou_container_content.frontend{"." if len(elements) > 1 else ""}{".".join(elements[:-1])}',
                         elements[-1]) as in_f:
            mimetype = guess_type(elements[-1])
            if mimetype and mimetype[0]:
                self.set_header('Content-Type', mimetype[0])
            self.write(in_f.read())


class WebsocketHandler(tornado.websocket.WebSocketHandler):
    """Handles sending progress messages via the websocket."""

    async def open(self):
        """Handle opening the websocket connection and sending progress messages."""
        next_idx = 0
        for message in messages:
            await self.write_message(json.dumps(message))
            next_idx = next_idx + 1
        while not complete:
            await messageEvent.wait()
            while next_idx < len(messages):
                await self.write_message(json.dumps(messages[next_idx]))
                next_idx = next_idx + 1
        self.close()
        messageReceivedEvent.set()


async def console_handler():
    """Console handler printing messages to the console."""
    next_idx = 0
    for message in messages:
        if 'message' in message:
            print(message['message'])  # noqa: T001
        next_idx = next_idx + 1
    while not complete:
        await messageEvent.wait()
        while next_idx < len(messages):
            if 'message' in messages[next_idx]:
                print(messages[next_idx]['message'])  # noqa: T001
            next_idx = next_idx + 1
    messageReceivedEvent.set()
