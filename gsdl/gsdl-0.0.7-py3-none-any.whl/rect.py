from .utils import *
from .frame import GFrame
import pygame


class GRect:
    def __init__(
            self,
            parent: GFrame,
            x: int = 0,
            y: int = 0,
            w: int = 0,
            h: int = 0,
            color: tuple = (0, 0, 0),
            width: int = 0,
            border_radius: int = -1,
            border_top_left_radius: int = -1,
            border_top_right_radius: int = -1,
            border_bottom_left_radius: int = -1,
            border_bottom_right_radius: int = -1,
            z_order: int = 0
    ):
        super(GRect, self).__init__()
        self.parent = parent
        self.surface = parent.surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.catch_keyboard = False
        self.catch_mouse = False
        self.is_visible = True
        self.color = color
        self.width = width
        self.is_pressed = False
        self.border_radius = border_radius
        self.border_top_left_radius = border_top_left_radius
        self.border_top_right_radius = border_top_right_radius
        self.border_bottom_left_radius = border_bottom_left_radius
        self.border_bottom_right_radius = border_bottom_right_radius
        self.z_order = z_order
        self.parent.add_child(self)

    def draw(self, delta: int, parent: GFrame):
        pygame.draw.rect(
            self.surface,
            self.color,
            (self.x, self.y, self.w, self.h),
            self.width,
            self.border_radius,
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        )

    def on_mouse_move(self, x: int, y: int) -> None:
        pass

    def on_mouse_down(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_mouse_up(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_mouse_leave(self, x: int, y: int) -> None:
        pass
