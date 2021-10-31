import os
import sys
import time
import pygame
import orjson
import pyautogui
from typing import Any
from pygame import mixer
from pygame import event
from pygame import display
from typing import Callable
from typing import Iterable
from typing import Optional
from pygame.font import Font
from threading import Thread
from pygame.event import Event
from pygame.surface import Surface
import pygame.locals as pygame_locals

import pygame_button
import pygame_menu

class JsonFile:
    def __init__(self, path: str, default_config: Optional[Any] = None) -> None:
        """Should use os.path.abspath for `path`"""
        self.path = path
        self.thread_true = True

        self.default_config = default_config
        self.config: Optional[Any] = None
        self.load_config()

        self.thread = Thread(target=self.update_config)
        self.thread.start()

    def load_config(self) -> None:
        if not os.path.exists(self.path):
            open(self.path, 'w+').close()
            self.config = self.default_config or {}
        else:
            with open(self.path, 'rb') as f:
                self.config = orjson.loads(f.read())

    def sleep(self, seconds: float, result: Any) -> Any:
        for _ in range(10): 
            if not self.thread_true:
                return result
            
            time.sleep(seconds / 10)
        
        return result

    def update_config(self) -> None:
        while self.sleep(5.0, self.thread_true):
            with open(self.path, 'wb+') as f:
                f.seek(0)
                f.truncate()
                f.write(orjson.dumps(self.config))

class Eaves:
    def __init__(self) -> None:
        self.running = True
        self.thread_true = True
        self.handlers: dict = {}
        self.screen: Optional[Surface] = None
        self.current_status: str = 'main_menu'
        self.type_handlers = {
            str: lambda status: exec('self.current_status = status'),
            tuple[pygame_menu.Menu, list[Event]]: self.handle_menus
        }
        self.fps_cap: int = 60
        self.clock = pygame.time.Clock()
        self.handlers_to_load: list[str] = []
        self.res: Optional[tuple[int, int]] = None
        self._on_startup: Optional[Callable] = None
        self.config_file: Optional[ConfigFile] = None
        self._before_shutdown: Optional[Callable] = None

    @property
    def fps(self) -> float:
        return self.clock.get_fps()

    def handle_menus(self, objs: tuple[pygame_menu.Menu, list[Event]]) -> None:
        menu, events = objs
        menu.update(events)
        menu.draw(self.screen) # type: ignore

    def load_files(self, files: list[str]) -> None:
        self.handlers_to_load = files

    def on_startup(self, func: Callable) -> Callable:
        self._on_startup = func
        return func
    
    def before_shutdown(self, func: Callable) -> Callable:
        self._before_shutdown = func
        return func

    def run_for_loop(self, iter: Iterable, check: Callable) -> list[Any]:
        return [check(item) for item in iter]

    def check_if_quit(self, events: list[Event]) -> bool:
        check = lambda event: event.type == pygame_locals.QUIT
        return True in self.run_for_loop(events, check)

    def return_type_handler(self, _type: Any) -> Callable:
        def inner(func: Callable) -> Callable:
            self.type_handlers[_type] = func
            return func
        return inner

    def handler(self, name: str, func_before_running: Optional[Callable[[list[Event]], Any]] = None) -> Callable:
        def inner(func: Callable[[list[Event]], Any]) -> Callable:

            if func_before_running:
                ret = func.__annotations__['return']
                def new_func(events) -> ret:
                    return func(func_before_running(events)) # type: ignore

                self.handlers[name] = new_func
            else:
                self.handlers[name] = func
            return func
        return inner

    def get_current_screen_size(self) -> tuple[int, int]:
        return pyautogui.size()

    def get_return_type(self, func: Callable) -> Any:
        return func.__annotations__["return"]
    
    def check_resize(self, events: list[Event]) -> None:
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                old_surface_saved = self.screen
                self.res = (event.w, event.h)

                self.screen = display.set_mode(
                    (event.w, event.h),
                    pygame.RESIZABLE
                )

                self.screen.blit(old_surface_saved, (0,0)) # type: ignore
                del old_surface_saved

    def render_text(
        self, font: Font,
        text: str, antialias: bool = True,
        color: tuple[int, int, int] = (255, 255, 255), 
        background: Optional[tuple[int, int, int]] = None,
        location: tuple[int, int] = (0, 0)
    ) -> None:
        source = font.render(text, antialias, color, background)
        self.screen.blit(source, location) # type: ignore

    def run(
        self, window_caption: str,
        screen_size: Optional[tuple[int, int]] = None,
        window_type: int = pygame.RESIZABLE
    ) -> None:

        if self.handlers_to_load:
            for file in self.handlers_to_load:
                if not file.endswith('.py'):
                    continue
                
                name = file[:-3].replace('//', '.').replace(r'/', '.')
                __import__(name)

        # init package
        pygame.init()
        mixer.pre_init(44100, -16, 2, 2048)
        mixer.init()

        # set screen
        if not screen_size:
            self.res = self.get_current_screen_size()
        else: 
            self.res = screen_size
        
        self.screen = display.set_mode(self.res, window_type)
        display.set_caption(window_caption)

        if self._on_startup:
            self._on_startup()

        while self.running:

            events = event.get()
            if self.check_if_quit(events):
                self.running = False
                break
            
            if window_type == pygame.RESIZABLE:
                self.check_resize(events)
            
            func: Callable = self.handlers[self.current_status]
            _type = func.__annotations__["return"]
            
            data = func(events)
            if data: self.type_handlers[_type](data)

            self.clock.tick(self.fps_cap)

            display.flip()
            display.update()

        self.thread_true = False
        if self.config_file:
            self.config_file.thread_true = False

        if self._before_shutdown:
            self._before_shutdown()
        
        pygame.quit()
        sys.exit()