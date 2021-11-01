from .utils import *
from .frame import GFrame
from .label import GLabel
import pygame


class GSimpleButton:
    def __init__(
            self,
            parent: GFrame,
            text: str,
            font: Union[pygame.font.Font, str],
            font_size: int = 0,
            text_color: tuple = (0, 0, 0),
            anti_aliasing: bool = True,
            x: int = 0,
            y: int = 0,
            w: int = 0,
            h: int = 0,
            color: tuple = (0, 255, 0),
            hover_color: tuple = (0, 255, 0),
            width: int = 5,
            border_radius: int = -1,
            border_top_left_radius: int = -1,
            border_top_right_radius: int = -1,
            border_bottom_left_radius: int = -1,
            border_bottom_right_radius: int = -1,
            z_order: int = 0
    ):
        super(GSimpleButton, self).__init__()
        self.parent = parent
        self.surface = parent.surface
        self.surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.catch_keyboard = False
        self.catch_mouse = True
        self.is_visible = True
        self.color = color
        self.hover_color = hover_color
        self.width = width
        self.is_pressed = False
        self.border_radius = border_radius
        self.border_top_left_radius = border_top_left_radius
        self.border_top_right_radius = border_top_right_radius
        self.border_bottom_left_radius = border_bottom_left_radius
        self.border_bottom_right_radius = border_bottom_right_radius
        self.z_order = z_order
        self.label = GLabel(
            None,
            text,
            font,
            font_size,
            text_color,
            auto_size=True,
            stretch=False,
            anti_aliasing=anti_aliasing
        )
        self.text_w, self.text_h = self.label.orig_image.get_size()
        self.label_pos = (
            round(self.w / 2 - self.text_w / 2),
            round(self.h / 2 - self.text_h / 2)
        )
        self.is_colliding = False
        self.parent.add_child(self)

    def update(self):
        self.text_w, self.text_h = self.label.orig_image.get_size()
        self.label_pos = (
            round(self.w / 2 - self.text_w / 2),
            round(self.h / 2 - self.text_h / 2)
        )

    def draw(self, delta: int, parent: GFrame):
        self.surf.fill((0, 0, 0, 0))
        pygame.draw.rect(
            self.surf,
            self.hover_color if self.is_colliding and self.is_pressed else self.color,
            (0, 0, self.w, self.h),
            0 if self.is_colliding else self.width,
            self.border_radius,
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        )
        self.surf.blit(self.label.orig_image, self.label_pos)
        self.surface.blit(self.surf, (self.x + self.parent.scroll_x, self.y + self.parent.scroll_y))

    def on_mouse_move(self, x: int, y: int) -> None:
        pass

    def on_mouse_leave(self, x: int, y: int) -> None:
        pass

    def on_mouse_down(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_mouse_up(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_click(self, x, y):
        pass

    def on_mouse_move_(self, x: int, y: int) -> None:
        self.is_colliding = True
        if self.is_pressed and self.is_colliding:
            if not is_object_colliding(self, x + self.parent.x, y + self.parent.y):
                self.is_colliding = False
        self.on_mouse_move(x, y)

    def on_mouse_leave_(self, x: int, y: int) -> None:
        self.is_colliding = False
        self.on_mouse_leave(x, y)

    def on_mouse_down_(self, x: int, y: int, button: int = 0) -> None:
        self.on_mouse_down(x, y, button)

    def on_mouse_up_(self, x: int, y: int, button: int = 0) -> None:
        self.on_mouse_up(x, y, button)
        if self.is_colliding:
            self.on_click(x, y)
