#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import logging
from contextlib import asynccontextmanager
from typing import Union

import trio
import trio_websocket as tws

from . import exceptions
from . import base_classes
from . import events

LOG = logging.getLogger(__name__)


class ObsWS(trio.abc.AsyncResource):
    """
    Core class for using obs-websocket-py

    Simple usage:
        >>> import obswebsocket_trio, obswebsocket_trio.requests as obsrequests
        >>> async with obswebsocket.open_obs_websocket("localhost", 4444, "secret") as client:
        >>>     await client.call(obsrequests.GetVersion()).getObsWebsocketVersion()
        '4.1.0'

    For advanced usage, including events callback, see the 'samples' directory.
    """

    def __init__(self, nursery: trio.Nursery, host='localhost', port=4444, password=''):
        """
        Construct a new obsws wrapper

        :param nursery: A trio Nursery to run background tasks
        :param host: Hostname to connect to
        :param port: TCP Port to connect to (Default is 4444)
        :param password: Password for the websocket server (Leave this field
            empty if no auth enabled on the server)
        """
        self.id = 1
        self.ws: Union[None, tws.WebSocketConnection] = None
        self.eventmanager = EventManager()
        self.answers = {}
        self._nursery = nursery
        self.closed: bool = True

        self.host = host
        self.port = port
        self.password = password

    async def connect(self, autoreconnect: bool = True):
        """
        Connect to the websocket server
        :param autoreconnect: If True, tries to reconnect every 2 seconds if disconnected.

        :return: Nothing
        """
        if not self.closed:
            return

        while True:
            try:
                LOG.info('Connecting...')
                self.ws = await tws.connect_websocket(self._nursery, self.host, self.port, '/', use_ssl=False,
                                                      message_queue_size=20)
                LOG.info('Connected!')
                self.closed = False
                await self._auth(self.password)
            except (tws.HandshakeError, OSError) as e:
                if not autoreconnect:
                    raise exceptions.ConnectionFailure(str(e))
                LOG.info('Could not connect, retrying...')
                await trio.sleep(2)
            else:
                break

        self._nursery.start_soon(self._handle_messages)
        if autoreconnect:
            self._nursery.start_soon(self._auto_reconnect)

    async def _auto_reconnect(self):
        while True:
            try:
                if self.ws.closed:
                    await self.reconnect()
            except AttributeError:
                await self.connect(False)  # Prevent infinite recursion
            await trio.sleep(2)

    async def reconnect(self):
        """
        Restart the connection to the websocket server

        :return: Nothing
        """
        await self.disconnect()
        await self.connect()

    async def disconnect(self):
        """
        Disconnect from websocket server

        :return: Nothing
        """
        LOG.info('Disconnecting...')
        try:
            await self.ws.aclose()
        except AttributeError:
            pass
        self.closed = True

    async def aclose(self):
        self._nursery.cancel_scope.cancel()
        await self.disconnect()

    async def _auth(self, password):
        if self.closed:
            raise trio.ClosedResourceError()

        auth_payload = {
            'request-type': 'GetAuthRequired',
            'message-id': str(self.id),
        }
        self.id += 1
        await self.ws.send_message(json.dumps(auth_payload))
        result = json.loads(await self.ws.get_message())

        if result['status'] != 'ok':
            raise exceptions.ConnectionFailure(result['error'])

        if result.get('authRequired'):
            secret = base64.b64encode(
                hashlib.sha256(
                    (password + result['salt']).encode('utf-8')
                ).digest()
            )
            auth = base64.b64encode(
                hashlib.sha256(
                    secret + result['challenge'].encode('utf-8')
                ).digest()
            ).decode('utf-8')

            auth_payload = {
                "request-type": "Authenticate",
                "message-id": str(self.id),
                "auth": auth,
            }
            self.id += 1
            await self.ws.send_message(json.dumps(auth_payload))
            result = json.loads(await self.ws.get_message())
            if result['status'] != 'ok':
                raise exceptions.ConnectionFailure(result['error'])

    async def call(self, obj) -> base_classes.Baserequests:
        """
        Make a call to the OBS server through the Websocket.

        :param obj: Request (class from obswebsocket.requests module) to send
            to the server.
        :return: Request object populated with response data.
        """
        if self.closed:
            raise trio.ClosedResourceError()

        if not isinstance(obj, base_classes.Baserequests):
            raise exceptions.ObjectError('Call parameter is not a request object')
        payload = obj.data()
        r = await self.send(payload)
        obj.input(r)
        return obj

    async def send(self, data: dict) -> dict:
        """
        Make a raw json call to the OBS server through the Websocket.

        :param data: Request (python dict) to send to the server. Do not
            include field "message-id".
        :return: Response (python dict) from the server.
        """
        if self.closed:
            raise trio.ClosedResourceError()

        message_id = str(self.id)
        self.id += 1
        data['message-id'] = message_id
        LOG.debug('Sending message id %s: %s', message_id, data)
        await self.ws.send_message(json.dumps(data))

        try:
            with trio.fail_after(60):
                return await self._wait_message(message_id)
        except trio.TooSlowError:
            raise exceptions.MessageTimeout(f'No answer for message {message_id}')

    async def _wait_message(self, message_id):
        while True:
            if message_id in self.answers:
                return self.answers.pop(message_id)
            await trio.sleep(0.1)

    async def _handle_messages(self):
        if self.closed:
            raise trio.ClosedResourceError()
        while True:
            message = ""
            try:
                message = await self.ws.get_message()

                if not message:
                    continue

                result = json.loads(message)
                if 'update-type' in result:
                    LOG.debug('Got message: %s', result)
                    obj = self.build_event(result)
                    self.eventmanager.trigger(obj)
                elif 'message-id' in result:
                    LOG.debug('Got answer for id %s: %s',
                              result['message-id'], result)
                    self.answers[result['message-id']] = result
                else:
                    LOG.warning('Unknown message: %s', result)
            except tws.ConnectionClosed:
                await self.reconnect()
            except (ValueError, exceptions.ObjectError) as e:
                LOG.warning('Invalid message: %s (%s)', message, e)

    @staticmethod
    def build_event(data):
        name = data['update-type']
        try:
            obj = getattr(events, name)()
        except AttributeError:
            raise exceptions.ObjectError(f'Invalid event {name}')
        obj.input(data)
        return obj

    def register(self, func, event=None):
        """
        Register a new hook in the websocket client

        :param func: Callback function pointer for the hook
        :param event: Event (class from obswebsocket.events module) to trigger
            the hook on. Default is None, which means trigger on all events.
        :return: Nothing
        """
        self.eventmanager.register(func, event)

    def unregister(self, func, event=None):
        """
        Unregister a new hook in the websocket client

        :param func: Callback function pointer for the hook
        :param event: Event (class from obswebsocket.events module) which
            triggered the hook on. Default is None, which means unregister this
            function for all events.
        :return: Nothing
        """
        self.eventmanager.unregister(func, event)


@asynccontextmanager
async def open_obs_websocket(host: str = 'localhost', port: int = 4444, password: str = '',
                             autoreconnect: bool = True) -> ObsWS:
    async with trio.open_nursery() as nursery:
        async with ObsWS(nursery, host, port, password) as ws:
            await ws.connect(autoreconnect)
            yield ws


class EventManager(object):
    def __init__(self):
        self.functions = []

    def register(self, callback, trigger):
        self.functions.append((callback, trigger))

    def unregister(self, callback, trigger):
        for c, t in self.functions:
            if (c == callback) and (trigger is None or t == trigger):
                self.functions.remove((c, t))

    def trigger(self, data):
        for callback, trigger in self.functions:
            if trigger is None or isinstance(data, trigger):
                callback(data)
