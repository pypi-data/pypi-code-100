from typing import Optional
from abc import ABC, abstractmethod
from pygame import Surface


class AppScene(ABC):
    @abstractmethod
    def update(self, screen: Surface):
        pass

    @abstractmethod
    def on_enter(self, manager: 'AppSceneManager', scene_prev: 'AppScene' = None):
        pass

    @abstractmethod
    def on_exit(self, scene_next: 'AppScene' = None):
        pass


class AppSceneManager:
    def __init__(self, scene: AppScene = None):
        self._scene: Optional[AppScene] = None

        if scene:
            self.switch_to_scene(scene)

    def switch_to_scene(self, scene: AppScene):
        if self._scene:
            self._scene.on_exit(scene_next=scene)

        scene_prev = self._scene
        self._scene = scene

        self._scene.on_enter(self, scene_prev=scene_prev)
