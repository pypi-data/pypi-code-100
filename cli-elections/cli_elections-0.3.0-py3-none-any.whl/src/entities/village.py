from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Village:
    district_id: str
    id: str
    name: str

    @staticmethod
    def get_village_id(city_name: str, villages: Dict) -> List:
        possible_villages = []

        for village in villages.values():
            if city_name in village.name:
                possible_villages.append(village)

        return possible_villages
