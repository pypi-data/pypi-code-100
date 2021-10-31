from typing import Tuple, Optional
from math import floor
import pygame as pg
from pygame import Surface

from .base import GroundRenderer


def unit_to_pixel(position: Tuple[float, float]) -> Tuple[float, float]:
    return position[0]*10, position[1]*10


class GridGroundRenderer(GroundRenderer):
    def __init__(self, dimension: Tuple[int, int], screen_center: Tuple[float, float], grid_length: int = 75):
        self._dimension: Tuple[int, int] = dimension
        self._screen_center: Tuple[float, float] = screen_center
        self._grid_length: int = grid_length

        self._grid_surface: Optional[Surface] = None

    @property
    def grid_surface(self) -> Surface:
        if self._grid_surface is None:
            self._grid_surface = self._generate_grid()
        return self._grid_surface

    def _generate_grid(self) -> Surface:
        assert self._grid_surface is None
        width, height = self._dimension[0] + 2 * self._grid_length, self._dimension[1] + 2 * self._grid_length
        width_half, height_half = width/2, height/2
        surface = Surface((width, height), pg.SRCALPHA).convert_alpha()

        n_cols_complete = floor(width_half/self._grid_length)
        col_residue = width_half - n_cols_complete*self._grid_length
        x = col_residue
        while x <= width_half:
            pg.draw.line(surface, 'darkgrey', (x, 0), (x, height), width=2)
            pg.draw.line(surface, 'darkgrey', (width-x, 0), (width-x, height), width=2)
            x += self._grid_length

        n_rows_complete = floor(height_half/self._grid_length)
        row_residue = height_half - n_rows_complete*self._grid_length
        y = row_residue
        while y <= width_half:
            pg.draw.line(surface, 'darkgrey', (0, y), (width, y), width=2)
            pg.draw.line(surface, 'darkgrey', (0, height-y), (width, height-y), width=2)
            y += self._grid_length
        return surface

    def render_ground(self, screen: Surface, character_position: Tuple[float, float]):
        screen.fill('grey')
        x, y = unit_to_pixel(character_position)
        t = self._grid_length
        area = pg.Rect(t + x % t, t + y % t, *self._dimension)
        screen.blit(self.grid_surface, [0, 0, *self._dimension], area)
