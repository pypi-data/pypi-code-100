from .utils import *
from .frame import GFrame
from .label import GLabel
import pygame


class GWinButton:  # TODO: add GAnimatedWinButton
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
            border_radius: int = -1,
            border_top_left_radius: int = -1,
            border_top_right_radius: int = -1,
            border_bottom_left_radius: int = -1,
            border_bottom_right_radius: int = -1,
            z_order: int = 0
    ):
        super(GWinButton, self).__init__()
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
        self.is_enabled = True
        self.last_btn = 0
        self.is_pressed = False
        self.z_order = z_order
        self.color = (225, 225, 225)
        self.hover_color = (229, 241, 251)
        self.click_color = (205, 228, 247)
        self.border_color = (173, 173, 173)
        self.border_hover_color = (0, 120, 215)
        self.border_click_color = (1, 85, 154)
        self.border_radius = border_radius
        self.border_top_left_radius = border_top_left_radius
        self.border_top_right_radius = border_top_right_radius
        self.border_bottom_left_radius = border_bottom_left_radius
        self.border_bottom_right_radius = border_bottom_right_radius
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
        col, b_col = (self.click_color, self.border_click_color) if self.is_pressed and self.last_btn == 1 else ((self.hover_color, self.border_hover_color) if self.is_colliding else (self.color, self.border_color))
        pygame.draw.rect(
            self.surf,
            col,
            (0, 0, self.w, self.h),
            0,
            self.border_radius,
            self.border_top_left_radius,
            self.border_top_right_radius,
            self.border_bottom_left_radius,
            self.border_bottom_right_radius
        )
        pygame.draw.rect(
            self.surf,
            b_col,
            (0, 0, self.w, self.h),
            1,
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

    def on_mouse_enter(self):
        pass

    def on_mouse_up(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_click(self, x, y):
        pass

    def on_mouse_move_(self, x: int, y: int) -> None:
        if self.is_pressed and self.last_btn == 1:
            if not is_object_colliding(self, x, y):
                self.is_colliding = False
                return self.on_mouse_move(x, y)
        if not self.is_colliding:
            self.is_colliding = True
            self.on_mouse_enter()
        self.on_mouse_move(x, y)

    def on_mouse_leave_(self, x: int, y: int) -> None:
        self.is_colliding = False
        self.on_mouse_leave(x, y)

    def on_mouse_down_(self, x: int, y: int, button: int = 0) -> None:
        self.on_mouse_down(x, y, button)

    def on_mouse_up_(self, x: int, y: int, button: int = 0) -> None:
        self.on_mouse_up(x, y, button)
        if self.last_btn == button == 1 and self.is_colliding:
            self.on_click(x, y)
