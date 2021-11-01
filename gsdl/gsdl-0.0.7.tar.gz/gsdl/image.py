from .utils import *
from .frame import GFrame
from io import BytesIO
from _io import BufferedReader
import pygame


class GImage:
    def __init__(
            self,
            parent: GFrame,
            image: Union[pygame.Surface, Image.Image, BytesIO, BufferedReader, str, bytes],
            x: int = 0,
            y: int = 0,
            w: int = 0,
            h: int = 0,
            alpha: bool = True,
            auto_size: bool = True,
            stretch: bool = False,
            alpha_blend: int = 255,
            z_order: int = 0
    ):
        super(GImage, self).__init__()
        self.parent = parent
        self.surface = parent.surface
        self.x = x
        self.y = y
        self.alpha = alpha
        self.w, self.h = w, h
        self.orig_image = self.surface
        self.image = self.orig_image
        self.auto_size = auto_size
        self.stretch = stretch
        self.is_visible = True
        self.catch_mouse = False
        self.is_pressed = False
        self.catch_keyboard = False
        self.alpha_blend = alpha_blend
        self.update_image(image)
        self.z_order = z_order
        if not self.w or not self.h:
            self.w, self.h = self.image.get_size()
        if not alpha_blend == 255:
            self.set_alpha_blend(alpha_blend)
        if stretch:
            self.resize(self.w, self.h)
        self.parent.add_child(self)

    def to_img(self, image: any) -> pygame.Surface:
        tp = type(image)
        if tp == pygame.Surface:
            return image
        if tp == Image.Image:
            return to_image(image, alpha=self.alpha)
        if tp == str and file_exists(image):
            return pygame.image.load(image)
        if 'read' in dir(tp):
            return to_image(Image.open(tp), alpha=self.alpha)
        raise RuntimeError('Can\'t load image: ' + str(tp))

    def update_image(self, image: Union[pygame.Surface, Image.Image, BytesIO, BufferedReader, str, bytes]):
        if self.alpha:
            self.orig_image = self.to_img(image).convert_alpha()
        else:
            self.orig_image = self.to_img(image).convert()
        self.image = self.orig_image
        if self.auto_size:
            self.w, self.h = self.image.get_size()
        else:
            self.w, self.h = self.w, self.h
        self.image.set_alpha(self.alpha_blend)

    def resize(self, w: int, h: int) -> None:
        if self.auto_size:
            return
        self.w = w
        self.h = h
        if self.stretch:
            self.image = pygame.transform.scale(self.orig_image, (w, h))

    def to_pil_image(self) -> Image.Image:
        return from_image(self.image)

    def draw(self, delta: float, parent: GFrame) -> None:
        self.parent.surface.blit(
            self.image,
            (self.x + self.parent.scroll_x, self.y + self.parent.scroll_y),
            None if self.stretch else (0, 0, self.w, self.h)
        )

    def set_alpha_blend(self, alpha: int):
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
