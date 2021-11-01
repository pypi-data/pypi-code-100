from typing import List
from src.actions.gen import Gen
from src.actions.test import Test
from src.actions.submit import Submit
from src.actions.config import Config
from src.actions.open import Open
from src.actions.version import Version
from src.actions.update import Update
from src.base import Action

map_key_to_class = {
    'gen': Gen,
    'test': Test,
    'submit': Submit,
    'config': Config,
    'open': Open,
    'version': Version,
    'update': Update
} 


def arg_parse(args: List[str]) -> Action:
    ''' Generate an appropriate command class based on user command stirng '''
    if len(args) == 0:
        raise ValueError(f'No command provided to kt')
    if args[0] not in map_key_to_class:
        raise ValueError(f'First argument should be one of {list(map_key_to_class.keys())}')
    return map_key_to_class[args[0]](*args[1:])
