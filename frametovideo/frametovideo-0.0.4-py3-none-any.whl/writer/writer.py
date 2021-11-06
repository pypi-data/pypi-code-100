import glob
from abc import ABC
from enum import Enum
from os import path

import cv2
from dataclasses import dataclass


class ImageType(Enum):
    JPG = '.jpg'
    PNG = '.png'

@dataclass
class Writer(ABC):
    frames_path: str
    output_path: str
    frame_size: (int, int)
    fps: int
    image_type: ImageType

    def convert(self):
        pass


class Mp4Writer(Writer):

    def convert(self):
        self._consistency_check()
        out = cv2.VideoWriter(f'{self.output_path}output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.fps, self.frame_size)

        for filename in glob.glob(f'{self.frames_path}*{self.image_type}'):
            img = cv2.imread(filename)
            out.write(img)

        out.release()

    def _consistency_check(self):

        if not path.isdir(self.frames_path):
            raise OSError(f'The provided path to the directory containing the frames: {self.frames_path} is not a '
                          f'directory.')

        if not path.exists(self.frames_path):
            raise OSError(f'The provided path to the directory containing the frames: {self.frames_path} does not exist.')

        width, height = self.frame_size
        if width < 1 or height < 0:
            raise ValueError(f'The frame width and height must be >= 1. {self.frame_size}')

        if self.fps < 1:
            raise ValueError(f'The frames per second must be >= 1. {self.fps}')

        if not path.exists(self.output_path):
            raise OSError(f'The provided output path: {self.output_path} does not exist.')



