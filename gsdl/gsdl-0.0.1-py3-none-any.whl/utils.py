import os
import sys
import json
import pygame
from typing import Optional, Tuple, List, Union, IO, Literal
from PIL import Image
try:
    import android
    is_android = True
    from android.permissions import request_permissions, Permission
except ImportError:
    is_android = False


encoding_ = sys.getdefaultencoding()
force_fullscreen = is_android
force_fullscreen_flag = pygame.FULLSCREEN if force_fullscreen else 0
cur_path = os.getcwd()


def request_storage_permissions() -> None:
    if not is_android:
        return
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE
    ])


def p(*path) -> str:
    return os.path.join(cur_path, *path)


def to_image(pillow_img: Image.Image, alpha=True) -> pygame.Surface:
    result = pygame.image.fromstring(
        pillow_img.tobytes(), pillow_img.size, pillow_img.mode
    )
    return result.convert_alpha() if alpha else result.convert()


def from_image(pygame_image: pygame.Surface, mode: str = 'RGBA', is_flipped: bool = False) -> Image.Image:
    return Image.frombytes(
        mode,
        pygame_image.get_size(),
        pygame.image.tostring(
            pygame_image,
            mode,
            is_flipped
        ),
    )


def file_exists(filename: str) -> bool:
    return os.access(filename, os.F_OK)


def fast_read(filename: str, response_type: type = str, encoding: str = 'utf-8') -> Union[str, bytes]:
    temp_file = open(filename, 'rb')
    result = temp_file.read()
    temp_file.close()
    return result if not response_type == str else result.decode(encoding)


def fast_write(filename: str, content) -> int:
    temp_file = open(filename, 'w' if type(content) == str else 'wb')
    result = temp_file.write(content)
    temp_file.close()
    return result


def read_json(filename: str) -> dict:
    return json.loads(fast_read(filename))


def write_json(filename: str, json_: dict) -> int:
    return fast_write(filename, json.dumps(json_))


def is_object_colliding(object_: any, x: int, y: int) -> bool:
    return object_.x + object_.w > x > object_.x and object_.y + object_.h > y > object_.y
