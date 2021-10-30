from enum import Enum
from typing import NamedTuple
from PIL import Image

from OpenGL import GL as gl


class Filter(Enum):
    NEAREST = gl.GL_NEAREST
    LINEAR = gl.GL_LINEAR


class Wrap(Enum):
    CLAMP = gl.GL_CLAMP
    REPEAT = gl.GL_REPEAT


TextureDesc = NamedTuple(
    "TextureDesc", [("path", str), ("filter", Filter), ("wrap", Wrap)]
)


class Texture:
    def __init__(self, desc: TextureDesc) -> None:
        image = Image.open(desc.path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        self.width = image.width
        self.height = image.height
        image_data = image.convert("RGBA").tobytes()

        self._texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, desc.wrap.value)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, desc.wrap.value)
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, desc.filter.value
        )
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, desc.filter.value
        )

        gl.glTexImage2D(
            gl.GL_TEXTURE_2D,
            0,
            gl.GL_RGBA,
            image.width,
            image.height,
            0,
            gl.GL_RGBA,
            gl.GL_UNSIGNED_BYTE,
            image_data,
        )

    def bind(self, slot: int = 0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + slot)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._texture)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
