from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional, Dict, List, Tuple
try:
    from anime_reference.constants import *
    from anime_reference.utils import clean_str_list, format_episode_links, clean_text
except:
    from constants import *
    from utils import clean_str_list, format_episode_links, clean_text

class AttackOnTitan:
    """
    A class to represent the AttackOnTitan anime title.
    ...

    Attributes
    ----------
    title : str
        title of the anime

    Methods
    -------
    _check_episode_name(episode_name):
        Checks if the episode name is valid

    _get_link():
        Gets the link of episodes associated with the anime title

    _episode_link_dict():
        Gets the episode:link dictionary

    get_episodes():
        Gets a dataframe of episode #, title, and airdate (Japanese and English)

    episode_summary(episode_name):
        Gets the summary of the given episode name

    episode_names():
        Gets a list of episode names
    """

    def __init__(self) -> None:
        self.title = "attack on titan"
        return None
    
    @property
    def _get_link(self) -> str:
        return AoA[self.title] # link for the all epsiodes, movies of the different naruto titles
    
    def _check_episode_name(self, episode_name: str) -> None:
        if episode_name not in self.episode_names:
            print(f"Episode \"{episode_name}\" is not a valid {self.title} episode name.")
            return None

    @property
    def _episode_link_dict(self) -> Optional[Dict[str, str]]:
        link = self._get_link
        response = get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = list(map(str, soup.find_all('table')))
            episode_names, links = [], []
            links = clean_str_list(tables, search_str='/wiki/"(.*)"')
            
    @property
    def episode_summary(self, episode_name) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
        link = self._get_link()
        for df in pd.read_html(link)
            print(df['Title'][0])
            print(df['Title'][1])
