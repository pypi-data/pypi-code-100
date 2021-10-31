from pymeet.core.registry import Registry
from pymeet.core.game.character.id import CharacterId
from pymeet.core.game.character.view import CharacterView


def view_from_id(character_id: str) -> CharacterView:
    reg = Registry()
    character = reg.character_repository.from_id(CharacterId(character_id))
    view = CharacterView.from_character(character)
    return view
