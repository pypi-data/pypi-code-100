from .utils import *
import pygame


class GFrame:
    def __init__(
            self,
            surface: pygame.Surface = None,
            x: int = 0,
            y: int = 0,
            w: int = 0,
            h: int = 0,
            is_main_window: bool = False,
            flags: int = 0,
            depth: int = None,
            display: int = None,
            vsync: int = None
    ):
        super(GFrame, self).__init__()
        self.surface = surface if surface else pygame.Surface((w, h), flags, depth)
        self.x = x
        self.y = y
        self.w = w if w else surface.get_size()[0]
        self.h = h if h else surface.get_size()[1]
        self.is_main_window = is_main_window
        self.scroll_x = 0
        self.scroll_y = 0
        self.flags = flags if flags else self.surface.get_flags()
        self.depth = depth
        self.display = display
        self.vsync = vsync
        self.bg_color = (0, 0, 0)
        self.is_visible = True
        self.catch_mouse = True
        self.catch_keyboard = True
        self.child = []

    def on_before_update(self) -> None:
        pass

    def on_after_update(self) -> None:
        pass

    def on_resize(self, w: int, h: int) -> None:
        pass

    def on_quit(self) -> None:
        pass

    def on_global_mouse_move(self, x: int, y: int) -> None:
        pass

    def on_global_mouse_down(self, x: int, y: int) -> None:
        pass

    def on_global_mouse_up(self, x: int, y: int) -> None:
        pass

    def on_mouse_move(self, x: int, y: int) -> None:
        pass

    def on_mouse_down(self, x: int, y: int) -> None:
        pass

    def on_mouse_up(self, x: int, y: int) -> None:
        pass

    def on_global_mouse_move_(self, x: int, y: int) -> None:
        if self.is_main_window:
            self.on_global_mouse_move(x, y)
        for child in self.child:
            if not child.is_visible or not is_object_colliding(child, x - self.scroll_x, y - self.scroll_y):
                continue
            if child.catch_mouse:
                return child.on_mouse_move_(x - self.scroll_x, y - self.scroll_y)
            else:
                return child.on_mouse_move(x - self.scroll_x, y - self.scroll_y)
        return self.on_mouse_move(x, y)

    def on_global_mouse_down_(self, x: int, y: int) -> None:
        if self.is_main_window:
            self.on_global_mouse_down(x, y)

    def on_global_mouse_up_(self, x: int, y: int) -> None:
        if self.is_main_window:
            self.on_global_mouse_up(x, y)

    def on_key_down(self, key_dict: dict) -> None:
        pass

    def on_key_up(self, key_dict: dict) -> None:
        pass

    def on_key_down_(self, key_dict: dict) -> None:
        for child in self.child:
            if child.catch_keyboard and child.on_key_down_(key_dict):
                return
        self.on_key_down(key_dict)

    def on_key_up_(self, key_dict: dict) -> None:
        for child in self.child:
            if child.catch_keyboard and child.on_key_down_(key_dict):
                return
        self.on_key_up(key_dict)

    def add_child(self, child: any) -> None:
        self.child.append(child)

    def remove_child(self, child: any) -> None:
        self.child.remove(child)

    def draw(self, delta: int, parent: any = None):
        self.on_before_update()
        self.surface.fill(self.bg_color)
        if parent:
            parent.surface.blit(self.surface, (self.x, self.y))
        for child in self.child:
            if not child.is_visible:
                continue
            child.draw(delta, parent=self)
        self.on_after_update()

    def process_events(self, events: list) -> None:
        if not self.is_main_window:
            return
        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.w, self.h = self.surface.get_size()
                self.on_resize(self.w, self.h)
                continue
            if event.type == pygame.MOUSEMOTION:
                x, y = pygame.mouse.get_pos()
                self.on_global_mouse_move_(x, y)
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                self.on_global_mouse_down_(x, y)
                continue
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                self.on_global_mouse_up_(x, y)
                continue
            if event.type == pygame.KEYDOWN:
                self.on_key_down_(event.dict)
                continue
            if event.type == pygame.KEYUP:
                self.on_key_up_(event.dict)
                continue
            if event.type == pygame.QUIT:
                self.on_quit()
                continue

    def resize(self, w: int, h: int) -> pygame.Surface:
        if self.is_main_window:
            self.surface = pygame.display.set_mode(
                (w, h),
                self.surface.get_flags(),
                self.depth, self.display, self.vsync
            )
        else:
            self.surface = pygame.transform.scale(self.surface, (w, h))
        self.w, self.h = self.surface.get_size()
        return self.surface

    def to_pillow_image(self) -> Image:
        return from_image(self.surface)
