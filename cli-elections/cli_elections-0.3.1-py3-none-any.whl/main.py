from __future__ import print_function, unicode_literals

from typing import Dict

import inquirer as inquirer

from cli_elections.src.parser import get_all_parties, get_all_villages, get_all_districts, get_election_result_for_village
from cli_elections.src.downloader import get_election_results
from cli_elections.src.entities.district import District
from cli_elections.src.entities.party import Party
from cli_elections.src.entities.village import Village
from cli_elections.src.graph import get_bar_graph
from cli_elections.src.question import get_input, get_select


def main():
    all_villages: Dict[str, Village] = get_all_villages('cli_elections/data/pscoco.csv')
    all_districts: Dict[str, District] = get_all_districts('cli_elections/data/cnumnuts.csv')
    all_parties: Dict[str, Party] = get_all_parties('cli_elections/data/psrkl.csv')

    print('Election cli app')

    question = get_input('Enter the city for which you want to view election results')
    inserted_city_name = inquirer.prompt(question)['question']

    possible_villages = Village.get_village_id(city_name=inserted_city_name, villages=all_villages)

    village_id = None

    if len(possible_villages) == 1:
        village_id = possible_villages[0].id

    if len(possible_villages) > 1:
        choices = [
            (f'{possible_village.name} - {all_districts[possible_village.district_id].name}', possible_village.id)
            for possible_village in possible_villages
        ]
        question = get_select(message='Select city from possibilities', choices=choices)
        village_id = inquirer.prompt(question)['question']

    if not village_id:
        print('No city found')
        exit()

    village: Village = all_villages[village_id]
    district: District = all_districts[village.district_id]
    election_results = get_election_results(district.nut_id)

    parties, votes = get_election_result_for_village(
        village_id=village.id, election_results=election_results, all_parties=all_parties)

    plt = get_bar_graph(title=village.name, x=parties, y=votes, all_parties=all_parties)
    plt.show()


if __name__ == "__main__":
    main()
