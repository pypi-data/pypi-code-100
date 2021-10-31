from typing import Tuple, Callable, Any, Dict, Optional
import pygame

from .base import AppScene, AppSceneManager


DimensionType = Tuple[int, int]

pygame.init()


KeyHandlerType = Callable[[str], Any]


class PygameApp(AppSceneManager):
    def __init__(self, dimension: DimensionType, fps: int = 30, *, scene: AppScene = None):
        self._key_pressed_handler: Dict[int, KeyHandlerType] = {}

        self._dimension: DimensionType = dimension
        self._fps: int = fps

        super().__init__(scene)

        self.running: bool = False

    @property
    def dimension(self) -> DimensionType:
        return self._dimension

    def loop(self):
        screen = pygame.display.set_mode(self._dimension)
        clock = pygame.time.Clock()

        self.running = True
        while self.running:
            self._handle_events()
            if self._scene:
                self._scene.update(screen)

            pygame.display.flip()
            clock.tick(self._fps)

    def set_key_pressed_handler(self, key: str, handler: KeyHandlerType):
        code = pygame.key.key_code(key)
        self._key_pressed_handler[code] = handler

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._handle_exit_event()
                self.running = False

        pressed = pygame.key.get_pressed()
        for code, handler in self._key_pressed_handler.items():
            if pressed[code]:
                name = pygame.key.name(code)
                handler(name)

    def _handle_exit_event(self):
        self._scene.on_exit(scene_next=None)
