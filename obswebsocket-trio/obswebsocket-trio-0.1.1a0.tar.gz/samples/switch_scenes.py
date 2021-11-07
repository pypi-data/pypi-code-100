#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

import trio
import typer

logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket_trio import open_obs_websocket, requests  # noqa: E402


async def main(host: str = 'localhost', port: int = 4444, password: str = 'secret'):
    async with open_obs_websocket(host, port, password) as ws:
        scenes = await ws.call(requests.GetSceneList())
        for s in scenes.getScenes():
            name = s['name']
            print(f"Switching to {name}")
            await ws.call(requests.SetCurrentScene(name))
            await trio.sleep(2)

        print('End of list')


def cli_args(host: str = 'localhost', port: int = 4444, password: str = 'secret'):
    trio.run(main, host, port, password)


if __name__ == '__main__':
    typer.run(cli_args)
