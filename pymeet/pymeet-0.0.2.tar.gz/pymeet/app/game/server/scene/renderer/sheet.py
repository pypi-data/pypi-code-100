from typing import Dict, Tuple, Optional
import json
import os

import pygame as pg
from pygame import Surface

package_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.abspath(os.path.join(package_dir, '../../../../..', 'img'))


class CharacterSpriteMapper:
    def __init__(self, center: Tuple[int, int], position: Tuple[int, int], dimension: Tuple[int, int]):
        self.center = center
        self.position = position
        self.dimension = dimension

    @classmethod
    def from_dict(cls, d, scale=1.0) -> 'CharacterSpriteMapper':
        center = d['center'][0]*scale, d['center'][1]*scale
        position = d['position'][0]*scale, d['position'][1]*scale
        dimension = d['dimension'][0]*scale, d['dimension'][1]*scale
        return cls(center=center, position=position, dimension=dimension)


class SpriteSheet:
    def __init__(self, path: str, scale: float = 1.0):
        self.path: str = path
        self._scale: float = scale

        self._mapper: Optional[Dict[str, CharacterSpriteMapper]] = None
        self._sheet: Optional[Surface] = None

    def scale(self, scale):
        if self._sheet is None and self._mapper is None:
            self._scale = scale
        else:
            raise NotImplementedError()

    @property
    def mapper(self):
        if self._mapper is None:
            mapper_path = os.path.join(self.path, 'mapper.json')
            with open(mapper_path) as mapper_file:
                mapper_config = json.load(mapper_file)
            self._mapper = {key: CharacterSpriteMapper.from_dict(mapper, scale=self._scale)
                            for key, mapper in mapper_config.items()}

        return self._mapper

    @property
    def sheet(self):
        if self._sheet is None:
            img = pg.image.load(os.path.join(self.path, 'sheet.png')).convert_alpha()
            _, _, width, height = img.get_rect()
            size = int(width*self._scale), int(height*self._scale)
            self._sheet = pg.transform.scale(img, size)
        return self._sheet

    def get_dimension(self, key) -> Tuple[int, int]:
        return self.mapper[key].dimension

    def render_at_center(self, key: str, destination: Surface, position: Tuple[float, float]):
        config = self.mapper[key]

        position = position[0]-config.center[0], position[1]-config.center[1]
        destination.blit(self.sheet, [*position, *config.dimension], pg.Rect(*config.position, *config.dimension))

    def render(self, key: str, destination: Surface, position: Tuple[float, float]):
        config = self.mapper[key]

        destination.blit(self.sheet, [*position, *config.dimension], pg.Rect(*config.position, *config.dimension))


character_sheet: SpriteSheet = SpriteSheet(os.path.join(img_dir, 'character/main'))
