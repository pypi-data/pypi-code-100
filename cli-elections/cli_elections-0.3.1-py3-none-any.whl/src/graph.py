import plotext as plt

from cli_elections.src.entities.party import Party


def get_bar_graph(title, x, y, all_parties) -> plt:
    """ Get bar graph with coloured bars (simple ohack because plotext library is stupider than i thought)
    """
    plt.title(title)

    for i, party_name in enumerate(reversed(x)):
        if i == len(x) - 1:
            y.append(0)  # ugly ohack because plotext dont support bar with one record TODO send fix MR to library
        plt.bar(x, y, color=Party.get_party_color(party_name, all_parties.values()))
        y.pop()

    return plt
