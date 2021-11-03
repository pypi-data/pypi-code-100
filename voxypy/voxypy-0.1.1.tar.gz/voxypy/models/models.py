import numpy as np

from voxypy.numpy_vox_io.models import Vox
from voxypy.numpy_vox_io.parser import VoxParser

import logging

from voxypy.numpy_vox_io.writer import VoxWriter

log = logging.getLogger()


def validate_and_pad_texture(tex):
    if len(tex) > 255:
        raise ValueError(f"Invalid length of texture {len(tex)}. Expected 255 RGB 3-tuples.")
    elif len(tex) < 255:
        # pad incomplete texture
        tex.extend([(0, 0, 0)] * (255 - len(tex)))
    for color in tex:
        if type(color) != tuple:
            raise ValueError(f"Failed to parse color {color}. Expected RGB 3-tuple.")
        if len(color) != 3:
            raise ValueError(f"Failed to parse color {color}. Expected RGB 3-tuple.")
        for channel in color:
            if type(channel) != int:
                raise ValueError(f"Invalid type {type(channel)} in color {color}. Expected RGB 3-tuple of ints.")
            if channel < 0 or channel > 255:
                raise ValueError(f"Out of range value {channel} in color {color}. Expected RGB values to be 0-255.")


class Voxel:
    def __init__(self, color=0):
        self._color = color

    def __eq__(self, other):
        if isinstance(other, Voxel):
            return self._color == other._color
        elif isinstance(other, int):
            return self._color == other

        try:
            return self._color == int(other)
        except Exception as e:
            raise ValueError(f"Unable to compare Voxel and {type(other)} :: {str(e)}")

    def __str__(self):
        return str(self._color)

    def __int__(self):
        return int(self._color)

    def subtract(self, amount=1):
        return self.add(-1 * amount)

    def add(self, amount=1):
        if self._color == 0:
            return self
        if not isinstance(amount, int):
            raise ValueError(f"Invalid increment type {type(amount)}")
        if self._color + amount < 0:
            amount += 1
        elif amount + self._color > 256:
            amount += 1
        self._color = (self._color + amount) % 256
        if self._color == 0:  # loop back 255 -> 1 or 1 -> 255 if subtracting
            if amount < 0:
                self._color = 255
            else:
                self._color = 1
        return self

    def set(self, color):
        color = int(color)
        if color < 0 or color > 255:
            raise ValueError(f"Invalid color index {color}. It must be 0-255")
        self._color = color
        return self

    def get(self):
        return self._color


class Entity:
    def __init__(self, x=0, y=0, z=0, data=None, texture=None, texture_file=None):
        if data is None:
            self.x = x
            self.y = y
            self.z = z
            self._voxels = np.zeros((x, y, z), dtype=int)
        else:
            if type(data) != np.ndarray:
                raise TypeError(f"Expected `data` to be an NumPy ndarray, but received f{type(data)}")
            elif data.dtype != int:
                raise TypeError(f"Expected `data` have dtype=int, but received f{data.dtype}")
            elif data.shape != (x, y, z) and (x, y, z) != (0, 0, 0):
                raise ValueError(f"Expected `data` ndarray with shape ({x}, {y}, {z}) but found shape {data.shape}")
            self.from_dense(data)

        self._texture = None
        self.texture_file = None
        if texture and texture_file:
            raise ValueError("You must provide `texture`, `texture_file`, or neither.")
        elif texture and not texture_file:
            self.set_texture(texture)
        elif texture_file and not texture:
            self.texture_file = texture_file

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        if self.x != other.x or self.y != other.y or self.z != other.z:
            return False
        return np.array_equal(self.get_dense(), other.get_dense())

    def __str__(self):
        s = f"Entity with dimensions x={self.x}, y={self.y}, z={self.z}"
        return s

    def set_texture(self, texture):
        if texture is not None:
            validate_and_pad_texture(texture)
        self._texture = texture

    def get_texture(self, padded=True):
        if padded:
            return [(-1, -1, -1)].extend(self._texture)
        else:
            return self._texture

    def from_file(self, filename):
        voxels = VoxParser(filename).parse().to_dense()
        voxels = np.flip(voxels, axis=2)
        self._voxels = voxels
        self.x = len(self._voxels)
        self.y = len(self._voxels[0])
        self.z = len(self._voxels[0][0])
        return self

    def from_dense(self, dense):
        self.x = len(dense)
        self.y = len(dense[0])
        self.z = len(dense[0][0])
        self._voxels = dense
        return self

    def write(self, filename):
        # TODO: fix this on the back end
        writing_voxels = np.copy(self._voxels)
        writing_voxels = np.rot90(np.fliplr(np.swapaxes(writing_voxels, 0, 1)), k=3, axes=(1, 2))
        writing_voxels = np.flip(writing_voxels, axis=1)
        vox = Vox.from_dense(writing_voxels)
        VoxWriter(filename, vox).write()

    def save(self, filename):
        self.write(filename)

    def swap_axes(self, a, b):
        self._voxels = np.swapaxes(self._voxels, a, b)
        return self

    def rotate(self, k, axes):
        self._voxels = np.rot90(self._voxels, k=k, axes=axes)
        return self

    def get_dense(self):
        return self._voxels

    def all_voxels(self):
        return self._voxels.flatten()

    def flip(self):
        self._voxels = np.flip(self._voxels, 2)

    def get(self, x, y, z):
        if x >= self.x:
            raise IndexError(f"Dimension X out of bounds in get. Received {x} but max is {self.x - 1}")
        elif y >= self.y:
            raise IndexError(f"Dimension Y out of bounds in get. Received {y} but max is {self.y - 1}")
        elif z >= self.z:
            raise IndexError(f"Dimension Z out of bounds in get. Received {z} but max is {self.z - 1}")

        return Voxel(self._voxels[x, y, z])

    def set(self, x, y, z, color):
        color = int(color)
        if color < 0 or color > 255:
            raise IndexError(f"Color {color} out of bounds [0-255]")
        self._voxels[x, y, z] = color

    def get_layer(self, z):
        if z > self.z:
            raise IndexError(f"Dimension Z out of bounds in get_layer. Received {z} but max is {self.z}")
        return self._voxels[:, :, z]

    def set_layer(self, z, layer):
        if type(layer) != np.ndarray:
            raise TypeError(f"Invalid input type {type(layer)}, please use np.ndarray")
        elif layer.shape != (self.x, self.y):
            raise IndexError(f"Mismatched dimensions in set_layer."
                             f" Received ({len(layer)}, {len(layer[0])})"
                             f" but expected ({self.x}, {self.y})")
        elif self._voxels.dtype != layer.dtype:
            raise TypeError(f"Layer has dtype of {layer.dtype}, but should be {self._voxels.dtype}")
        log.debug(f"Setting layer {z} to {layer}")
        self._voxels[:, :, z] = layer

    def layers(self):
        for _z in range(self.z):
            yield self.get_layer(_z)
