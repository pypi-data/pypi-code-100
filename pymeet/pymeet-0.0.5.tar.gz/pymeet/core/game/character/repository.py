from typing import Dict

from .id import CharacterId
from .main import Character


class IdAlreadyExistsException(Exception):
    pass


class IdNotFoundException(Exception):
    pass


class CharacterRepository:
    def __init__(self):
        self._store: Dict[CharacterId, Character] = dict()

    def add(self, character: Character):
        id_ = character.get_id()
        if id_ in self._store:
            raise IdAlreadyExistsException(f'Character Id {id_} already exists')

        self._store[id_] = character

    def remove(self, character_id: CharacterId):
        try:
            del self._store[character_id]
        except KeyError:
            raise IdNotFoundException(f'Character Id {character_id} not exists')

    def from_id(self, character_id: CharacterId):
        try:
            return self._store[character_id]
        except KeyError:
            raise IdNotFoundException(f'Character Id {character_id} not exists')

    def update_all(self):
        for character in self._store.values():
            character.update()
