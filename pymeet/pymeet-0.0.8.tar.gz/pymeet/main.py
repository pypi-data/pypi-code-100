from typing import Tuple

from .app import PygameApp
from pymeet.app.game.server.scene import GameServerScene


class PyMeet:
    def __init__(self, dimension: Tuple[int, int], fps: int):
        scene = GameServerScene()
        self.app_client = PygameApp(dimension, fps, scene=scene)

    def start(self):
        self.app_client.loop()


def main():
    app = PyMeet((1080, 720), 30)
    app.start()


if __name__ == '__main__':
    main()
