from typing import Optional, Set
from pygame import Surface

from pymeet.core import usecase

from pymeet.app.base import AppScene
from pymeet.app.app import PygameApp

from .renderer import GameServerSceneRenderer


class GameServerScene(AppScene):
    def __init__(self):
        self._app: Optional[PygameApp] = None
        self._renderer: Optional[GameServerSceneRenderer] = None
        self._main_character_id = '000'

        self._tmp_walk_keys: Set[str] = set()

    def _set_handlers(self):
        for key in 'wasd':
            self._app.set_key_pressed_handler(key, self._handle_walk_key_pressed)

    def _handle_walk_key_pressed(self, key):
        self._tmp_walk_keys.add(key)

    def _process_key_pressed(self):
        if 'w' in self._tmp_walk_keys and 's' in self._tmp_walk_keys:
            self._tmp_walk_keys -= {'w', 's'}
        if 'a' in self._tmp_walk_keys and 'd' in self._tmp_walk_keys:
            self._tmp_walk_keys -= {'a', 'd'}

        direction = None
        if self._tmp_walk_keys == {'w', 'd'}:
            direction = 'UP_RIGHT'
        elif self._tmp_walk_keys == {'w', 'a'}:
            direction = 'UP_LEFT'
        elif self._tmp_walk_keys == {'s', 'd'}:
            direction = 'DOWN_RIGHT'
        elif self._tmp_walk_keys == {'s', 'a'}:
            direction = 'DOWN_LEFT'
        elif self._tmp_walk_keys == {'w'}:
            direction = 'UP'
        elif self._tmp_walk_keys == {'a'}:
            direction = 'LEFT'
        elif self._tmp_walk_keys == {'s'}:
            direction = 'DOWN'
        elif self._tmp_walk_keys == {'d'}:
            direction = 'RIGHT'

        if direction:
            usecase.character.walk(self._main_character_id, direction)

        self._tmp_walk_keys = set()

    def update(self, screen: Surface):
        self._renderer.render(screen)

        self._process_key_pressed()

        usecase.server.update_server()

    def on_enter(self, manager: PygameApp, scene_prev: AppScene = None):
        self._app = manager
        self._renderer = GameServerSceneRenderer(dimension=self._app.dimension)

        self._set_handlers()

        usecase.server.start_server()

    def on_exit(self, scene_next: AppScene = None):
        pass
