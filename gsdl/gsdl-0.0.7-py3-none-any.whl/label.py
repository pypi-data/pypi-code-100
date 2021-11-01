from .utils import *
from .frame import GFrame
import pygame


class GLabel:
    def __init__(
            self,
            parent: Union[GFrame, None],
            text: str,
            font: Union[pygame.font.Font, str],
            font_size: int = 0,
            color: tuple = (255, 255, 255),
            bg_color: tuple = None,
            x: int = 0,
            y: int = 0,
            w: int = 0,
            h: int = 0,
            alpha: bool = True,
            auto_size: bool = True,
            stretch: bool = False,
            alpha_blend: int = 255,
            anti_aliasing: bool = True,
            z_order: int = 0
    ):
        super(GLabel, self).__init__()
        self.parent = parent
        self.surface = parent.surface if parent else pygame.Surface((1, 1))
        self.x = x
        self.y = y
        self.alpha = alpha
        self.w, self.h = w, h
        self.text = text
        self.bg_color = bg_color
        self.color = color
        self.orig_image = self.surface
        self.image = self.orig_image
        self.auto_size = auto_size
        self.anti_aliasing = anti_aliasing
        self.stretch = stretch
        self.is_visible = True
        self.is_pressed = False
        self.catch_mouse = False
        self.catch_keyboard = False
        self.z_order = z_order
        self.alpha_blend = alpha_blend
        self.font_size = font_size
        self.font = self.to_font(font)
        self.update_text()
        if not self.w or not self.h:
            self.w, self.h = self.image.get_size()
        if stretch:
            self.resize(self.w, self.h)
        if parent:
            self.parent.add_child(self)

    def set_text(self, new_text: str):
        self.text = new_text
        self.update_text()

    def update_text(self) -> None:
        self.orig_image = self.font.render(
            self.text, self.anti_aliasing, self.color, self.bg_color
        )
        if self.stretch:
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
        else:
            self.image = self.orig_image
        if self.auto_size:
            self.w, self.h = self.image.get_size()
        self.image.set_alpha(self.alpha_blend)

    def to_font(self, font) -> pygame.font.Font:
        if type(font) == str:
            return pygame.font.Font(font, self.font_size)
        return font

    def resize(self, w: int, h: int) -> None:
        if self.auto_size:
            return
        self.w = w
        self.h = h
        if self.stretch:
            self.image = pygame.transform.scale(self.orig_image, (w, h))

    def draw(self, delta: float, parent: GFrame) -> None:
        if not self.parent:
            if not parent:
                return
            self.parent = parent
        if self.auto_size:
            self.surface.blit(
                self.image,
                (self.x + self.parent.scroll_x, self.y + self.parent.scroll_y)
            )
        else:
            self.surface.blit(
                self.image,
                (self.x + self.parent.scroll_x, self.y + self.parent.scroll_y),
                (self.x, self.y, self.w, self.h)
            )

    def to_pil_image(self) -> Image.Image:
        return from_image(self.image)

    def set_alpha(self, alpha: int):
        self.alpha_blend = alpha
        self.image.set_alpha(alpha)

    def on_mouse_move(self, x: int, y: int) -> None:
        pass

    def on_mouse_down(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_mouse_up(self, x: int, y: int, button: int = 0) -> None:
        pass

    def on_mouse_leave(self, x: int, y: int) -> None:
        pass

