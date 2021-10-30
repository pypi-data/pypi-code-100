"""

"""


import concurrent.futures
from typing import Optional
from datetime import datetime
import aiohttp
import asyncio
import json
import importlib
import threading
import time
import sys
import traceback
import inspect

from . import utils
from .container import Container
from .decorators import Command, Component, Event
from .models.user import User
from .models.context import Context, ButtonContext, SelectMenuContext

class MaintainSocketAlive(threading.Thread):
    def __init__(self, *args, **kwargs):
        socket = kwargs.pop('socket')
        interval = kwargs.pop('interval')
        threading.Thread.__init__(self, *args, **kwargs)
        self.socket = socket
        self.interval = interval / 1000
        self.daemon = True
        self._stop_event = threading.Event()
        self._last_ack = time.perf_counter()
        self._last_recv = time.perf_counter()
        self._last_send = time.perf_counter()
        self.latency = float('inf')
        self.main_id = threading.get_ident()

    def run(self):
        while not self._stop_event.wait(self.interval):
            if self._last_recv + 60 < time.perf_counter():
                func = self.socket.close(4000)
                f = asyncio.run_coroutine_threadsafe(func, self.socket.loop)
                try:
                    f.result()
                except Exception:
                    pass
                finally:
                    self.stop()
                    return

            coro = self.socket.send_heartbeat(self.payload())
            f = asyncio.run_coroutine_threadsafe(coro, self.socket.loop)
            try:
                total = 0
                while True:
                    try:
                        f.result(10)
                        break
                    except concurrent.futures.TimeoutError:
                        total += 10
                        try:
                            frame = sys._current_frames()[self.main_id]
                        except KeyError:
                            pass
            except Exception:
                self.stop()
                traceback.print_exc()
            else:
                self._last_send = time.perf_counter()

    def payload(self):
        return {
            "op": 1,
            "d": None
        }

    def stop(self):
        self._stop_event.set()
    
    def tick(self):
        self._last_recv = time.perf_counter()
    
    def ack(self):
        ack_time = time.perf_counter()
        self._last_ack = ack_time
        self.latency = ack_time - self._last_send


class Socket(object):
    """
    Connects to the Discord websocket.

    Example:
    ```
    import discsocket
    socket = discsocket.Socket()

    @socket.event('ready')
    async def ready_listener():
        print(f"{socket.user.username} is online")

    if __name__ == '__main__':
        socket.run('token')
    ```
    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop() if loop is None else loop
        self.session: aiohttp.BaseConnector = None
        self.headers = {}
        self.container = Container()
        self.thread_id = threading.get_ident()
        self.unchecked_decorators = {"events": [], "commands": []}
        self.__handler = None
        self.__gateway = None

    async def send_heartbeat(self, payload: dict):
        """
        Sends a heartbeat to the Discord websocket.
        """
        await self.__gateway.send_json(payload)

    def add_component_listener(self, parent_context, ucid, func, timeout: float = 0.0):
        """
        Adds a component listener to the current socket container.
        """

        if not inspect.iscoroutinefunction(func):
            raise TypeError("Component function must be a coroutine function.")
        self.container.add_component(Component(ucid, func, parent_context, timeout))

# ------- Decorators -------

    def event(self, name: str):
        """
        Decorator to add an event to listen for.

        ```
        import discsocket
        socket = discsocket.Socket()

        @socket.event('ready')
        async def ready_listener():
            print(f"{socket.user.username} is online")
        ```
        """

        def predicate(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("Event function must be a coroutine function.")
            self.unchecked_decorators["events"].append(Event(name, func))
        return predicate

    def command(self, name: str, _type: int):
        """
        Decorator to add a command to listen for.
        
        ```
        import discsocket
        socket = discsocket.Socket()

        @socket.command('ping', discsocket.utils.SLASH)
        async def ping(ctx):
            await ctx.callback('pong')
        ```
        """

        def predicate(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("Command function must be a coroutine function.")
            self.unchecked_decorators["commands"].append(Command(name, func, _type))
        return predicate

# ------- Command Handlers -------

    async def run_command(self, context):
        """Runs a command"""
        try:
            coro = None
            if context.type == utils.SLASH:
                coro = self.container.commands.get(context.command, None)
            elif context.type == utils.USER:
                coro = self.container.commands.get(context.command, None)
            elif context.type == utils.utils.MESSAGE:
                coro = self.container.message_commands.get(context.command, None)
            
            if coro is None:
                raise ValueError(f"Command {context.command} not found.")
            await coro(context)
        except Exception:
            traceback.print_exc()

    async def run_component_command(self, context):
        """Runs a component command."""
        component = self.container.components.get(context.ucid, None)
        if component is None:
            raise ValueError(f"Component {context.ucid} not found.")

        context.parent_context = component[2]
        
        if component[1] is not None:
            epoch = datetime.fromtimestamp(0)
            time_difference = (datetime.utcnow() - epoch).total_seconds()
            if datetime.fromtimestamp(time_difference) > component[1]:
                await context.callback('This component has timed out. Using this component again will result in an error.', ephemeral=True)
                await context.parent_context.message.disable_component(context.ucid)
                del self.container.components[context.ucid]
                return

        coro = component[0]

        try:
            await coro(context)
            await context.parent_context.message.disable_component(context.ucid)
            del self.container.components[context.ucid]
        except Exception:
            traceback.print_exc()

# ------- Connection -------

    async def before_login(self):
        # Build socket headers
        self.headers = {"Authorization": f"Bot {self.__token}"}
        self.session = aiohttp.ClientSession()
        self.user = User(await (await self.session.get('https://discord.com/api/v8/users/@me', headers=self.headers)).json())


    async def connect(self):
        """
        Establishes the connection to the Discord gateway.
        """
        await self.before_login()
        async with self.session.ws_connect("wss://gateway.discord.gg/") as connection:
            self.__gateway = connection
            async for message in self.__gateway:
                msg = json.loads(message.data)
                op, t, d = msg["op"], msg["t"], msg["d"]

                if self.__handler:
                    self.__handler.tick()

                try:
                    if op == utils.HELLO:
                        await self.__gateway.send_json(
                            {
                                "op": utils.IDENTIFY,
                                "d": {
                                    "token": self.__token,
                                    "intents": 513,
                                    "properties": {
                                        "$os": "Windows",
                                        "$browser": "discsocket {}".format(utils.__version__),
                                        "$device": "discsocket {}".format(utils.__version__)
                                    },
                                    "compress": False,
                                    "large_threshold": 250
                                }
                            }
                        )

                        self.__handler = MaintainSocketAlive(socket=self, interval=d['heartbeat_interval'])
                        await self.__gateway.send_json(self.__handler.payload())
                        self.__handler.start()

                    elif op == utils.HEARTBEAT:
                        try:
                            if self.__handler:
                                await self.__gateway.send_json(self.__handler.payload())
                        except Exception:
                            traceback.print_exc()
                    
                    elif op == utils.HEARTBEAT_ACK:
                        if self.__handler:
                            self.__handler.ack()

                    elif t == 'INTERACTION_CREATE':
                        if d['type'] == 2: # Slash command has been invoked
                            d['injected'] = {"type": utils.SLASH}
                            context = Context(self, d)
                            await self.run_command(context)
                        elif d['type'] == 3: # Component interaction
                            if d['data']['component_type'] == 3: # Select menu was used
                                context = SelectMenuContext(self, d)
                            elif d['data']['component_type'] == 2: # Button was used
                                context = ButtonContext(self, d)
                            
                            await self.run_component_command(context)
                    else:
                        if t is not None:
                            listeners = self.container.events.get(t.lower(), None)
                            if listeners is not None:
                                for coro in listeners:
                                    # Check if it needs args
                                    f = inspect.signature(coro)
                                    if len(f.parameters) > 0:
                                        await coro(d)
                                    else:
                                        await coro()

                except Exception:
                    traceback.print_exc()

# ------- Running -------

    def run(self, token: str):
        for _type in ['events', 'commands']:
            if len(self.unchecked_decorators[_type]) > 0:
                for item in self.unchecked_decorators[_type]:
                    if isinstance(item, Event):
                        self.container.add_event(item)
                    elif isinstance(item, Command):
                        self.container.add_command(item)

        self.__token = token
        self.loop.create_task(self.connect())
        self.loop.run_forever()

    def add_extension(self, path_to_extension):
        """
        Adds an extension to the socket.
        Example:
        ```
        import pathlib
        import discsocket
        
        socket = discsocket.Socket()

        for ext in pathlib.Path('name_of_folder_with_extensions').glob('*.py'):
            socket.add_extension(ext)
        ```
        """
        extension = importlib.import_module(path_to_extension)
        for name in dir(extension):
            attr = getattr(extension, name)

            if isinstance(attr, Command):
                self.container.add_command(attr)
            elif isinstance(attr, Event):
                self.container.add_event(attr)
            else:
                raise TypeError(f"{name} is not a command or event.")