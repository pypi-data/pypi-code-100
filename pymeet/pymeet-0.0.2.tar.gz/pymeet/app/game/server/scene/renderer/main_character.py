from typing import Tuple, Optional
from pygame import Surface

from pymeet.core.game.character.view import CharacterView
from pymeet.core.game.character.direction import Direction
from pymeet.core.game.character.walk.state import WalkState
from pymeet.core.game.character.idle.state import IdleState

from .base import CharacterRenderer
from .sheet import character_sheet


class MainCharacterRenderer(CharacterRenderer):
    def __init__(self, screen_center: Tuple[float, float]):
        self._screen_center: Tuple[float, float] = screen_center
        self._walk_animation_id: int = 0
        self._previous_side: str = ''
        self._previous_heading: Optional[Direction] = None

    def render_character(self, screen: Surface, character: CharacterView):
        state = character.state

        if isinstance(state, IdleState):
            key = self._get_idle_render_key(character)
        elif isinstance(state, WalkState):
            key = self._get_walk_render_key(character)
        else:
            raise NotImplementedError()

        self._render_from_key(screen, key)

    def _render_from_key(self, screen: Surface, key: str):
        character_sheet.render_at_center(key, screen, self._screen_center)

    def _get_walk_render_key(self, character: CharacterView) -> str:
        side = self._heading_side(character)

        animation_id = int(self._walk_animation_id / 4) + 1
        if self._walk_animation_id == 15:
            self._walk_animation_id = 0
        else:
            self._walk_animation_id += 1

        return f'{side}-walk-{animation_id}'

    def _get_idle_render_key(self, character: CharacterView) -> str:
        side = self._heading_side(character)
        return f'{side}-idle'

    def _heading_side(self, character: CharacterView) -> str:
        heading = character.heading

        if heading.is_up():
            side = 'back'
        elif heading.is_down():
            side = 'front'
        elif heading.is_right():
            side = 'right'
        elif heading.is_left():
            side = 'left'
        elif heading.is_up_right():
            if self._previous_heading != heading:
                if self._previous_side == 'back':
                    side = 'right'
                else:
                    side = 'back'
            else:
                side = self._previous_side
        elif heading.is_down_right():
            if self._previous_heading != heading:
                if self._previous_side == 'front':
                    side = 'right'
                else:
                    side = 'front'
            else:
                side = self._previous_side
        elif heading.is_up_left():
            if self._previous_heading != heading:
                if self._previous_side == 'back':
                    side = 'left'
                else:
                    side = 'back'
            else:
                side = self._previous_side
        elif heading.is_down_left():
            if self._previous_heading != heading:
                if self._previous_side == 'front':
                    side = 'left'
                else:
                    side = 'front'
            else:
                side = self._previous_side
        else:
            raise NotImplementedError()
        self._previous_heading = heading
        self._previous_side = side

        return side
