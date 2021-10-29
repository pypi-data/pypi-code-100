import csv
from typing import Dict, Tuple, List

from cli_elections.src.entities.district import District
from cli_elections.src.entities.party import Party
from cli_elections.src.entities.village import Village

PARTIES_ID = 0
PARTIES_NAME = 5

VILLAGES_DISTRICT_ID = 1
VILLAGES_ID = 4
VILLAGES_NAME = 5

DISTRICT_ID = 0
DISTRICT_NUT_ID = 1
DISTRICT_NAME = 2

DISTRICT_NUT_EXCEPTIONS = {
    '1100': 'CZ0100'  # ohack for Prague
}


def get_all_parties(source_file: str) -> Dict[str, Party]:
    parties = {}
    with open(source_file, 'rt', encoding='windows-1250') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)  # skip headers
        for row in reader:
            _id = row[PARTIES_ID]
            name = row[PARTIES_NAME]

            parties[_id] = Party(_id=_id, name=name)

    return parties


def get_all_villages(source_file: str) -> Dict[str, Village]:
    villages = {}
    with open(source_file, 'rt', encoding='windows-1250') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            district_id = row[VILLAGES_DISTRICT_ID]
            _id = row[VILLAGES_ID]
            name = row[VILLAGES_NAME]

            villages[_id] = Village(district_id=district_id, id=_id, name=name)

    return villages


def get_all_districts(source_file: str):
    districts = {}
    with open(source_file, 'rt', encoding='windows-1250') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            _id = row[DISTRICT_ID]
            nut_id = row[DISTRICT_NUT_ID]
            name = row[DISTRICT_NAME]

            if _id in DISTRICT_NUT_EXCEPTIONS:
                nut_id = DISTRICT_NUT_EXCEPTIONS[_id]

            districts[_id] = District(id=_id, nut_id=nut_id, name=name)

    return districts


def get_election_result_for_village(village_id: str, election_results: Dict, all_parties: Dict[str, Party]) -> Tuple[List, List]:
    parties = []
    votes = []
    for v in election_results['VYSLEDKY_OKRES']['OBEC']:
        if v['@CIS_OBEC'] == village_id:
            for k in v['HLASY_STRANA']:
                parties.append(all_parties[k['@KSTRANA']].name)
                votes.append(int(k['@HLASY']))

    return parties, votes
