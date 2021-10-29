import random
from typing import Dict

from diskcache import Cache
import plotext.utility as utility


class Party:
    id: str
    name: str
    color: str

    def __init__(self, _id, name) -> None:
        self.id = _id
        self.name = name

        cache = Cache()
        cache.close()
        with Cache(directory="/tmp/cache") as reference:
            self.color = reference.get(_id)
            if not self.color:
                colors_pallete = utility.color_sequence

                if 'white' in colors_pallete:
                    colors_pallete.remove('white')

                self.color = random.choice(colors_pallete)
                reference.set(_id, self.color)

    @staticmethod
    def get_party_color(party_name: str, parties: Dict) -> str:
        for party in parties:
            if party.name == party_name:
                return party.color

        return 'black'
