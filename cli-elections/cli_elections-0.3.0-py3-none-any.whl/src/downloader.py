from typing import Dict

import requests
import xmltodict

BASE_URL = 'https://volby.cz/pls/ps2021/vysledky_okres'


def get_election_results(nut_id: str) -> Dict:
    params = {
        'nuts': nut_id
    }
    response = requests.get(url=BASE_URL, params=params)

    return xmltodict.parse(response.content)
