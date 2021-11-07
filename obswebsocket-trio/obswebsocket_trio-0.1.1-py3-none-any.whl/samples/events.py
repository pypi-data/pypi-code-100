#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

import trio
import typer

logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket_trio import open_obs_websocket, events  # noqa: E402


def on_event(message):
    print(f"Got message: {message}")


def on_switch(message):
    print(f"You changed the scene to {message.getSceneName()}")


async def main(host: str = 'localhost', port: int = 4444, password: str = 'secret'):
    async with open_obs_websocket(host, port, password) as ws:
        ws.register(on_event)
        ws.register(on_switch, events.SwitchScenes)
        while True:
            await trio.sleep_forever()


def cli_args(host: str = 'localhost', port: int = 4444, password: str = 'secret'):
    trio.run(main, host, port, password)


if __name__ == '__main__':
    typer.run(cli_args)
